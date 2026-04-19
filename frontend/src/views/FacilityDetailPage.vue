<template>
  <div class="detail-page">
    <Header />

    <div v-if="facility" class="detail-container">
      <div class="breadcrumb">
        <span class="breadcrumb-link" @click="goBack">← Back to results</span>
        <span class="breadcrumb-separator">|</span>
        <span class="breadcrumb-current">{{ facility.name }}</span>
      </div>

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
              <span class="recommend-badge">Recommended</span>
            </div>
            <p class="facility-address">📍 {{ facility.address }}</p>
            <div class="care-tag-wrapper">
              <span class="care-tag">{{ facility.careType }}</span>
            </div>
          </div>

          <div class="summary-cards">
            <div class="summary-card">
              <div class="summary-value availability-text">{{ facility.bedAvailability }}</div>
              <div class="summary-label">BED AVAILABILITY ESTIMATION</div>
            </div>
            <div class="summary-card">
              <div class="summary-value">{{ facility.totalBeds }}</div>
              <div class="summary-label">TOTAL BEDS</div>
            </div>
          </div>

          <div class="info-card">
            <h2 class="section-title">Aged Care Details</h2>
            <div class="detail-table">
              <div class="detail-row">
                <span class="detail-label">Physical Suburb</span>
                <span class="detail-value">{{ facility.suburb }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">State</span>
                <span class="detail-value">Victoria</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Postcode</span>
                <span class="detail-value">{{ facility.postcode }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Care Type</span>
                <span class="detail-value">{{ facility.careType }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Organisation Type</span>
                <span class="detail-value">{{ facility.organisationType }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Government Funding</span>
                <span class="detail-value">${{ facility.governmentFunding }}</span>
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

          <div class="sidebar-card provider-card">
            <h3 class="sidebar-title">About the Provider</h3>
            <div class="provider-top">
              <p class="provider-name">{{ facility.provider }}</p>
              <p class="provider-sub">{{ facility.providerType }}</p>
            </div>
            <div class="provider-info">
              <div class="provider-row">
                <span class="provider-label">ABS Remoteness</span>
                <span class="provider-value">{{ facility.remoteness }}</span>
              </div>
              <div class="provider-row">
                <span class="provider-label">Aged Care Planning Region (ACPR)</span>
                <span class="provider-value">{{ facility.acpr }}</span>
              </div>
            </div>
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

const goToMapSearch = () => {
  if (facility.value?.suburb) {
    router.push({
      path: '/find-bed',
      query: { ...route.query, suburb: facility.value.suburb }
    })
  } else {
    router.push({ path: '/find-bed', query: route.query })
  }
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
  padding: 18px 32px 0;
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
}

.breadcrumb-link {
  cursor: pointer;
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

.recommend-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 12px;
  border-radius: 999px;
  background: #e6f0e8;
  color: #7ea08a;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.facility-address {
  margin: 10px 0 10px;
  font-size: 14px;
  color: #87a098;
  text-align: left;
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
  display: flex;
  gap: 12px;
}

.summary-card {
  min-width: 114px;
  max-width: 100px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  padding: 14px 16px 12px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.summary-value {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.15;
  color: #22332e;
}

.availability-text {
  color: #4f7a62;
}

.summary-label {
  margin-top: 4px;
  font-size: 10px;
  line-height: 1.35;
  color: #7f8d87;
  text-transform: uppercase;
  text-align: center;
}

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

.info-card .section-title {
  padding-bottom: 14px;
  border-bottom: 1px solid #e4ddd3;
}

.detail-table {
  margin-top: 2px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  align-items: center;
  gap: 18px;
  padding: 14px 0;
  border-bottom: 1px solid #ebe4da;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 14px;
  color: #687a73;
  text-align: left;
}

.detail-value {
  font-size: 14px;
  color: #2b2b2b;
  font-weight: 600;
  text-align: right;
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

.provider-card {
  padding: 18px 18px 16px;
  text-align: left;
}

.provider-card .sidebar-title {
  padding-bottom: 14px;
  border-bottom: 1px solid #e4ddd3;
}

.provider-top {
  padding: 12px 0 14px;
  border-bottom: 1px solid #e4ddd3;
}

.provider-name {
  margin: 0 0 6px;
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: #22332e;
  line-height: 1.35;
}

.provider-sub {
  margin: 0;
  font-size: 13px;
  color: #6c8077;
  line-height: 1.35;
}

.provider-info {
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.provider-row {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 14px;
  align-items: start;
}

.provider-label {
  font-size: 13px;
  color: #6c8077;
  line-height: 1.4;
}

.provider-value {
  font-size: 13px;
  font-weight: 700;
  color: #202020;
  line-height: 1.4;
  text-align: right;
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

  .detail-row,
  .provider-row {
    grid-template-columns: 1fr;
  }

  .detail-value,
  .provider-value {
    text-align: left;
  }

  .summary-cards {
    flex-wrap: wrap;
  }

  .summary-card {
    flex: 1;
    min-width: 120px;
    max-width: 100%;
  }
}
</style>