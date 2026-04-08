<template>
  <div class="home-page">
    <Header />

    <section class="hero-section">
      <div class="hero-left">
        <p class="hero-badge">Aged Care Bed Finder - Victoria</p>
        <h1>
          Find the right
          care place, <span>near you right now</span>          
        </h1>
        <p class="hero-description">
          Search available beds across residential aged care and home care services in 
          Victoria, with real wait times and funding options explained clearly.
        </p>

        <button class="primary-btn">Search Care Places</button>

        <div class="care-tags">
          <span>Residential Care</span>
          <span>New Care Places</span>
          <span>Memory Care</span>
          <span>Respite Care</span>
          <span>High-Level Care</span>
        </div>
      </div>

      <div class="hero-right">
        <div class="hero-image-card">
          Main Visual / Carousel
        </div>
      </div>
    </section>

    <section class="search-toggle-section">
      <div class="toggle-bar">
        <button>Explore</button>
        <button>Search</button>
      </div>
    </section>

    <section class="results-section">
      <div class="results-toolbar">
        <input type="text" placeholder="Search by facility name, suburb or postcode" />
      </div>

      <div class="results-content">
        <aside class="filter-panel">
          <FilterPanel />
        </aside>

        <main class="results-main">
          <FacilityList />
        </main>
      </div>
    </section>

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
import Header from '../components/Header.vue'
import FilterPanel from '../components/FilterPanel.vue'
import FacilityList from '../components/FacilityList.vue'
</script>

<style scoped>
.home-page {
  background: #f7f4ee;
  color: #1f2d2a;
  min-height: 100vh;
}

.hero-section {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 40px;
  padding: 60px 80px;
  background: #dfe8e3;
  align-items: center;
}

.hero-left h1 {
  font-size: 52px;
  line-height: 1.15;
  color: #1a1a1a;
  margin: 16px 0;
  max-width: 520px;
}

.hero-left h1 span {
  color: #5d8b72;
}

.hero-description {
  max-width: 500px;
  font-size: 16px;
  line-height: 1.7;
  color: #5f6d67;
  margin-bottom: 20px;
}

.hero-badge {
  display: inline-block;
  padding: 6px 12px;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  color: #5f6d67;
}

.primary-btn {
  background: #5d8b72;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 20px;
}

.care-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.care-tags span {
  padding: 6px 10px;
  border: 1px solid #d4d4d4;
  background: white;
  border-radius: 8px;
  font-size: 13px;
}

.hero-right {
  display: flex;
  justify-content: center;
}

.hero-image-card {
  width: 100%;
  max-width: 520px;
  height: 320px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-toggle-section {
  padding: 20px 80px;
  background: #f7f4ee;
}

.toggle-bar {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.toggle-bar button {
  border: 1px solid #cfd7d2;
  background: white;
  padding: 10px 18px;
  border-radius: 20px;
  cursor: pointer;
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