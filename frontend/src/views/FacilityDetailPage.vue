<template>
  <div class="detail-page">
    <Header />

    <div v-if="facility" class="detail-container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <button class="breadcrumb-link" @click="goHome">Home</button>
        <span class="breadcrumb-separator">&gt;</span>
        <button class="breadcrumb-link" @click="goToFindBed">Find a Bed</button>
        <span class="breadcrumb-separator">&gt;</span>
        <span class="breadcrumb-current">{{ facility.name }}</span>
      </nav>

      <div class="detail-layout">
        <div class="detail-main">
          <div class="detail-image-wrapper">
            <img
              :src="facility.image"
              :alt="facility.name"
              class="detail-image"
            />
          </div>

          <div class="facility-header">
            <div class="facility-title-row">
              <h1 class="facility-title">{{ facility.name }}</h1>
            </div>
            <p class="facility-address">
              <svg class="address-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
                <circle cx="12" cy="9" r="2.5" />
              </svg>
              <span>{{ facility.address }}</span>
            </p>
            <div class="care-tag-wrapper">
              <span class="care-tag">{{ facility.careType }}</span>
            </div>
          </div>

          <div class="summary-cards">
            <div class="summary-card">
              <div class="summary-value availability-text" :class="availabilityClass">
                {{ facility.bedAvailability }}
              </div>
              <div class="summary-label">BED AVAILABILITY ESTIMATION</div>
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
            <button class="action-btn" @click="copyAddress">Copy Address</button>
            <button class="action-btn" @click="printPage">Print This Page</button>
            <button class="action-btn" @click="goBack">Back to Search Results</button>
          </div>
        </aside>

        <div class="similar-section">
          <h2 class="section-title">Similar Facilities Nearby</h2>
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

function escapeHtml(str) {
  if (str == null) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

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
      <strong>${escapeHtml(facility.value.name)}</strong><br />
      ${escapeHtml(facility.value.address)}
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

.breadcrumb-separator {
  color: #b1bbb6;
}

.breadcrumb-current {
  color: #22332e;
  font-weight: 600;
}

.detail-layout {
  display: grid;
  grid-template-columns: minmax(0, 2.15fr) minmax(320px, 1fr);
  grid-template-rows: auto auto;
  gap: 24px;
  align-items: start;
}

.detail-main {
  display: flex;
  flex-direction: column;
  gap: 18px;
  grid-column: 1;
  grid-row: 1;
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
  grid-column: 2;
  grid-row: 1;
}

.similar-section {
  grid-column: 1 / -1;
  grid-row: 2;
  margin-top: 2px;
}

.detail-image-wrapper {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  border: 1px solid #e1dbd1;
}

.detail-image {
  width: 100%;
  height: 380px;
  object-fit: cover;
  display: block;
}

.facility-header {
  padding: 2px 2px 0;
}

.facility-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.facility-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 30px;
  line-height: 1.2;
  font-weight: 700;
  color: #22332e;
}

.facility-address {
  margin: 10px 0 10px;
  font-size: 14px;
  color: #87a098;
  text-align: left;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.5;
}

.address-icon {
  width: 17px;
  height: 17px;
  flex: 0 0 auto;
  margin-top: 2px;
  color: #6f9181;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.care-tag-wrapper {
  display: flex;
  justify-content: flex-start;
}

.care-tag {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 2px 10px;
  border-radius: 999px;
  background: #e6f0e8;
  color: #6f9181;
  font-size: 11px;
  font-weight: 600;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 4px;
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

.summary-value {
  font-size: 21px;
  font-weight: 700;
  line-height: 1.15;
  color: #22332e;
}

.availability-text {
  color: #4f7a62;
}

.availability-likely {
  color: #4f7a62;
}

.availability-potential {
  color: #c9a200;
}

.availability-constrained {
  color: #d9822b;
}

.availability-highly-constrained {
  color: #c53b2c;
}

.availability-none {
  color: #9e9e9e;
}

.availability-default {
  color: #4f6a63;
}

.summary-label {
  margin-top: 6px;
  font-size: 12px;
  line-height: 1.35;
  color: #7f8d87;
  text-transform: uppercase;
  text-align: center;
  letter-spacing: 0;
}

.info-card,
.sidebar-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 18px 18px 16px;
}

.info-card {
  margin-top: 2px;
}

.section-title,
.sidebar-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: #22332e;
}

.info-card .section-title {
  margin-bottom: 16px;
}

.detail-overview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-overview-top {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(220px, 1fr);
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
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 22px;
  padding-right: 22px;
}

.detail-funding-tile {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #f3f0ea;
  padding-top: 10px;
  padding-bottom: 10px;
}

.detail-tile-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-start;
  color: #8a9791;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.detail-tile-icon {
  width: 16px;
  height: 16px;
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
  gap: 20px;
  margin-top: 10px;
}

.detail-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

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
}

.detail-location-grid .detail-stat:last-child {
  padding-right: 16px;
}

.detail-stat-label {
  font-size: 13px;
  font-weight: 700;
  color: #7b8882;
  text-transform: uppercase;
}

.detail-stat-value,
.detail-meta-value {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.15;
  color: #22332e;
}

.detail-meta-value {
  margin-top: 14px;
  text-wrap: balance;
  text-align: left;
}

.detail-funding-value {
  margin-top: 10px;
  font-size: 22px;
  line-height: 1;
  font-weight: 800;
  color: #22332e;
}

.detail-funding-tile .detail-tile-heading {
  font-size: 20px;
  justify-content: center;
}

.detail-map {
  width: 100%;
  height: 220px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #ddd8cf;
  margin-bottom: 14px;
}

.map-placeholder {
  width: 100%;
  height: 220px;
  border-radius: 14px;
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
  height: 42px;
  border: none;
  border-radius: 8px;
  background: #688374;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: block;
  margin: 0 auto;
}

.action-btn {
  width: 100%;
  background: #fff;
  border: 1px solid #d8dcd7;
  color: #667871;
  border-radius: 8px;
  padding: 13px 16px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 12px;
}

.similar-section .section-title {
  font-size: 18px;
  margin-bottom: 14px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

@media (max-width: 1100px) {
  .detail-layout {
    display: flex;
    flex-direction: column;
  }

  .detail-main {
    order: 1;
    width: 100%;
  }

  .detail-sidebar {
    order: 2;
    width: 100%;
  }

  .similar-section {
    order: 3;
    width: 100%;
  }

  .similar-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .detail-container {
    padding: 80px 16px 16px;
  }

  .detail-image {
    height: 220px;
  }

  .facility-title {
    font-size: 22px;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .summary-card {
    min-height: 68px;
  }

  .detail-overview-top,
  .detail-overview-bottom,
  .detail-location-grid {
    grid-template-columns: 1fr;
  }

  .detail-overview-bottom {
    grid-template-columns: 1fr;
  }

  .detail-location-grid .detail-stat:not(:first-child) {
    align-items: flex-start;
    text-align: left;
  }

  .detail-location-grid .detail-stat:last-child {
    align-items: flex-start;
    text-align: left;
  }

  .detail-funding-value {
    font-size: 20px;
  }

  .detail-stat-value,
  .detail-meta-value {
    font-size: 16px;
  }
}
</style>
