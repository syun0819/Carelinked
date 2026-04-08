<template>
  <div class="home-page">
    <Header />

    <HeroSection />

    <section class="mode-switch-section">
      <div class="stats-card">
        <div class="stats-icon">🏢</div>
        <div class="stats-content">
          <div class="stats-number">400+</div>
          <div class="stats-text">Facilities across Victoria</div>
        </div>
      </div>

      <div class="mode-switch">
        <button
          :class="{ active: currentMode === 'explore' }"
          @click="currentMode = 'explore'"
        >
          <span class="icon">⌖</span>
          <span>Explore</span>
        </button>

        <button
          :class="{ active: currentMode === 'search' }"
          @click="currentMode = 'search'"
        >
          <span class="icon">⌕</span>
          <span>Search</span>
        </button>
      </div>
    </section>

    <ExploreSection
      v-if="currentMode === 'explore'"
      :facilities="mockFacilities"
    />

    <SearchSection
      v-else
      :facilities="mockFacilities"
    />

    <section class="wait-time-section">
      <h2>Wait Time Estimator</h2>
      <div class="wait-time-box">Estimator form goes here</div>
    </section>

    <section class="how-it-works-section">
      <h2>How It Works</h2>
      <div class="how-cards">
        <div class="how-card">Search</div>
        <div class="how-card">Compare</div>
        <div class="how-card">Connect</div>
      </div>
    </section>

    <footer class="footer">
      CareLink Footer
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from '../components/Header.vue'
import HeroSection from '../components/HeroSection.vue'
import ExploreSection from '../components/ExploreSection.vue'
import SearchSection from '../components/SearchSection.vue'
import mockFacilities from '../mock_data/mockFacilities'

const currentMode = ref('explore')
</script>

<style scoped>
.home-page {
  width: 100%;
  background: #f7f4ee;
  color: #1f2d2a;
  min-height: 100vh;
  font-family: 'Playfair Display', sans-serif;
}

.mode-switch-section {
  position: relative;
  z-index: 10;
  margin-top: -35px;
  padding: 0 24px 20px;
  background:transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}

.stats-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 6px;
  padding: 2px 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}

.stats-icon {
  font-size: 22px;
  line-height: 1;
}

.stats-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stats-number {
  font-size: 18px;
  font-weight: 700;
  color: #1f2d2a;
  font-family: 'Inter', sans-serif;
}

.stats-text {
  font-size: 12px;
  color: #61706a;
  font-family: 'Inter', sans-serif;
}

.mode-switch {
  display: flex;
  align-items: center;
  gap: 2px;
  background: white;
  border-radius: 999px;
  padding: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.mode-switch button {
  border: none;
  background: transparent;
  color: #557067;
  border-radius: 999px;
  padding: 6px 22px;
  min-width: 128px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
}

.mode-switch button.active {
  background: #5d8b72;
  color: white;
  border-color: #5d8b72;
}

.mode-switch button .icon {
  font-size: 15px;
  line-height: 1;
}

.mode-switch button:not(.active):hover {
  background: #f3f4f2;
}

.results-section {
  padding: 20px 80px 60px;
}

.results-toolbar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.results-toolbar input {
  width: 100%;
  max-width: 700px;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.results-content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  align-items: start;
}

.filter-panel {
  background: white;
  border-radius: 12px;
  padding: 16px;
}

.results-main {
  min-height: 500px;
}

.wait-time-section,
.how-it-works-section {
  padding: 60px 80px;
  text-align: center;
}

.wait-time-box {
  max-width: 500px;
  margin: 20px auto 0;
  background: white;
  border-radius: 12px;
  padding: 24px;
  min-height: 180px;
}

.how-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  max-width: 900px;
  margin: 24px auto 0;
}

.how-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  min-height: 120px;
}

.footer {
  background: #16352f;
  color: white;
  padding: 32px 80px;
  text-align: center;
}

@media (max-width: 1024px) {
  .hero-section,
  .results-content,
  .how-cards {
    grid-template-columns: 1fr;
  }

  .hero-section,
  .search-toggle-section,
  .results-section,
  .wait-time-section,
  .how-it-works-section,
  .footer {
    padding-left: 24px;
    padding-right: 24px;
  }

  .hero-left h1 {
    font-size: 38px;
  }
}
</style>