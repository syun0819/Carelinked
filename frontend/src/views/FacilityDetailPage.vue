<template>
  <div class="detail-page">
    <Header/>

    <div v-if="facility" class="detail-container">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <span class="breadcrumb-link" @click="goHome">Home</span>
        <span class="breadcrumb-separator">></span>
        <span class="breadcrumb-current">{{ facility.name }}</span>
      </div>

      <div class="detail-layout">
        <!-- Left -->
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

            <p class="facility-address">{{ facility.address }}</p>
            <span class="care-tag">{{ facility.careType }}</span>
          </div>

          <div class="summary-cards">
            <div class="summary-card">
              <div class="summary-value">{{ facility.bedAvailability }}</div>
              <div class="summary-label">ESTIMATED BEDS AVAILABLE</div>
            </div>

            <div class="summary-card">
              <div class="summary-value">{{ facility.totalBeds }}</div>
              <div class="summary-label">TOTAL BEDS</div>
            </div>
          </div>

          <div class="info-card">
            <h2 class="section-title">Aged Care Details</h2>

            <div class="info-row">
              <span>Physical Suburb</span>
              <span>{{ facility.suburb }}</span>
            </div>
            <div class="info-row">
              <span>State</span>
              <span>{{ facility.state }}</span>
            </div>
            <div class="info-row">
              <span>Postcode</span>
              <span>{{ facility.postcode }}</span>
            </div>
            <div class="info-row">
              <span>Care Type</span>
              <span>{{ facility.careType }}</span>
            </div>
            <div class="info-row">
              <span>Organisation Type</span>
              <span>{{ facility.organisationType }}</span>
            </div>
            <div class="info-row">
              <span>Australian Government Funding</span>
              <span>{{ facility.funding }}</span>
            </div>
          </div>

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

        <!-- Right -->
        <aside class="detail-sidebar">
          <div class="sidebar-card">
            <h3 class="sidebar-title">Location</h3>
            <div class="map-placeholder">Map</div>
            <button class="sidebar-btn">Find with Map</button>
          </div>

          <div class="sidebar-card">
            <h3 class="sidebar-title">About the Provider</h3>
            <p class="provider-name">{{ facility.provider }}</p>
            <p class="provider-sub">{{ facility.providerType }}</p>

            <div class="provider-meta">
              <div class="info-row">
                <span>ABS Remoteness</span>
                <span>{{ facility.remoteness }}</span>
              </div>
              <div class="info-row">
                <span>Aged Care Planning Region (ACPR)</span>
                <span>{{ facility.acpr }}</span>
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
      </div>
    </div>

    <div v-else class="detail-container">
      <p>Facility not found.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FacilityCard from '../components/FacilityCard.vue'
import mockFacilities from '../mock_data/mockFacilities.js'

const route = useRoute()
const router = useRouter()

const facility = computed(() => {
  const routeId = String(route.params.id)
  return mockFacilities.find(item => String(item.id) === routeId)
})

const similarFacilities = computed(() => {
  if (!facility.value) return []
  return mockFacilities
    .filter(item => String(item.id) !== String(route.params.id))
    .slice(0, 2)
})

const goBack = () => {
  router.back()
}

const goHome = () => {
  router.push('/')
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
  padding: 0px 0 60px;
}

.detail-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.breadcrumb {
  font-size: 14px;
  color: #7d857f;
  margin-bottom: 20px;
}

.breadcrumb-link {
  cursor: pointer;
}

.breadcrumb-separator {
  margin: 0 8px;
}

.breadcrumb-current {
  color: #23312f;
  font-weight: 600;
}

.detail-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.detail-main,
.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-image-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.detail-image {
  width: 100%;
  height: 420px;
  object-fit: cover;
  display: block;
}

.facility-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.facility-title {
  font-size: 44px;
  margin: 0;
  color: #23312f;
  font-family: Georgia, serif;
}

.recommend-badge,
.care-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  background: #e6f1e8;
  color: #5f8a6e;
}

.facility-address {
  color: #70807a;
  margin: 12px 0;
}

.summary-cards {
  display: flex;
  gap: 16px;
}

.summary-card,
.info-card,
.sidebar-card {
  background: white;
  border: 1px solid #e5ded3;
  border-radius: 12px;
  padding: 20px;
}

.summary-card {
  min-width: 180px;
  text-align: center;
}

.summary-value {
  font-size: 28px;
  font-weight: 700;
  color: #23312f;
}

.summary-label {
  font-size: 12px;
  color: #7c827c;
  margin-top: 8px;
}

.section-title,
.sidebar-title {
  margin: 0 0 16px;
  font-family: Georgia, serif;
  color: #23312f;
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-top: 1px solid #eee7dc;
}

.info-row:first-of-type {
  border-top: none;
}

.map-placeholder {
  height: 220px;
  border-radius: 10px;
  background: #e8ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6f7a76;
  margin-bottom: 16px;
}

.sidebar-btn,
.action-btn {
  width: 100%;
  border: none;
  border-radius: 10px;
  padding: 14px 16px;
  cursor: pointer;
  font-size: 14px;
}

.sidebar-btn {
  background: #5d7f72;
  color: white;
}

.action-btn {
  background: white;
  border: 1px solid #d8dcd7;
  color: #5d6f68;
  margin-top: 12px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.provider-name {
  font-weight: 700;
  color: #23312f;
  margin: 0 0 8px;
}

.provider-sub {
  color: #6e7672;
  margin: 0 0 16px;
}

@media (max-width: 1024px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }

  .similar-grid {
    grid-template-columns: 1fr;
  }

  .detail-image {
    height: 300px;
  }
}
</style>