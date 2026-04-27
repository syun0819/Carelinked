<template>
  <div class="info-card resident-card">
    <div class="resident-title-row">
      <svg class="resident-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78Z"/>
      </svg>
      <h2 class="section-title">Resident Experience</h2>
    </div>

    <div class="resident-grid">
      <div v-for="metric in metrics" :key="metric.label" class="resident-metric">
        <div class="resident-metric-header">
          <span class="resident-metric-label">{{ metric.label }}</span>
          <span class="resident-metric-pct">{{ metric.pct }}%</span>
        </div>
        <div class="resident-bar-track">
          <div class="resident-bar-fill" :style="{ width: metric.pct + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const metrics = [
  { label: 'Food',            pct: 65 },
  { label: 'Safety',          pct: 72 },
  { label: 'Respect',         pct: 70 },
  { label: 'Caring',          pct: 75 },
  { label: 'Feeling at Home', pct: 64 },
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

.resident-card { display: flex; flex-direction: column; gap: 20px; }

.resident-title-row { display: flex; align-items: center; gap: 10px; }

.resident-icon {
  width: 20px;
  height: 20px;
  color: #3d6b59;
  flex: 0 0 auto;
}

.resident-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px 32px;
}

.resident-metric { display: flex; flex-direction: column; gap: 6px; }

.resident-metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.resident-metric-label {
  font-size: 14px;
  font-weight: 500;
  color: #3a4e47;
}

.resident-metric-pct {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

.resident-bar-track {
  width: 100%;
  height: 8px;
  background: #e8e2d8;
  border-radius: 999px;
  overflow: hidden;
}

.resident-bar-fill {
  height: 100%;
  background: #3d6b59;
  border-radius: 999px;
  transition: width 0.4s ease;
}

@media (max-width: 768px) {
  .resident-grid { grid-template-columns: 1fr; }
}
</style>
