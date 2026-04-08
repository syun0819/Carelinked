<template>
  <section class="explore-section">
    
    <div class="summary-row">
      <p class="summary-text">
        Showing {{ facilities.length }} care facilities within 10km
      </p>
      <div class="sort-box">
        <label>Sort by:</label>
        <select v-model="sortOption">
            <option value="Closest to me">Closest to me</option>
            <option value="Shortest wait time">Shortest wait time</option>
        </select>
      </div>
    </div>

    <div class="explore-grid">
      <FacilityCard
        v-for="facility in facilities"
        :key="facility.id"
        :facility="facility"
      />
    </div>
  </section>
</template>

<script setup>
import FacilityCard from './FacilityCard.vue'

import { ref } from 'vue'

const sortOption = ref('Closest to me')

defineProps({
  facilities: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.explore-section {
  padding: 20px 80px 60px;
  background: #f7f4ee;
}

.stats-card {
  width: fit-content;
  margin: 0 auto 24px;
  background: white;
  border: 1px solid #e3dfd8;
  border-radius: 10px;
  padding: 10px 18px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
}

.summary-text {
  margin: 0;
  font-size: 13px;
  color: #6b736f;
  font-family: 'Inter', sans-serif;
}

.sort-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Inter', sans-serif;
}

.sort-box label {
  font-size: 13px;
  color: #6b736f;
}

.sort-box select {
  padding: 6px 10px;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  background: white;
  font-size: 13px;
  color: #1f2d2a;
  cursor: pointer;
  appearance: auto;
}

.sort-box select:focus,
.sort-box select:active {
  background-color: white;
  color: #1f2d2a;
  outline: none;
  border-color: #bfc8c2;
}

.explore-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
}

.pagination button {
  min-width: 32px;
  height: 32px;
  border: 1px solid #ddd8cf;
  background: white;
  border-radius: 999px;
  cursor: pointer;
  font-size: 13px;
  color: #5f6d67;
}

.pagination button.active {
  background: #5d8b72;
  color: white;
  border-color: #5d8b72;
}

@media (max-width: 1024px) {
  .explore-section {
    padding-left: 24px;
    padding-right: 24px;
  }

  .summary-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .explore-grid {
    grid-template-columns: 1fr;
  }
}
</style>