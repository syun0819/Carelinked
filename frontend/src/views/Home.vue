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
    </section>

    <ExploreSection
      v-if="currentMode === 'explore'"
      :facilities="mockFacilities"
    />

    <SearchSection
      v-else
      :facilities="mockFacilities"
    />

    <ExploreSection :facilities="mockFacilities" />

    <HowItWorksSection />

    <FooterSection />
  </div>
</template>

<script setup>
import Header from '../components/Header.vue'
import HeroSection from '../components/HeroSection.vue'
import ExploreSection from '../components/ExploreSection.vue'
import HowItWorksSection from '../components/HowItWorksSection.vue'
import FooterSection from '../components/FooterSection.vue'
import mockFacilities from '../mock_data/mockFacilities.js'
</script>

<style scoped>
.home-page {
  width: 100%;
  background: #f7f4ee;
  color: #1f2d2a;
  min-height: 100vh;
}

.stats-section {
  position: relative;
  z-index: 10;
  margin-top: -35px;
  padding: 0 24px 24px;
  display: flex;
  justify-content: center;
  background: transparent;
}

.stats-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  padding: 8px 18px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}

.stats-icon {
  font-size: 20px;
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
  line-height: 1.3;
  font-family: 'Inter', sans-serif;
}

.stats-text {
  font-size: 12px;
  color: #61706a;
  line-height: 1.2;
  font-family: 'Inter', sans-serif;
}
</style>