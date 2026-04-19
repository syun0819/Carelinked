<template>
  <div class="search-page">
    <Header />

    <section class="page-title">
      <h1>Find a Bed</h1>
      <p>Get a personalised estimate of how long you may wait for an aged care placement.</p>
    </section>

    <SearchBar
      v-model="searchQuery"
      v-model:search-type="searchType"
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
      <FilterPanel
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
        @update:selectedCareTypes="selectedCareTypes = $event"
        @update:selectedRemoteness="selectedRemoteness = $event"
        @update:minBeds="minBeds = $event"
        @update:maxBeds="maxBeds = $event"
        @update:distance="distance = $event"
        @update:distanceFilterEnabled="distanceFilterEnabled = $event"
        @reset="resetFilters"
      />

      <div class="results-main">
        <ResultsHeader
          :count="activeView === 'map' ? mapResultCount : totalResults"
          :start="activeView === 'map' ? (mapResultCount ? 1 : 0) : startIndex"
          :end="activeView === 'map' ? mapResultCount : endIndex"
          :distance="distance"
          :sort-by="sortBy"
          :viewMode="activeView"
          @update:sortBy="sortBy = $event"
        />

        <div v-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="activeView === 'list' && !loading && totalResults === 0 && searchMessage" class="status-message">{{ searchMessage }}</div>

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
import FooterSection from '../components/FooterSection.vue'

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

const currentPage = ref(1)
const pageSize = 4
const mapResultCount = ref(0)
const totalResults = ref(0)
const searchMessage = ref('')

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

function getDistanceValue(facility) {
  return facility.distanceKm ?? facility.distance ?? Number.MAX_SAFE_INTEGER
}

const filteredFacilities = computed(() => facilities.value)

watch(
  () => route.query.careType,
  (newCareType) => {
    selectedCareTypes.value = normalizeCareTypes(newCareType)
    currentPage.value = 1
  },
  { immediate: true }
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
    currentPage.value = 1
    syncStateToQuery()
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

  currentPage.value = route.query.page ? Number(route.query.page) : 1
}

function syncStateToQuery() {
  const uniqueCareTypes = [...new Set(selectedCareTypes.value)]

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
      page: currentPage.value !== 1 ? String(currentPage.value) : undefined
    }
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
  padding: 0px 0 60px;
  color: #1f2d2a;
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
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 26px;
  align-items: start;
}

.results-main {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
}

.results-main > * {
  min-width: 0;
  max-width: 100%;
}

.pagination-row {
  grid-column: 1 / -1;
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
}
</style>
