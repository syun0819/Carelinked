<template>
  <div class="search-page">
    <Header />

    <section class="page-title">
      <h1>Find a Bed</h1>
      <p>Get a personalised estimate of how long you may wait for an aged care placement.</p>
    </section>

    <SearchBar v-model="searchQuery" />

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
        :selectedAvailability="selectedAvailability"
        :distance="distance"
        :care-type-options="careTypeOptions"
        :availabilityOptions="availabilityOptions"
        :min-distance="minDistance"
        :max-distance="maxDistance"
        @update:selectedCareTypes="selectedCareTypes = $event"
        @update:selectedAvailability="selectedAvailability = $event"
        @update:distance="distance = $event"
        @reset="resetFilters"
      />

      <div class="results-main">
        <ResultsHeader
          :count="filteredFacilities.length"
          :distance="distance"
          :sort-by="sortBy"
          @update:sortBy="sortBy = $event"
        />
        
        <div v-if="loading" class="status-message">Loading facilities...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>

        <ListSection
          v-if="activeView === 'list'"
          :facilities="filteredFacilities"
        />

        <MapSection
          v-else
          :search-query="searchQuery"
          :selected-care-types="selectedCareTypes"
          :distance="distance"
        />

        <PaginationBar
          :current-page="currentPage"
          :page-size="pageSize"
          :total="totalResults"
          @page-change="handlePageChange"
        />
      </div>
    </section>
    
    <FooterSection />
  
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { searchFacilities } from '../services/facilitiesApi'
import { mapFacilityCard } from '../utils/facilityMappers'

import Header from '../components/Header.vue'
import SearchBar from '../components/search/SearchBar.vue'
import FilterPanel from '../components/search/FilterPanel.vue'
import ResultsHeader from '../components/search/ResultsHeader.vue'
import ListSection from '../components/search/ListSection.vue'
import MapSection from '../components/MapSection.vue'
import PaginationBar from '../components/search/PaginationBar.vue'
import FooterSection from '../components/FooterSection.vue'

const route = useRoute()

const facilities = ref([])
const loading = ref(false)
const error = ref('')

const searchQuery = ref('')
const activeView = ref('list')
const sortBy = ref('closest')

const selectedCareTypes = ref([])
const selectedAvailability = ref([])

const distance = ref(10)
const minDistance = 1
const maxDistance = 20

const currentPage = ref(1)
const pageSize = 20
const totalResults = ref(0)

const careTypeOptions = [
  { value: 'Residential', label: 'Residential', icon: '🏠' },
  { value: 'Home Care', label: 'Home Care', icon: '♡' },
  { value: 'Transition Care', label: 'Transition Care', icon: '🔄' },
  { value: 'Short-Term Restorative Care (STRC)', label: 'Short-Term Restorative Care (STRC)', icon: '🛏️' },
  { value: 'Multi-Purpose Service', label: 'Multi-Purpose Service', icon: '🏥' },
  { value: 'National Aboriginal and Torres Strait Islander Aged Care Program', label: 'Indigenous Care', icon: '🌿' }
]

const availabilityOptions = [
  { value: 'High', label: 'High' },
  { value: 'Medium', label: 'Medium' },
  { value: 'Low', label: 'Low' }
]

async function fetchFacilities() {
  loading.value = true
  error.value = ''

  try {
    const q = searchQuery.value.trim()

    const params = {
      limit: pageSize,
      offset: (currentPage.value - 1) * pageSize
    }

    if (q) {
      if (/^\d+$/.test(q)) {
        params.postcode = q
      } else {
        params.suburb = q
      }
    }

    if (selectedCareTypes.value.length > 0) {
      params.care_type = selectedCareTypes.value.join(',')
    }

    console.log('search params:', params)

    const data = await searchFacilities(params)
    console.log('search response:', data)

    facilities.value = (data.results || data.items || data.facilities || []).map(mapFacilityCard)
    totalResults.value = data.total || 0
  } catch (err) {
    console.error('Failed to load facilities:', err)
    error.value = 'Failed to load facilities.'
    facilities.value = []
    totalResults.value = 0
  } finally {
    loading.value = false
  }
}

function handlePageChange(page) {
  currentPage.value = page
  fetchFacilities()
}

function resetFilters() {
  searchQuery.value = ''
  selectedCareTypes.value = []
  selectedAvailability.value = []
  distance.value = 10
  sortBy.value = 'closest'
  currentPage.value = 1
}

function getAvailabilityRank(level) {
  if (level === 'High') return 3
  if (level === 'Medium') return 2
  if (level === 'Low') return 1
  return 0
}

function getAvailabilityLevel(facility) {
  const beds = facility.totalBeds ?? facility.residential_places ?? 0

  if (beds >= 80) return 'High'
  if (beds <= 30) return 'Low'
  return 'Medium'
}

const filteredFacilities = computed(() => {
  let result = [...facilities.value]

  if (selectedAvailability.value.length > 0) {
    result = result.filter(f =>
      selectedAvailability.value.includes(getAvailabilityLevel(f))
    )
  }

  if (sortBy.value === 'name') {
    result.sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortBy.value === 'availability') {
    result.sort(
      (a, b) => getAvailabilityRank(getAvailabilityLevel(b)) - getAvailabilityRank(getAvailabilityLevel(a))
    )
  }

  return result
})

watch(
  () => route.query.careType,
  (newCareType) => {
    selectedCareTypes.value = newCareType ? [newCareType] : []
    currentPage.value = 1
  },
  { immediate: true }
)

watch(
  [searchQuery, selectedCareTypes, sortBy],
  () => {
    currentPage.value = 1
    fetchFacilities()
  },
  { deep: true }
)

onMounted(() => {
  fetchFacilities()
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
  margin-top: 40px;
  margin-bottom: 40px;
  font-size: 14px;
  color: #76828a
}

.page-title h1 {
  margin-bottom: 8px;
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
  color: #1f2d2a;
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

.view-toggle {
  display: flex;
  justify-content: center;
  gap: 22px;
  margin-bottom: 30px;
}

.view-btn {
  border: none;
  background: transparent;
  color: #6a7d76;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
}

.view-btn.active {
  color: #557067;
  font-weight: 700;
  text-decoration: underline;
  text-underline-offset: 4px;
}

@media (max-width: 1024px) {
  .results-layout {
    grid-template-columns: 1fr;
  }
}
</style>