<template>
  <div class="detail-page">
    <Header />

    <div v-if="facility" class="detail-container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <button class="breadcrumb-link" @click="goHome">Home</button>
        <span class="breadcrumb-separator">&gt;</span>
        <button class="breadcrumb-link" @click="goToFindBed">Find Care</button>
        <span class="breadcrumb-separator">&gt;</span>
        <span class="breadcrumb-current">{{ facility.name }}</span>
      </nav>

      <div class="detail-layout">
        <!-- Full-width image carousel -->
        <div class="detail-image-wrapper">
          <button class="carousel-btn prev" aria-label="Previous image">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 18l-6-6 6-6"/>
            </svg>
          </button>
          <img :src="facility.image" :alt="facility.name" class="detail-image" />
          <button class="carousel-btn next" aria-label="Next image">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </button>
        </div>

        <div class="detail-main">
          <!-- Nav + content -->
          <div class="main-below-image">
            <!-- Left navigation menu -->
            <nav class="detail-nav-menu" aria-label="Page sections">
              <button
                class="detail-nav-item"
                :class="{ active: activeSection === 'summary' }"
                @click="activeSection = 'summary'"
              >
                <svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5Z"/>
                  <path d="M9 21V12h6v9"/>
                </svg>
                <span class="nav-label">Summary</span>
                <svg class="nav-chevron" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
              <button
                class="detail-nav-item"
                :class="{ active: activeSection === 'quality' }"
                @click="activeSection = 'quality'"
              >
                <svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
                <span class="nav-label">Quality Ratings</span>
                <svg class="nav-chevron" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
              <button
                class="detail-nav-item"
                :class="{ active: activeSection === 'staffing' }"
                @click="activeSection = 'staffing'"
              >
                <svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <circle cx="9" cy="7" r="3"/>
                  <path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  <path d="M21 21v-2a4 4 0 0 0-3-3.87"/>
                </svg>
                <span class="nav-label">Staffing &amp; Compliance</span>
                <svg class="nav-chevron" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
              <button
                class="detail-nav-item"
                :class="{ active: activeSection === 'resident' }"
                @click="activeSection = 'resident'"
              >
                <svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78Z"/>
                </svg>
                <span class="nav-label">Resident Experience</span>
                <svg class="nav-chevron" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            </nav>

            <!-- Right content area -->
            <div class="detail-content">
              <div class="facility-header">
                <h1 class="facility-title">{{ facility.name }}</h1>
                <p class="facility-address">
                  <svg class="address-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
                    <circle cx="12" cy="9" r="2.5" />
                  </svg>
                  <span>{{ facility.address }}</span>
                </p>
                <div class="tags-rating-row">
                  <span class="care-tag">{{ facility.careType }}</span>
                  <div v-if="starDisplay" class="star-rating">
                    <span
                      v-for="i in starDisplay.full"
                      :key="'f' + i"
                      class="star filled"
                    >★</span>
                    <span
                      v-for="i in starDisplay.empty"
                      :key="'e' + i"
                      class="star empty"
                    >★</span>
                    <span class="rating-value">{{ starDisplay.value }}</span>
                  </div>
                </div>
              </div>

              <!-- Summary section -->
              <template v-if="activeSection === 'summary'">
                <div class="summary-cards">
                  <div class="summary-card">
                    <div class="summary-value availability-text" :class="availabilityClass">
                      {{ facility.bedAvailability }}
                    </div>
                    <div class="summary-label">BED AVAILABILITY ESTIMATION</div>
                  </div>
                  <div class="summary-card">
                    <div class="summary-value wait-text">
                      {{ facility.estimatedWait || 'Unknown' }}
                    </div>
                    <div class="summary-label">ESTIMATED WAIT</div>
                  </div>
                  <div class="summary-card">
                    <div class="summary-value">{{ facility.totalBeds }}</div>
                    <div class="summary-label">TOTAL BEDS</div>
                  </div>
                </div>

                <div class="info-card">
                  <h2 class="section-title">Aged Care Details</h2>
                  <div class="detail-overview">
                    <div class="detail-overview-top">
                      <section class="detail-tile detail-location-tile">
                        <div class="detail-tile-heading">
                          <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
                            <circle cx="12" cy="9" r="2.5" />
                          </svg>
                          <span>Location</span>
                        </div>
                        <div class="detail-location-grid">
                          <div class="detail-stat">
                            <span class="detail-stat-label">Suburbs</span>
                            <span class="detail-stat-value">{{ facility.suburb || 'N/A' }}</span>
                          </div>
                          <div class="detail-stat">
                            <span class="detail-stat-label">State</span>
                            <span class="detail-stat-value">{{ stateAbbreviation }}</span>
                          </div>
                          <div class="detail-stat">
                            <span class="detail-stat-label">Postcode</span>
                            <span class="detail-stat-value">{{ facility.postcode || 'N/A' }}</span>
                          </div>
                        </div>
                      </section>

                      <section class="detail-tile detail-funding-tile">
                        <div class="detail-tile-heading">
                          <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <rect x="3.5" y="6.5" width="17" height="11" rx="2.5" />
                            <circle cx="12" cy="12" r="2.2" />
                          </svg>
                          <span>Gov. Funding</span>
                        </div>
                        <div class="detail-funding-value">{{ formattedFunding }}</div>
                      </section>
                    </div>

                    <div class="detail-overview-bottom">
                      <section class="detail-tile detail-meta-tile">
                        <div class="detail-tile-heading">
                          <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 21s-6-3.8-8-8.6A5.2 5.2 0 0 1 12 5a5.2 5.2 0 0 1 8 7.4C18 17.2 12 21 12 21Z" />
                            <path d="M9.5 12.5 11.2 14 14.8 10" />
                          </svg>
                          <span>Care Type</span>
                        </div>
                        <div class="detail-meta-value">{{ facility.careType || 'N/A' }}</div>
                      </section>

                      <section class="detail-tile detail-meta-tile">
                        <div class="detail-tile-heading">
                          <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M6 20V8.5h12V20" />
                            <path d="M4 20h16" />
                            <path d="M9 8.5V5h6v3.5" />
                            <path d="M9 12h.01M15 12h.01M9 15.5h.01M15 15.5h.01" />
                          </svg>
                          <span>Organisation</span>
                        </div>
                        <div class="detail-meta-value">{{ facility.organisationType || 'N/A' }}</div>
                      </section>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Quality Ratings section -->
              <template v-else-if="activeSection === 'quality'">
                <div class="info-card">
                  <div class="quality-header">
                    <h2 class="section-title">Quality Ratings</h2>
                    <div class="quality-overall">
                      <span class="star filled">★</span>
                      <span class="star filled">★</span>
                      <span class="star filled">★</span>
                      <span class="star empty">★</span>
                      <span class="star empty">★</span>
                      <span class="rating-value">3.0</span>
                      <span class="overall-badge">OVERALL</span>
                    </div>
                  </div>
                  <div class="quality-grid">
                    <div class="quality-item">
                      <span class="quality-label">Resident Experience</span>
                      <div class="quality-stars">
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star empty">★</span>
                        <span class="star empty">★</span>
                        <span class="quality-num">3.0</span>
                      </div>
                    </div>
                    <div class="quality-item">
                      <span class="quality-label">Staffing</span>
                      <div class="quality-stars">
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star empty">★</span>
                        <span class="star empty">★</span>
                        <span class="quality-num">3.0</span>
                      </div>
                    </div>
                    <div class="quality-item">
                      <span class="quality-label">Compliance</span>
                      <div class="quality-stars">
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star empty">★</span>
                        <span class="star empty">★</span>
                        <span class="quality-num">3.0</span>
                      </div>
                    </div>
                    <div class="quality-item">
                      <span class="quality-label">Quality Measures</span>
                      <div class="quality-stars">
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star filled">★</span>
                        <span class="star empty">★</span>
                        <span class="star empty">★</span>
                        <span class="quality-num">3.0</span>
                      </div>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Staffing & Compliance placeholder -->
              <template v-else-if="activeSection === 'staffing'">
                <div class="info-card section-placeholder">
                  <h2 class="section-title">Staffing &amp; Compliance</h2>
                  <p class="placeholder-text">Data coming soon.</p>
                </div>
              </template>

              <!-- Resident Experience placeholder -->
              <template v-else-if="activeSection === 'resident'">
                <div class="info-card section-placeholder">
                  <h2 class="section-title">Resident Experience</h2>
                  <p class="placeholder-text">Data coming soon.</p>
                </div>
              </template>
            </div>
          </div>
        </div>

        <aside class="detail-sidebar">
          <div class="sidebar-card">
            <h3 class="sidebar-title">Location</h3>
            <div v-if="hasCoordinates" ref="mapEl" class="detail-map"></div>
            <div v-else class="map-placeholder">Location unavailable</div>
            <button class="sidebar-btn" @click="goToMapSearch">Find with Map</button>
          </div>

          <div class="sidebar-card">
            <h3 class="sidebar-title">What You Can Do</h3>
            <button class="action-btn" @click="addToCompare">
              <svg class="action-btn-icon" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="3" y="3" width="7" height="7" rx="1"/>
                <rect x="14" y="3" width="7" height="7" rx="1"/>
                <rect x="3" y="14" width="7" height="7" rx="1"/>
                <rect x="14" y="14" width="7" height="7" rx="1"/>
              </svg>
              Add to Compare
            </button>
            <button class="action-btn" @click="copyAddress">
              <svg class="action-btn-icon" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="9" y="9" width="13" height="13" rx="2"/>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
              </svg>
              Copy Address
            </button>
            <button class="action-btn" @click="printPage">
              <svg class="action-btn-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M6 9V2h12v7"/>
                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                <rect x="6" y="14" width="12" height="8"/>
              </svg>
              Print This Page
            </button>
            <button class="action-btn" @click="goBack">
              <svg class="action-btn-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M19 12H5"/>
                <path d="M12 19l-7-7 7-7"/>
              </svg>
              Back to Search Results
            </button>
          </div>
        </aside>

        <div class="similar-section">
          <h2 class="similar-title">Similar Facilities Nearby</h2>
          <div class="similar-grid">
            <FacilityCard
              v-for="item in similarFacilities"
              :key="item.id"
              :facility="item"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-else class="detail-container">
      <p>Facility not found.</p>
    </div>

    <FooterSection />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, onBeforeUnmount, ref, computed, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import FacilityCard from '../components/FacilityCard.vue'

import { getFacilityDetail, getSimilarFacilities } from '../services/facilitiesApi'
import { mapFacilityCard, mapFacilityDetail } from '../utils/facilityMappers'

const route = useRoute()
const router = useRouter()

const facility = ref(null)
const similarFacilities = ref([])
const loading = ref(false)
const error = ref('')
const activeSection = ref('summary')

const mapEl = ref(null)
let map = null
let marker = null

const hasCoordinates = computed(() => {
  return (
    facility.value &&
    facility.value.latitude != null &&
    facility.value.longitude != null
  )
})

const availabilityClass = computed(() => {
  const value = facility.value?.bedAvailability
  if (value === 'Likely Available') return 'availability-likely'
  if (value === 'Potentially Available') return 'availability-potential'
  if (value === 'Constrained by Market' || value === 'Constrained by Size') return 'availability-constrained'
  if (value === 'Highly Constrained') return 'availability-highly-constrained'
  if (value === 'Does Not Provide This Service') return 'availability-none'
  return 'availability-default'
})

const stateAbbreviation = computed(() => {
  const state = facility.value?.state?.trim()
  if (!state) return 'N/A'

  const stateMap = {
    'New South Wales': 'NSW',
    Victoria: 'VIC',
    Queensland: 'QLD',
    'South Australia': 'SA',
    'Western Australia': 'WA',
    Tasmania: 'TAS',
    'Northern Territory': 'NT',
    'Australian Capital Territory': 'ACT'
  }

  return stateMap[state] || state.toUpperCase()
})

const formattedFunding = computed(() => {
  const funding = facility.value?.governmentFunding
  if (funding == null || funding === '') return 'N/A'

  const numericFunding = Number(funding)
  if (Number.isNaN(numericFunding)) return String(funding)

  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
    maximumFractionDigits: 0
  }).format(numericFunding)
})

const starDisplay = computed(() => {
  if (!facility.value) return null
  const rating = facility.value.rating
  const num = rating ? parseFloat(rating) : 3.0
  const full = Math.round(isNaN(num) ? 3 : num)
  return { full: Math.max(0, Math.min(5, full)), empty: 5 - Math.max(0, Math.min(5, full)), value: (isNaN(num) ? 3 : num).toFixed(1) }
})

function initMap() {
  if (!hasCoordinates.value || !mapEl.value) return

  if (map) {
    map.remove()
    map = null
  }

  map = L.map(mapEl.value, {
    zoomControl: true
  }).setView([facility.value.latitude, facility.value.longitude], 15)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  marker = L.marker([facility.value.latitude, facility.value.longitude]).addTo(map)

  marker.bindPopup(`
    <div>
      <strong>${facility.value.name}</strong><br />
      ${facility.value.address || ''}
    </div>
  `)

  setTimeout(() => {
    if (map) {
      map.invalidateSize()
    }
  }, 100)
}

async function fetchFacilityDetail() {
  loading.value = true
  error.value = ''

  try {
    const id = route.params.id
    const detailData = await getFacilityDetail(id)
    facility.value = mapFacilityDetail(detailData)

    const similarData = await getSimilarFacilities(id, 2)
    similarFacilities.value = (similarData.results || []).map(mapFacilityCard)

    await nextTick()
    initMap()
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load facility details.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFacilityDetail()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})

const goBack = () => {
  const hasSearchState = Object.keys(route.query).length > 0
  if (hasSearchState) {
    router.push({ path: '/find-bed', query: route.query })
  } else {
    router.back()
  }
}

const goHome = () => {
  router.push('/')
}

const goToFindBed = () => {
  router.push({ path: '/find-bed', query: route.query })
}

const goToMapSearch = () => {
  const query = {
    ...route.query,
    view: 'map',
    page: undefined
  }

  if (facility.value?.suburb) {
    query.search = facility.value.suburb
    query.searchType = 'suburb'
  }

  if (hasCoordinates.value) {
    query.focusLat = String(facility.value.latitude)
    query.focusLng = String(facility.value.longitude)
  }

  router.push({ path: '/find-bed', query })
}

const printPage = () => {
  window.print()
}

const copyAddress = async () => {
  if (facility.value?.address) {
    await navigator.clipboard.writeText(facility.value.address)
    alert('Address copied')
  }
}

const addToCompare = () => {
  alert('Add to Compare — coming soon')
}
</script>

<style scoped>
.detail-page {
  background: #f7f4ee;
  min-height: 100vh;
  padding: 0;
  color: #22332e;
  overflow-x: hidden;
}

.detail-container {
  max-width: 1360px;
  margin: 0 auto;
  padding: 96px 32px 0;
  width: 100%;
  box-sizing: border-box;
}

/* ── Breadcrumb ── */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #98a39d;
  margin: 18px 0 18px;
  flex-wrap: wrap;
}

.breadcrumb-link {
  border: none;
  background: transparent;
  padding: 0;
  color: #6d7f79;
  font: inherit;
  cursor: pointer;
}

.breadcrumb-link:hover {
  color: #2f5d50;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.breadcrumb-separator { color: #b1bbb6; }
.breadcrumb-current { color: #22332e; font-weight: 600; }

/* ── Layout grid ── */
.detail-layout {
  display: grid;
  grid-template-columns: minmax(0, 2.15fr) minmax(300px, 1fr);
  grid-template-rows: auto auto auto;
  gap: 24px;
  align-items: start;
}

/* Image spans full width (row 1) */
.detail-image-wrapper {
  grid-column: 1 / -1;
  grid-row: 1;
}

.detail-main {
  display: flex;
  flex-direction: column;
  gap: 0;
  grid-column: 1;
  grid-row: 2;
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
  grid-column: 2;
  grid-row: 2;
}

.similar-section {
  grid-column: 1 / -1;
  grid-row: 3;
  margin-top: 0;
}

/* ── Image carousel ── */
.detail-image-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #e8e2d8;
  border: 1px solid #e1dbd1;
  grid-column: 1 / -1;
  grid-row: 1;
}

.detail-image {
  width: 100%;
  height: 380px;
  object-fit: cover;
  display: block;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.88);
  color: #22332e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 1px 6px rgba(0,0,0,0.18);
  transition: background 0.15s;
}

.carousel-btn:hover {
  background: #fff;
}

.carousel-btn svg {
  width: 18px;
  height: 18px;
}

.carousel-btn.prev { left: 14px; }
.carousel-btn.next { right: 14px; }

/* ── Below image: nav + content ── */
.main-below-image {
  display: grid;
  grid-template-columns: 200px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
  margin-top: 18px;
}

/* ── Left nav menu ── */
.detail-nav-menu {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 6px;
  position: sticky;
  top: 100px;
}

.detail-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 11px 12px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #667871;
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
  width: 100%;
}

.detail-nav-item:hover {
  background: #f3f0ea;
}

.detail-nav-item.active {
  background: #3d6b59;
  color: #fff;
  font-weight: 600;
}

.nav-label {
  flex: 1;
  text-align: left;
}

.nav-icon {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.nav-chevron {
  width: 14px;
  height: 14px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.55;
}

.detail-nav-item.active .nav-chevron {
  opacity: 0.8;
}

/* ── Right content area ── */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* ── Facility header ── */
.facility-header { padding: 2px 2px 0; }

.facility-title {
  margin: 0 0 8px;
  font-family: var(--font-display);
  font-size: 26px;
  line-height: 1.2;
  font-weight: 700;
  color: #22332e;
}

.facility-address {
  margin: 0 0 10px;
  font-size: 14px;
  color: #c07a40;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  line-height: 1.5;
}

.address-icon {
  width: 16px;
  height: 16px;
  flex: 0 0 auto;
  margin-top: 2px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.tags-rating-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.care-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 12px;
  border-radius: 999px;
  background: #e6f0e8;
  color: #4f7a62;
  font-size: 12px;
  font-weight: 600;
}

.star-rating {
  display: flex;
  align-items: center;
  gap: 1px;
}

.star {
  font-size: 16px;
  line-height: 1;
}

.star.filled { color: #e8a023; }
.star.empty  { color: #d8d0c4; }

.rating-value {
  margin-left: 5px;
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

/* ── Summary cards — 3 columns ── */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.summary-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  min-height: 72px;
  padding: 16px 18px 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.wait-text {
  font-size: 19px;
  font-weight: 700;
  color: #22332e;
}

.summary-value {
  font-size: 19px;
  font-weight: 700;
  line-height: 1.15;
  color: #22332e;
}

.availability-text  { color: #4f7a62; }
.availability-likely { color: #4f7a62; }
.availability-potential { color: #c9a200; }
.availability-constrained { color: #d9822b; }
.availability-highly-constrained { color: #c53b2c; }
.availability-none { color: #9e9e9e; }
.availability-default { color: #4f6a63; }

.summary-label {
  margin-top: 6px;
  font-size: 11px;
  line-height: 1.35;
  color: #7f8d87;
  text-transform: uppercase;
  text-align: center;
  letter-spacing: 0.02em;
}

/* ── Info card ── */
.info-card,
.sidebar-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 18px 18px 16px;
}

.section-title,
.sidebar-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: #22332e;
}

.info-card .section-title { margin-bottom: 16px; }

/* ── Detail overview tiles ── */
.detail-overview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-overview-top {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(180px, 1fr);
  gap: 12px;
}

.detail-overview-bottom {
  display: grid;
  grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr);
  gap: 12px;
}

.detail-tile {
  border: 1px solid #e3ddd3;
  border-radius: 12px;
  background: #fff;
  padding: 12px 16px;
}

.detail-location-tile {
  background: #f3f0ea;
  padding: 10px 22px;
}

.detail-funding-tile {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #f3f0ea;
  padding: 10px;
}

.detail-tile-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8a9791;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.detail-tile-icon {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.detail-location-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 10px;
}

.detail-stat { display: flex; flex-direction: column; gap: 4px; }

.detail-location-grid .detail-stat:first-child {
  align-items: flex-start;
  text-align: left;
  padding-left: 12px;
}

.detail-location-grid .detail-stat:not(:first-child) {
  align-items: flex-end;
  text-align: right;
}

.detail-location-grid .detail-stat:last-child {
  align-items: center;
  text-align: center;
  padding-right: 16px;
}

.detail-stat-label {
  font-size: 12px;
  font-weight: 700;
  color: #7b8882;
  text-transform: uppercase;
}

.detail-stat-value,
.detail-meta-value {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.15;
  color: #22332e;
}

.detail-meta-value {
  margin-top: 12px;
  text-wrap: balance;
  text-align: left;
}

.detail-funding-value {
  margin-top: 10px;
  font-size: 20px;
  line-height: 1;
  font-weight: 800;
  color: #22332e;
}

.detail-funding-tile .detail-tile-heading {
  font-size: 13px;
  justify-content: center;
}

/* ── Map ── */
.detail-map {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #ddd8cf;
  margin-bottom: 14px;
}

.map-placeholder {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  border: 1px solid #ddd8cf;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f8f8;
  color: #7a7a7a;
  margin-bottom: 14px;
}

.sidebar-btn {
  width: 138px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: #688374;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  transition: background 0.15s;
}

.sidebar-btn:hover {
  background: #3d6b59;
}

/* ── Action buttons ── */
.action-btn {
  width: 100%;
  background: #fff;
  border: 1px solid #d8dcd7;
  color: #667871;
  border-radius: 8px;
  padding: 13px 16px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background 0.15s, border-color 0.15s;
}

.action-btn:hover {
  background: #f3f0ea;
  border-color: #c4c9c5;
}

.action-btn-icon {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* ── Similar section ── */
.similar-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: #22332e;
  margin: 0 0 16px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

/* ── Responsive ── */
@media (max-width: 1100px) {
  .detail-layout {
    display: flex;
    flex-direction: column;
  }

  .detail-image-wrapper { order: 1; width: 100%; }
  .detail-main { order: 2; width: 100%; }
  .detail-sidebar { order: 3; width: 100%; }
  .similar-section { order: 4; width: 100%; }
  .similar-grid { grid-template-columns: 1fr; }
}

/* ── Quality Ratings ── */
.quality-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.quality-overall {
  display: flex;
  align-items: center;
  gap: 3px;
}

.quality-overall .rating-value {
  margin-left: 6px;
  font-size: 16px;
  font-weight: 700;
  color: #22332e;
}

.overall-badge {
  margin-left: 6px;
  font-size: 11px;
  font-weight: 700;
  color: #7a8a84;
  letter-spacing: 0.06em;
  background: #f0ece4;
  padding: 2px 8px;
  border-radius: 4px;
}

.quality-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.quality-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f5ef;
  border: 1px solid #e8e2d8;
  border-radius: 10px;
  padding: 12px 16px;
  gap: 10px;
}

.quality-label {
  font-size: 14px;
  font-weight: 600;
  color: #3a4e47;
}

.quality-stars {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}

.quality-num {
  margin-left: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

/* ── Placeholder sections ── */
.section-placeholder { min-height: 120px; }

.placeholder-text {
  margin-top: 16px;
  font-size: 14px;
  color: #9aada6;
}

@media (max-width: 768px) {
  .detail-container { padding: 80px 16px 16px; }
  .detail-image { height: 220px; }
  .facility-title { font-size: 20px; }

  .main-below-image {
    grid-template-columns: 1fr;
  }

  .detail-nav-menu {
    flex-direction: row;
    flex-wrap: wrap;
    position: static;
  }

  .detail-nav-item {
    flex: 1 1 auto;
    justify-content: center;
    font-size: 12px;
    padding: 8px 8px;
  }

  .nav-chevron { display: none; }

  .summary-cards { grid-template-columns: 1fr; }
  .summary-card { min-height: 68px; }

  .detail-overview-top,
  .detail-overview-bottom,
  .detail-location-grid {
    grid-template-columns: 1fr;
  }

  .detail-location-grid .detail-stat:not(:first-child),
  .detail-location-grid .detail-stat:last-child {
    align-items: flex-start;
    text-align: left;
  }

  .detail-funding-value { font-size: 18px; }

  .detail-stat-value,
  .detail-meta-value { font-size: 15px; }

  .quality-grid { grid-template-columns: 1fr; }

  .quality-item { flex-direction: column; align-items: flex-start; gap: 6px; }
}
</style>
