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
        :selected-funding="selectedFunding"
        :distance="distance"
        :care-type-options="careTypeOptions"
        :funding-options="fundingOptions"
        :min-distance="minDistance"
        :max-distance="maxDistance"
        @update:selectedCareTypes="selectedCareTypes = $event"
        @update:selectedFunding="selectedFunding = $event"
        @update:distance="distance = $event"
        @reset="resetFilters"
      />

      <div class="results-main">
        <ResultsHeader
          :count="filteredFacilities.length"
          :sort-by="sortBy"
          @update:sortBy="sortBy = $event"
        />

        <ListSection
          v-if="activeView === 'list'"
          :facilities="filteredFacilities"
        />

        <MapSection
          v-else
          :facilities="filteredFacilities"
        />

        <PaginationBar />

        
      </div>
    </section>
    
    <FooterSection />
  
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import mockFacilities from '../mock_data/mockFacilities'

import Header from '../components/Header.vue'
import SearchBar from '../components/search/SearchBar.vue'
import FilterPanel from '../components/search/FilterPanel.vue'
import ResultsHeader from '../components/search/ResultsHeader.vue'
import ListSection from '../components/search/ListSection.vue'
import MapSection from '../components/MapSection.vue'
import PaginationBar from '../components/search/PaginationBar.vue'
import FooterSection from '../components/FooterSection.vue'

const searchQuery = ref('')
const activeView = ref('list')
const sortBy = ref('availability')

const careTypeOptions = [
  { value: 'Residential Care', label: 'Residential Aged Care', icon: '🏠' },
  { value: 'Home Care Package (HCP)', label: 'Home Care Package (HCP)', icon: '♡' },
  { value: 'CHSP - Community Support', label: 'CHSP - Community Support', icon: '○' },
  { value: 'Respite Care', label: 'Respite (Short Stay)', icon: '🛏️' },
  { value: 'Memory Care', label: 'Dementia / Memory Care', icon: '🧠' }
]

const fundingOptions = [
  { value: 'Government Funded (CHSP/HCP)', label: 'Government Funded (CHSP/HCP)' },
  { value: 'DVA (Veterans)', label: 'DVA (Veterans)' },
  { value: 'Private / Self-funded', label: 'Private / Self-funded' }
]

const selectedCareTypes = ref([])
const selectedFunding = ref([])

const distance = ref(10)
const minDistance = 1
const maxDistance = 20

function resetFilters() {
  selectedCareTypes.value = []
  selectedFunding.value = []
  distance.value = 10
}

function getWaitWeeks(wait) {
  const match = wait.match(/\d+/)
  return match ? Number(match[0]) : 999
}

function getAvailabilityRank(level) {
  if (level === 'High') return 3
  if (level === 'Medium') return 2
  if (level === 'Low') return 1
  return 0
}

const filteredFacilities = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()

  let result = mockFacilities.filter((f) => {
    const matchesQuery =
      !q ||
      f.service_name.toLowerCase().includes(q) ||
      f.physical_suburb.toLowerCase().includes(q) ||
      f.care_type.toLowerCase().includes(q)

    const matchesCareType =
      selectedCareTypes.value.length === 0 ||
      selectedCareTypes.value.includes(f.care_type)

    const matchesFunding =
      selectedFunding.value.length === 0 || true

    return matchesQuery && matchesCareType && matchesFunding
  })

  if (sortBy.value === 'wait') {
    result = [...result].sort(
      (a, b) => getWaitWeeks(a.estimated_wait_time) - getWaitWeeks(b.estimated_wait_time)
    )
  } else if (sortBy.value === 'name') {
    result = [...result].sort((a, b) =>
      a.service_name.localeCompare(b.service_name)
    )
  } else {
    result = [...result].sort(
      (a, b) => getAvailabilityRank(b.availability_level) - getAvailabilityRank(a.availability_level)
    )
  }

  return result
})
</script>

<style scoped>
.search-page {
  background: #f7f4ee;
  min-height: 100vh;
  padding: 24px 0 60px;
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