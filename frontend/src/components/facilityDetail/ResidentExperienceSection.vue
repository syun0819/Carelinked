<template>
  <div class="info-card">
    <div class="resident-header">
      <h2 class="section-title">Resident Experience</h2>
    </div>

    <div class="resident-grid">
      <div v-for="metric in metrics" :key="metric.label" class="resident-metric">
        <span class="resident-label">{{ metric.label }}</span>
        <div class="resident-stars" :aria-label="metric.value != null ? `${metric.label} rating ${metric.value.toFixed(1)} out of 5` : `${metric.label} rating unavailable`">
          <template v-if="metric.value != null">
            <span v-for="i in metric.full" :key="'f' + i" class="star filled">★</span>
            <span v-for="i in metric.empty" :key="'e' + i" class="star empty">★</span>
            <span class="resident-num">{{ metric.value.toFixed(1) }}</span>
          </template>
          <span v-else class="no-data-text">N/A</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  facility: { type: Object, required: true }
})

function toStars(val) {
  if (val == null) return { full: 0, empty: 5, value: null }
  const value = Math.max(0, Math.min(5, Number(val)))
  const full = Math.max(0, Math.min(5, Math.round(value)))
  return { full, empty: 5 - full, value }
}

const metrics = computed(() => [
  { label: 'Food',            ...toStars(props.facility?.reFoodScore) },
  { label: 'Safety',          ...toStars(props.facility?.reSafetyScore) },
  { label: 'Respect',         ...toStars(props.facility?.reRespectScore) },
  { label: 'Caring',          ...toStars(props.facility?.reCaringScore) },
  { label: 'Feeling at Home', ...toStars(props.facility?.reHomeScore) },
])
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

.resident-header {
  display: flex;
  align-items: center;
  margin-bottom: 18px;
}

.resident-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.resident-metric {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f5ef;
  border: 1px solid #e8e2d8;
  border-radius: 10px;
  padding: 12px 14px;
  gap: 8px;
}

.resident-label {
  font-size: 13.5px;
  font-weight: 600;
  color: #3a4e47;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.resident-stars {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}

.star { font-size: 16px; line-height: 1; }
.star.filled { color: #e8a023; }
.star.empty { color: #d8d0c4; }

.resident-num {
  margin-left: 5px;
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
}

.no-data-text {
  font-size: 13px;
  color: #a0a8a4;
}

@media (max-width: 768px) {
  .resident-grid { grid-template-columns: 1fr; }
}
</style>
