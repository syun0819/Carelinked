<template>
  <div class="info-card">
    <div class="quality-header">
      <h2 class="section-title">Quality Ratings</h2>
      <div class="quality-overall">
        <span class="star filled">★</span>
        <span class="star filled">★</span>
        <span class="star filled">★</span>
        <span class="star empty">★</span>
        <span class="star empty">★</span>
        <span class="rating-value">3.0</span>
        <span class="overall-badge">OVERALL</span>
      </div>
    </div>

    <div class="quality-grid">
      <div v-for="item in ratingItems" :key="item.label" class="quality-item">
        <span class="quality-label">{{ item.label }}</span>
        <div class="quality-stars">
          <span v-for="i in item.full" :key="'f'+i" class="star filled">★</span>
          <span v-for="i in item.empty" :key="'e'+i" class="star empty">★</span>
          <span class="quality-num">{{ item.value }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const ratingItems = [
  { label: 'Resident Experience', full: 3, empty: 2, value: '3.0' },
  { label: 'Staffing',            full: 3, empty: 2, value: '3.0' },
  { label: 'Compliance',          full: 3, empty: 2, value: '3.0' },
  { label: 'Quality Measures',    full: 3, empty: 2, value: '3.0' },
]
</script>

<style scoped>
.info-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 18px 18px 16px;
}

.section-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: #22332e;
}

.quality-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.quality-overall {
  display: flex;
  align-items: center;
  gap: 3px;
}

.quality-overall .rating-value {
  margin-left: 6px;
  font-size: 16px;
  font-weight: 700;
  color: #22332e;
}

.overall-badge {
  margin-left: 6px;
  font-size: 11px;
  font-weight: 700;
  color: #7a8a84;
  letter-spacing: 0.06em;
  background: #f0ece4;
  padding: 2px 8px;
  border-radius: 4px;
}

.quality-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.quality-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f5ef;
  border: 1px solid #e8e2d8;
  border-radius: 10px;
  padding: 12px 14px;
  gap: 8px;
}

.quality-label {
  font-size: 13.5px;
  font-weight: 600;
  color: #3a4e47;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.quality-stars {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}

.star { font-size: 16px; line-height: 1; }
.star.filled { color: #e8a023; }
.star.empty  { color: #d8d0c4; }

.quality-num {
  margin-left: 5px;
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

.rating-value {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

@media (max-width: 768px) {
  .quality-grid { grid-template-columns: 1fr; }
}
</style>
