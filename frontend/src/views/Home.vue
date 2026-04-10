<template>
  <div class="home-page">
    <Header />

    <HeroSection />

    <section class="mode-switch-section">
      <div class="stats-wrapper">
        <div class="stats-bar">
          <div class="stats-icon">🏥</div>
          <div class="stats-content">
            <div class="stats-number">400+</div>
            <div class="stats-text">Facilities across Victoria</div>
          </div>
        </div>
      </div>
    </section>

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

.mode-switch-section {
  position: relative;
  margin-top: -36px;
  z-index: 2;
}

.stats-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  padding: 0 24px;
}

.stats-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  background: #ffffff;
  border: 2px solid #d8d1c8;
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 100px;
}

.stats-icon {
  font-size: 28px;
  line-height: 1;
}

.stats-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}

.stats-number {
  font-size: 18px;
  font-weight: 700;
  color: #223432;
  line-height: 1.1;
}

.stats-text {
  font-size: 10px;
  color: #5f7f79;
  line-height: 1.3;
  margin-top: 4px;

}
</style>