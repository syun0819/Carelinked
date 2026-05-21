<template>
  <div class="home-page">
    <Header />

    <HeroSection />

    <section class="mode-switch-section">
      <div class="stats-wrapper">
        <div class="stats-grid">
          <div
            v-for="stat in highlightStats"
            :key="stat.label"
            class="stats-card scroll-animate"
          >
            <div class="stats-icon" aria-hidden="true">
              <svg v-if="stat.icon === 'home-care'" viewBox="0 0 24 24" fill="none">
                <path d="M7 20v-6.5A2.5 2.5 0 0 1 9.5 11H14" />
                <path d="M14 8.5A2.5 2.5 0 1 0 14 3.5a2.5 2.5 0 0 0 0 5Z" />
                <path d="M17 20v-5" />
                <path d="M14.5 17.5H19.5" />
              </svg>
              <svg v-else-if="stat.icon === 'residential'" viewBox="0 0 24 24" fill="none">
                <path d="M3.5 20.5h17" />
                <path d="M5.5 20.5v-9l6.5-4 6.5 4v9" />
                <path d="M9 20.5v-5h6v5" />
                <path d="M10 11.5h.01" />
                <path d="M14 11.5h.01" />
              </svg>
              <svg v-else-if="stat.icon === 'wait-time'" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="8.5" />
                <path d="M12 7.5v5l3.5 2" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none">
                <path d="M4 20.5h16" />
                <path d="M6.5 20.5v-11h11v11" />
                <path d="M9 6.5h6" />
                <path d="M12 3.5v6" />
                <path d="M9 12.5h.01" />
                <path d="M12 12.5h.01" />
                <path d="M15 12.5h.01" />
                <path d="M9 15.5h.01" />
                <path d="M12 15.5h.01" />
                <path d="M15 15.5h.01" />
              </svg>
            </div>
            <div class="stats-content">
              <div class="stats-number">{{ stat.value }}</div>
              <div class="stats-text">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <ExploreSection
      :user-location="userLocation"
      @request-location="requestLocation"
    />

    <HowItWorksSection />

    <FooterSection />
    <CompareBar />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from '../components/Header.vue'
import HeroSection from '../components/HeroSection.vue'
import ExploreSection from '../components/ExploreSection.vue'
import HowItWorksSection from '../components/HowItWorksSection.vue'
import FooterSection from '../components/FooterSection.vue'
import CompareBar from '../components/CompareBar.vue'

import { useLocationStore } from '../stores/locationStore'

const userLocation = ref(null)
const locationStore = useLocationStore()
const highlightStats = [
  { value: '275,000', label: 'Using home care in Australia', icon: 'home-care' },
  { value: '198,000', label: 'In residential care', icon: 'residential' },
  { value: '41 days', label: 'Median residential care wait', icon: 'wait-time' },
  { value: '2,617', label: 'Residential care services nationwide', icon: 'services' }
]

async function requestLocation() {
  await locationStore.requestUserLocation()
  if (locationStore.userLat != null && locationStore.userLng != null) {
    userLocation.value = {
      lat: locationStore.userLat,
      lng: locationStore.userLng
    }
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
  background: #f7f4ee;
  color: #1f2d2a;
  min-height: 100vh;
}

.mode-switch-section {
  position: relative;
  height: 0;
  z-index: 2;
}

@media (max-width: 640px) {
  .mode-switch-section {
    height: auto;
  }
}
.stats-wrapper {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  padding: 0 24px;
  transform: translateY(-50%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  width: min(100%, 1320px);
}

.stats-card {
  background: #ffffff;
  border: 1.5px solid #d8d1c8;
  border-radius: 12px;
  padding: 14px 18px;
  box-shadow: 0 10px 22px rgba(32, 43, 39, 0.08);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 14px;
  min-height: 80px;
}

.stats-icon {
  width: 36px;
  height: 36px;
  color: #4d7f70;
  flex-shrink: 0;
}

.stats-icon svg {
  width: 100%;
  height: 100%;
}

.stats-icon path,
.stats-icon circle {
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.stats-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  flex: 1;
}

.stats-number {
  font-size: 22px;
  font-weight: 700;
  color: #223432;
  line-height: 1.1;
  font-family: var(--font-display);
  width: 100%;
  text-align: left;
}

.stats-text {
  font-size: 12px;
  color: #5f7f79;
  line-height: 1.45;
  margin-top: 4px;
  font-family: var(--font-sans);
  width: 100%;
  text-align: left;
}

@media (max-width: 1024px) {
  .mode-switch-section {
    height: auto;
    background: linear-gradient(to bottom, #dfe8e3 55%, #f7f4ee 55%);
  }

  .stats-wrapper {
    transform: translateY(0);
    padding-top: 20px;
    padding-bottom: 0;
  }

  .stats-grid {
    align-items: stretch;
  }

  .stats-card {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 16px 10px;
    gap: 6px;
    min-height: 90px;
  }

  .stats-icon {
    width: 26px;
    height: 26px;
  }

  .stats-content {
    align-items: center;
  }

  .stats-number {
    font-size: 18px;
    text-align: center;
  }

  .stats-text {
    font-size: 11px;
    text-align: center;
  }
}

@media (max-width: 640px) {
  .mode-switch-section {
    background: #f7f4ee;
  }

  .stats-wrapper {
    padding: 16px 16px 24px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .stats-card {
    padding: 14px 16px;
    min-height: auto;
  }

  .stats-number {
    font-size: 20px;
  }

  .stats-text {
    font-size: 12px;
  }
}
</style>
