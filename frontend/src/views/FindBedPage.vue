<template>
  <div class="search-page">
    <Header />

    <section class="page-title page-animate">
      <h1>{{ pageTitle }}</h1>
      <p>{{ pageSubtitle }}</p>
    </section>

    <SearchBar
      v-model="searchQuery"
      v-model:search-type="searchType"
      :matching-active="matchingActive"
      :match-weights="matchWeights"
      :match-disabled="activeView === 'map'"

      @open-match-modal="matchModalOpen = true"
      @clear-match="clearMatching"
    />

    <section class="view-toggle">
      <button
        class="view-btn"
        :class="{ active: activeView === 'list' }"
        @click="activeView = 'list'"
      >
        ≡ List View
      </button>

      <button
        class="view-btn"
        :class="{ active: activeView === 'map' }"
        @click="activeView = 'map'"
      >
        ⊞ Map View
      </button>
    </section>

    <section class="results-layout">
      <ResultsHeader
        class="results-header-row"
        :count="activeView === 'map' ? mapResultCount : totalResults"
        :start="activeView === 'map' ? (mapResultCount ? 1 : 0) : startIndex"
        :end="activeView === 'map' ? mapResultCount : endIndex"
        :distance="distance"
        :sort-by="sortBy"
        :viewMode="activeView"
        :matching-active="matchingActive"
        @update:sortBy="sortBy = $event"
        @clear-match="clearMatching"
      />

      <FilterPanel
        class="filters-column"
        :selected-care-types="selectedCareTypes"
        :selected-remoteness="selectedRemoteness"
        :min-beds="minBeds"
        :max-beds="maxBeds"
        :distance="distance"
        :distanceFilterEnabled="distanceFilterEnabled"
        :distanceWarning="distanceWarning"
        :care-type-options="careTypeOptions"
        :min-distance="minDistance"
        :max-distance="maxDistance"
        @apply="applyFilters"
        @reset="resetFilters"
      />

      <div class="results-main">
        <div v-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="activeView === 'list' && !loading && totalResults === 0 && searchMessage" class="status-message">{{ searchMessage }}</div>
        <div v-if="activeView === 'list' && matchingActive" class="match-thresholds" aria-label="Match score thresholds">
          <strong>Match thresholds:</strong>
          <span>Strong Match: 75%+</span>
          <span>Moderate Match: 50-74%</span>
          <span>Lower Match: below 50%</span>
        </div>

        <FacilityCardSkeleton v-if="loading && activeView === 'list'" />

        <ListSection
          v-else-if="activeView === 'list'"
          :facilities="filteredFacilities"
        />

        <MapSection
          v-else
          :search-query="searchQuery"
          :search-type="searchType"
          :selected-care-types="selectedCareTypes"
          :distance="distance"
          :distance-filter-enabled="distanceFilterEnabled"
          :user-lat="null"
          :user-lng="null"
          :focus-lat="focusLat"
          :focus-lng="focusLng"
          :is-active="activeView === 'map'"
          @update:count="mapResultCount = $event"
        />

      </div>

      <PaginationBar
        v-if="activeView === 'list'"
        class="pagination-row"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="totalResults"
        @page-change="handlePageChange"
      />
    </section>

    <FooterSection />
    <PreferenceMatchModal
      v-model="matchModalOpen"
      :initial-weights="matchWeights"
      @confirm="applyMatchWeights"
    />
    <CompareBar ref="compareBarRef" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchFacilities } from '../services/facilitiesApi'
import { mapFacilityCard } from '../utils/facilityMappers'
import Header from '../components/Header.vue'
import SearchBar from '../components/search/SearchBar.vue'
import FilterPanel from '../components/search/FilterPanel.vue'
import ResultsHeader from '../components/search/ResultsHeader.vue'
import ListSection from '../components/search/ListSection.vue'
import FacilityCardSkeleton from '../components/FacilityCardSkeleton.vue'
import MapSection from '../components/MapSection.vue'
import PaginationBar from '../components/search/PaginationBar.vue'
import PreferenceMatchModal from '../components/search/PreferenceMatchModal.vue'
import FooterSection from '../components/FooterSection.vue'
import CompareBar from '../components/CompareBar.vue'

const compareBarRef = ref(null)

const route = useRoute()
const router = useRouter()

const initialized = ref(false)
const facilities = ref([])
const loading = ref(false)
const error = ref('')

const searchQuery = ref('')
const searchType = ref('')
const activeView = ref('list')
const sortBy = ref('name')

const selectedCareTypes = ref([])
const selectedRemoteness = ref('')
const minBeds = ref(null)
const maxBeds = ref(null)

const distance = ref(10)
const minDistance = 1
const maxDistance = 20
const distanceFilterEnabled = ref(false)
const distanceWarning = ref('')
const focusLat = ref(null)
const focusLng = ref(null)

const currentPage = ref(1)
const pageSize = 4
const mapResultCount = ref(0)
const totalResults = ref(0)
const searchMessage = ref('')
const matchModalOpen = ref(false)
const matchWeights = ref(null)
let applyingRouteState = false
let syncingToRoute = false

const matchingActive = computed(() => {
  if (!matchWeights.value) return false
  return Object.values(matchWeights.value).reduce((sum, value) => sum + Number(value || 0), 0) === 100
})

const pageTitle = computed(() => activeView.value === 'map' ? 'Map Search' : 'Find Care')
const pageSubtitle = computed(() => (
  activeView.value === 'map'
    ? 'Explore aged care facilities and local risk overlays on the map.'
    : 'Search and compare aged care facilities in a list view.'
))

const careTypeOptions = [
  { value: 'Residential', label: 'Residential' },
  { value: 'Transition Care', label: 'Transition Care' },
  { value: 'Short-Term Restorative Care (STRC)', label: 'Short-Term Restorative Care (STRC)' },
  { value: 'Multi-Purpose Service', label: 'Multi-Purpose Service' },
  {
    value: 'National Aboriginal and Torres Strait Islander Aged Care Program',
    label: 'Indigenous Care'
  }
]

async function fetchFacilities() {
  loading.value = true
  error.value = ''
  distanceWarning.value = ''

  try {
    const q = searchQuery.value.trim()

    const params = {
      limit: pageSize,
      offset: (currentPage.value - 1) * pageSize,
      sort_by: sortBy.value
    }

    if (q !== '') {
      params[getSearchParamType(q)] = q
    }

    if (selectedCareTypes.value.length > 0) {
      params.care_type = selectedCareTypes.value
    }

    if (selectedRemoteness.value) {
      params.abs_remoteness = selectedRemoteness.value
    }

    if (minBeds.value != null && minBeds.value > 0) {
      params.min_beds = minBeds.value
    }

    if (maxBeds.value != null && maxBeds.value > 0) {
      params.max_beds = maxBeds.value
    }

    if (distanceFilterEnabled.value) {
      if (!q) {
        distanceWarning.value = 'Please enter a suburb or postcode to use distance filtering'
      } else {
        params.max_distance_km = distance.value
      }
    }

    if (matchingActive.value) {
      Object.assign(params, matchWeights.value)
    }

    console.log('search params:', params)

    const data = await searchFacilities(params)
    console.log('search response:', data)

    const rawFacilities = data.results || data.items || data.facilities || []
    facilities.value = rawFacilities.map(mapFacilityCard)
    totalResults.value = data.total || facilities.value.length
    searchMessage.value = data.message || ''
  } catch (err) {
    console.error('Failed to load facilities:', err)
    error.value = 'Failed to load facilities.'
    facilities.value = []
    totalResults.value = 0
    searchMessage.value = ''
  } finally {
    loading.value = false
  }
}

const startIndex = computed(() => {
  return totalResults.value === 0
    ? 0
    : (currentPage.value - 1) * pageSize + 1
})

const endIndex = computed(() => {
  return Math.min(currentPage.value * pageSize, totalResults.value)
})

function handlePageChange(page) {
  currentPage.value = page
  syncStateToQuery()
  fetchFacilities()
}

function handleSearch() {
  currentPage.value = 1
  syncStateToQuery()
  fetchFacilities()
}

function resetFilters() {
  searchQuery.value = ''
  searchType.value = ''
  selectedCareTypes.value = []
  selectedRemoteness.value = ''
  minBeds.value = null
  maxBeds.value = null
  distance.value = 10
  distanceFilterEnabled.value = false
  distanceWarning.value = ''
  sortBy.value = 'name'
  currentPage.value = 1
  syncStateToQuery()
}

function applyFilters(filters) {
  selectedCareTypes.value = filters.selectedCareTypes
  selectedRemoteness.value = filters.selectedRemoteness
  minBeds.value = filters.minBeds
  maxBeds.value = filters.maxBeds
  distance.value = filters.distance
  distanceFilterEnabled.value = filters.distanceFilterEnabled
}

function applyMatchWeights(weights) {
  matchWeights.value = { ...weights }
  currentPage.value = 1
  syncStateToQuery()
  fetchFacilities()
}

function clearMatching() {
  matchWeights.value = null
  currentPage.value = 1
  fetchFacilities()
}

function getDistanceValue(facility) {
  return facility.distanceKm ?? facility.distance ?? Number.MAX_SAFE_INTEGER
}

const filteredFacilities = computed(() => facilities.value)

watch(
  () => route.query.careType,
  (newCareType) => {
    const nextCareTypes = normalizeCareTypes(newCareType)

    if (arraysEqual(nextCareTypes, selectedCareTypes.value)) {
      return
    }

    selectedCareTypes.value = nextCareTypes
    currentPage.value = 1
  },
  { immediate: true }
)

watch(
  () => route.query.view,
  (view) => {
    const nextView = view === 'map' ? 'map' : 'list'
    if (activeView.value !== nextView) {
      activeView.value = nextView
    }
  }
)

watch(
  [
    searchQuery,
    searchType,
    selectedCareTypes,
    selectedRemoteness,
    minBeds,
    maxBeds,
    distanceFilterEnabled,
    distance,
    sortBy,
    activeView
  ],
  () => {
    if (!initialized.value) return
    if (applyingRouteState) return
    currentPage.value = 1
    syncStateToQuery()
    fetchFacilities()
  },
  { deep: true }
)

watch(
  () => route.query,
  async () => {
    if (!initialized.value) return
    if (syncingToRoute) return

    applyingRouteState = true
    applyQueryToState()
    await nextTick()
    applyingRouteState = false
    fetchFacilities()
  },
  { deep: true }
)

function applyQueryToState() {
  searchQuery.value = route.query.search ?? ''
  searchType.value = normalizeSearchType(route.query.searchType ?? '')
  activeView.value = route.query.view ?? 'list'
  sortBy.value = route.query.sortBy ?? 'name'

  selectedCareTypes.value = normalizeCareTypes(route.query.careType)

  selectedRemoteness.value = route.query.remoteness ?? ''

  minBeds.value = route.query.minBeds ? Number(route.query.minBeds) : null
  maxBeds.value = route.query.maxBeds ? Number(route.query.maxBeds) : null

  distance.value = route.query.distance ? Number(route.query.distance) : 10
  distanceFilterEnabled.value = route.query.distanceEnabled === 'true'
  focusLat.value = route.query.focusLat ? Number(route.query.focusLat) : null
  focusLng.value = route.query.focusLng ? Number(route.query.focusLng) : null

  currentPage.value = route.query.page ? Number(route.query.page) : 1
}

function syncStateToQuery() {
  const uniqueCareTypes = [...new Set(selectedCareTypes.value)]

  syncingToRoute = true
  router.replace({
    path: '/find-bed',
    query: {
      search: searchQuery.value || undefined,
      searchType: searchType.value || undefined,
      view: activeView.value !== 'list' ? activeView.value : undefined,
      sortBy: sortBy.value || undefined,
      careType: uniqueCareTypes.length ? uniqueCareTypes : undefined,
      remoteness: selectedRemoteness.value || undefined,
      minBeds: minBeds.value != null ? String(minBeds.value) : undefined,
      maxBeds: maxBeds.value != null ? String(maxBeds.value) : undefined,
      distance: distance.value !== 10 ? String(distance.value) : undefined,
      distanceEnabled: distanceFilterEnabled.value ? 'true' : undefined,
      focusLat: focusLat.value != null ? String(focusLat.value) : undefined,
      focusLng: focusLng.value != null ? String(focusLng.value) : undefined,
      page: currentPage.value !== 1 ? String(currentPage.value) : undefined
    }
  }).finally(() => {
    syncingToRoute = false
  })
}

function getSearchParamType(q) {
  const type = normalizeSearchType(searchType.value)
  if (type) return type
  return /^\d+$/.test(q) ? 'postcode' : 'keyword'
}

function normalizeSearchType(value) {
  const type = String(value).toLowerCase()
  if (['suburb', 'postcode', 'region', 'keyword'].includes(type)) return type
  return ''
}

function arraysEqual(a, b) {
  if (a.length !== b.length) return false
  return a.every((item, index) => item === b[index])
}

function normalizeCareTypes(value) {
  if (!value) return []

  if (Array.isArray(value)) {
    return [...new Set(
      value.flatMap(item =>
        String(item)
          .split(',')
          .map(v => v.trim())
          .filter(Boolean)
      )
    )]
  }

  return [...new Set(
    String(value)
      .split(',')
      .map(v => v.trim())
      .filter(Boolean)
  )]
}

onMounted(async () => {
  applyQueryToState()
  await fetchFacilities()
  initialized.value = true
})
</script>

<style scoped>
.search-page {
  background: #f7f4ee;
  min-height: 100vh;
  overflow: hidden;
  padding: 0;
  color: #1f2d2a;
  overflow-x: hidden;
  width: 100%;
  box-sizing: border-box;
}

.search-top {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto 30px;
  padding: 0 16px;
  display: flex;
  justify-content: center;
  box-sizing: border-box;
}

.page-title {
  text-align: center;
  margin-top: 135px;
  margin-bottom: 32px;
  width: 100%;
  padding: 0;
  box-sizing: border-box;
}

.page-title h1 {
  margin: 0 0 10px;
  font-size: 42px;
  font-weight: 800;
  color: #1f2d2a;
  font-family: var(--font-display);
}

.page-title p {
  font-size: 16px;
  color: #76828a;
  margin: 0;
}

.results-layout {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 330px minmax(0, 1fr);
  column-gap: 32px;
  row-gap: 10px;
  align-items: start;
  box-sizing: border-box;
}

.results-main {
  grid-column: 2;
  grid-row: 2;
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
}

.results-main > * {
  min-width: 0;
  max-width: 100%;
}

.match-thresholds {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  padding: 10px 14px;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  background: #fff;
  color: #60706b;
  font-size: 13px;
  line-height: 1.35;
}

.match-thresholds strong {
  color: #22332e;
  font-weight: 800;
}

.results-header-row {
  grid-column: 2;
  grid-row: 1;
}

.filters-column {
  grid-column: 1;
  grid-row: 2;
  position: relative;
  z-index: 2000;
}

.pagination-row {
  grid-column: 1 / -1;
  grid-row: 3;
}

.view-toggle {
  display: flex;
  justify-content: center;
  gap: 0;
  margin-bottom: 30px;
  background: white;
  border: 1.5px solid #ddd8cf;
  border-radius: 999px;
  padding: 4px;
  width: fit-content;
  margin: 0 auto 30px;
}

.view-btn {
  border: none;
  background: transparent;
  color: #2D6A5F;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  padding: 8px 22px;
  border-radius: 999px;
  transition: all 0.2s;
  font-family: var(--font-sans);
}

.view-btn.active {
  background: #557067;
  color: white;
  font-weight: 600;
}

@media (max-width: 768px) {
  .search-page {
    padding: 0;
  }

  .page-title {
    margin-top: 120px;
    margin-left: 15px;
    padding: 0 20px;
  }

  .results-layout {
    grid-template-columns: 1fr;
    padding: 0 16px;
  }

  .results-header-row,
  .filters-column,
  .results-main,
  .pagination-row {
    grid-column: 1;
    grid-row: auto;
  }
}
</style>
