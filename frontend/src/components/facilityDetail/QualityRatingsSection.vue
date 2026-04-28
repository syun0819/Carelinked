<template>
  <div class="info-card">
    <div class="quality-header">
      <h2 class="section-title">Quality Ratings</h2>
      <div v-if="overallRating != null" class="quality-overall">
        <span v-for="i in overallFull" :key="'f'+i" class="star filled">★</span>
        <span v-for="i in (5 - overallFull)" :key="'e'+i" class="star empty">★</span>
        <span class="rating-value">{{ overallRating.toFixed(1) }}</span>
        <span class="overall-badge">OVERALL</span>
      </div>
      <div v-else class="quality-overall">
        <span class="no-data-text">No rating data</span>
      </div>
    </div>

    <div class="quality-grid">
      <div v-for="item in ratingItems" :key="item.label" class="quality-item">
        <span class="quality-label">{{ item.label }}</span>
        <div class="quality-stars">
          <template v-if="item.value != null">
            <span v-for="i in item.full" :key="'f'+i" class="star filled">★</span>
            <span v-for="i in item.empty" :key="'e'+i" class="star empty">★</span>
            <span class="quality-num">{{ item.value.toFixed(1) }}</span>
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

const overallRating = computed(() => props.facility?.overallStarRating ?? null)
const overallFull = computed(() => overallRating.value != null ? Math.max(0, Math.min(5, Math.round(overallRating.value))) : 0)

function toStars(val) {
  if (val == null) return { full: 0, empty: 5, value: null }
  const full = Math.max(0, Math.min(5, Math.round(val)))
  return { full, empty: 5 - full, value: val }
}

const ratingItems = computed(() => [
  { label: 'Resident Experience', ...toStars(props.facility?.residentsExperienceRating) },
  { label: 'Staffing',            ...toStars(props.facility?.staffingRating) },
  { label: 'Compliance',          ...toStars(props.facility?.complianceRating) },
  { label: 'Quality Measures',    ...toStars(props.facility?.qualityMeasuresRating) },
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

.no-data-text {
  font-size: 13px;
  color: #a0a8a4;
}

@media (max-width: 768px) {
  .quality-grid { grid-template-columns: 1fr; }
}
</style>
