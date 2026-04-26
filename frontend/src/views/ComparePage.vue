<template>
  <div class="compare-page">
    <Header />
    <div class="compare-container">
      <h1 class="compare-title">Compare Facilities</h1>
      <p class="compare-sub">Coming soon.</p>
    </div>
    <FooterSection />
  </div>
</template>

<script setup>
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
</script>

<style scoped>
.compare-page {
  background: #f7f4ee;
  min-height: 100vh;
}

.compare-container {
  max-width: 1360px;
  margin: 0 auto;
  padding: 140px 32px 80px;
  text-align: center;
}

.compare-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  color: #22332e;
  margin: 0 0 12px;
}

.compare-sub {
  font-size: 16px;
  color: #7f8d87;
}
</style>
