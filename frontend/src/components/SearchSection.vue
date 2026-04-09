<template>
  <div class="search-page">
    <div class="search-container">
      <section class="search-top">
        <label class="search-bar">
          <span class="search-icon">⌕</span>
          <input class="search-input "
            v-model="searchQuery"
            type="text"
            placeholder="Search by facility name, suburb, or care type..."
          />
        </label>

        <div class="view-toggle">
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
        </div>
      </section>

      <section class="results-layout">
      <!-- left filter panel -->
        <aside class="filters-panel">
          <div class="filters-header">
            <h2>Filters</h2>
            <button class="reset-btn" @click="resetFilters">Reset all</button>
          </div>

          <!-- CARE TYPE -->
          <div class="filter-section">
            <p class="filter-title">CARE TYPE</p>

            <label
              v-for="item in careTypeOptions"
              :key="item.value"
              class="filter-option"
              :class="{ selected: selectedCareTypes.includes(item.value) }"
            >
              <input
                v-model="selectedCareTypes"
                type="checkbox"
                :value="item.value"
              />
              <span class="custom-checkbox">
                <span v-if="selectedCareTypes.includes(item.value)">✓</span>
              </span>
              <span class="option-icon">{{ item.icon }}</span>
              <span class="option-text">{{ item.label }}</span>
            </label>
          </div>

          <hr class="filter-divider"/>

          <!-- DISTANCE -->
          <div class="filter-section">
            <p class="filter-title">DISTANCE FROM YOU</p>

            <div class="distance-top">
              <span>Within</span>
              <strong>{{ distance }} km</strong>
            </div>

            <div class="range-wrap">
              <input
                v-model="distance"
                class="distance-range"
                type="range"
                :min="minDistance"
                :max="maxDistance"
                :style="rangeStyle"
              />
            </div>
          </div>

          <hr class="filter-divider"/>

          <!-- FUNDING -->
          <div class="filter-section">
            <p class="filter-title">FUNDING TYPE ACCEPTED</p>

            <label
              v-for="item in fundingOptions"
              :key="item.value"
              class="filter-option funding-option"
              :class="{ selected: selectedFunding.includes(item.value) }"
            >
              <input
               v-model="selectedFunding"
                type="checkbox"
                :value="item.value"
              />
              <span class="custom-checkbox">
                <span v-if="selectedFunding.includes(item.value)">✓</span>
              </span>
              <span class="option-text funding-text">{{ item.label }}</span>
           </label>
          </div>
        </aside>

        <!-- right results -->
        <div class="results-main">
          <div class="results-header">
            <p class="results-count">
              Showing {{ filteredFacilities.length }} care facilities
            </p>

            <label class="sort-box">
              <span>Sort by:</span>
              <select v-model="sortBy">
                <option value="availability">Highest availability</option>
                <option value="wait">Shortest wait</option>
                <option value="name">A to Z</option>
              </select>
            </label>
          </div>

          <div v-if="activeView === 'list'" class="results-list">
            <article
              v-for="facility in filteredFacilities"
              :key="facility.id"
              class="facility-card"
            >
              <img
                :src="facility.image_url"
                :alt="facility.service_name"
                class="facility-image"
              />

              <div class="facility-body">
                <div class="facility-top-row">
                  <div>
                    <h3>{{ facility.service_name }}</h3>
                    <p class="facility-address">
                      📍 {{ facility.physical_address }}, {{ facility.physical_suburb }}
                      {{ facility.physical_state }} {{ facility.physical_post_code }}
                    </p>
                  </div>

                  <span class="recommended-badge">Recommended</span>
                </div>

                <div class="tag-row">
                  <span class="tag-chip">{{ facility.care_type }}</span>
                  <span class="tag-chip">{{ facility.provider_name }}</span>
                </div>

                <div class="metrics-row">
                  <div class="metric-block availability">
                    <div class="metric-value">{{ facility.availability_level }}</div>
                    <div class="metric-caption">BEDS AVAILABLE</div>
                  </div>

                <div class="metric-block wait-time">
                  <div class="metric-value">{{ facility.estimated_wait_time }}</div>
                  <div class="metric-caption">EST. WAIT</div>
                </div>
              </div>

              <div class="facility-footer">
                <p class="places-line">
                  Residential places: {{ facility.residential_places }} ·
                  Home care places: {{ facility.home_care_places }}
                </p>

                <button class="details-btn">View Details</button>
              </div>
              </div>
            </article>
          </div>

          <div v-else class="map-placeholder">
            Map placeholder
          </div>

          <div class="pagination">
            <button>‹</button>
            <button class="active-page">1</button>
            <button>2</button>
            <button>3</button>
            <button>›</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import mockFacilities from '../mock_data/mockFacilities'

const currentMode = ref('search')
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

const selectedCareTypes = ref(['Residential Care'])
const selectedFunding = ref([
  'Government Funded (CHSP/HCP)',
  'DVA (Veterans)'
])

const distance = ref(10)

const minDistance = 1
const maxDistance = 20

const rangeStyle = computed(() => {
  const percentage =
    ((distance.value - minDistance) / (maxDistance - minDistance)) * 100

  return {
    background: `linear-gradient(to right, #4f7d6f 0%, #4f7d6f ${percentage}%, #dbd8d4 ${percentage}%, #dbd8d4 100%)`
  }
})

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
  font-family: 'Inter', sans-serif;
}

.search-container {
  width: 100%;
  max-width: 1000px;     
  margin: 0 auto;         
  padding: 0 24px;       
}

.search-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  margin-bottom: 30px;
}

.search-bar {
  width: 100%;
  max-width: 750px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid #ddd8cf;
  
  border-radius: 10px;
  padding: 6px 16px;
}

.search-bar input::placeholder {
  color: #bec5c2; 
}

.search-icon {
  color: #7b8d87;
  font-size: 16px;
}

.search-bar input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #030303;
}

.view-toggle {
  display: flex;
  align-items: center;
  gap: 22px;
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

.results-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 26px;
  align-items: start;
}

.filters-panel {
  background: #ffffff;
  border: 1.5px solid #ddd5ca;
  border-radius: 8px;
  padding: 26px 26px 30px;
  width: 100%;
  box-sizing: border-box;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 26px;
}

.filters-header h2 {
  margin: 0;
  font-size: 24px;
  line-height: 1.1;
  font-weight: 800;
  color: #22332e;
  font-family: 'Inter', sans-serif;
}

.reset-btn {
  border: none;
  background: transparent;
  padding: 0;
  font-size: 14px;
  font-weight: 700;
  color: #5a8b72;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 18px;
}

.filter-title {
  margin: 0;
  font-size: 13px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: #a4afa9;
  font-family: 'Inter', sans-serif;
  text-align: left;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 700;
  color: #8a9691;
}

.filter-option {
  display: grid;
  grid-template-columns: 28px 24px 1fr;
  align-items: center;
  column-gap: 4px;
  height: 40px;
  padding: 0 15px;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.18s ease;
  box-sizing: border-box;
}

.funding-option {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: center;
  column-gap: 4px;
  min-height: 40px;
  padding: 0 16px;
}

.funding-text {
  font-size: 14px;
  line-height: 1.35;
  color: #40534d;
  font-family: 'Inter', sans-serif;
  white-space: normal;
  word-break: keep-all;
}

.filter-option input[type="checkbox"] {
  display: none;
}

.filter-option.selected {
  background: #edf5ef;
  border-color: #4f7d6f;
}

.filter-option input {
  display: none;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid #c5d1ca;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  font-weight: 900;
  flex-shrink: 0;
  box-sizing: border-box;
  background: white;
}

.filter-option.selected .custom-checkbox {
  background: #4f7d6f;
  border-color: #4f7d6f;
}
.option-icon {
  width: 22px;
  text-align: center;
  font-size: 19px;
  line-height: 1;
  flex-shrink: 0;
}

.option-text {
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
  color: #40534d;
  font-family: 'Inter', sans-serif;
  text-align: left;
}

.filter-option.selected .option-text {
  font-weight: 700;
  color: #2a4a40;
}

.results-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-count {
  margin: 0;
  color: #77857f;
  font-size: 15px;
}

.distance-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  margin-bottom: 0px;
}

.distance-top span {
  font-size: 14px;
  color: #5d6f69;
  font-family: 'Inter', sans-serif;
}

.distance-top strong {
  font-size: 14px;
  font-weight: 600;
  color: #22332e;
  font-family: 'Inter', sans-serif;
}

.range-wrap {
  padding-top: 2px;
}

.distance-range {
  width: 100%;
  appearance: none;
  background: transparent;
}

.distance-range {
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
  background: transparent;
}

.distance-range::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 999px;
  background: transparent;
}

.distance-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f8f8f6;
  border: 4px solid #4f7d6f;
  margin-top: -8px;
  cursor: pointer;
}

.distance-range::-moz-range-track {
  height: 8px;
  border-radius: 999px;
  background: transparent;
}

.distance-range::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f8f8f6;
  border: 4px solid #4f7d6f;
  cursor: pointer;
}

.sort-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Inter', sans-serif;
}

.sort-box label {
  font-size: 13px;
  color: #6b736f;
}

.sort-box span {
  color: #6b736f;
}

.sort-box select {
  padding: 6px 10px;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  background: white;
  font-size: 13px;
  color: #1f2d2a;
  cursor: pointer;
  appearance: auto;
}

.sort-box select:focus,
.sort-box select:active {
  background-color: white;
  color: #1f2d2a;
  outline: none;
  border-color: #bfc8c2;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.facility-card {
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 12px;
  overflow: hidden;
}

.facility-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 18px 20px;
}

.facility-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.facility-top-row h3 {
  margin: 0;
  font-size: 20px;
  font-family: 'Playfair Display', serif;
}

.facility-address {
  margin: 8px 0 0;
  color: #7b8d87;
  font-size: 14px;
}

.recommended-badge {
  background: #eaf4ec;
  color: #7aa284;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.tag-row {
  display: flex;
  gap: 8px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.tag-chip {
  background: #eef5ef;
  color: #678072;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-top: 18px;
  padding: 18px 0;
  border-top: 1px solid #ece7dd;
  border-bottom: 1px solid #ece7dd;
}

.metric-block {
  text-align: center;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  font-family: 'Playfair Display', serif;
}

.metric-caption {
  margin-top: 4px;
  font-size: 11px;
  color: #7b8d87;
}

.availability .metric-value {
  color: #4f7a62;
}

.wait-time .metric-value {
  color: #c98a3d;
}

.facility-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.places-line {
  margin: 0;
  color: #7b8d87;
  font-size: 14px;
}

.details-btn {
  border: none;
  background: #557067;
  color: white;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 600;
  cursor: pointer;
}

.map-placeholder {
  min-height: 400px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7b8d87;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.pagination button {
  border: 1px solid #ddd8cf;
  background: white;
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
}

.active-page {
  background: #557067 !important;
  color: white;
}

@media (max-width: 1024px) {
  .filters-panel {
    padding: 22px 20px 24px;
  }

  .filters-header h2 {
    font-size: 22px;
  }

  .filter-option {
    min-height: 52px;
    padding: 0 14px;
  }
  .results-layout {
    grid-template-columns: 1fr;
  }

  .results-header,
  .facility-footer,
  .facility-top-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>