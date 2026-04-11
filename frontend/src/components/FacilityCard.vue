<template>
  <article class="facility-card">
    <img
      :src="facility.image"
      :alt="facility.name"
      class="facility-image"
    />

    <div class="facility-body">
      <div class="facility-top-row">
        <div>
          <h3>{{ facility.name }}</h3>
          <p class="facility-address">
            📍 {{ facility.address }}
          </p>
        </div>

        <span class="recommended-badge">Recommended</span>
      </div>

      <div class="tag-row">
        <span class="tag-chip">{{ facility.careType }}</span>
        <span class="tag-chip">{{ facility.provider }}</span>
      </div>

      <div class="metrics-row">
        <div class="metric-block availability">
        <div
          class="metric-value"
          :class="availabilityClass"
        >
          {{ facility.bedAvailability }}
        </div>
        <div class="metric-caption">BEDS AVAILABLE</div>
      </div>

        <div class="metric-block wait-time">
          <div class="metric-value">{{ facility.distance }} km</div>
          <div class="metric-caption">DISTANCE</div>
        </div>
      </div>

      <div class="facility-footer">
        <p class="places-line">
          Total beds: {{ facility.totalBeds }} · {{ facility.state }}
        </p>

        <button class="details-btn" @click.stop="goToDetail">
          View Details
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const availabilityClass = computed(() => {
  const level = props.facility.bedAvailability

  if (level === 'High') return 'availability-high'
  if (level === 'Medium') return 'availability-medium'
  if (level === 'Low') return 'availability-low'
  return ''
})

const props = defineProps({
  facility: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/facility/${props.facility.id}`)
}
</script>

<style scoped>
.facility-card {
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 12px;
  overflow: hidden;
}

.facility-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 18px 20px;
}

.facility-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.facility-top-row h3 {
  margin: 0;
  font-size: 20px;
}

.facility-address {
  margin: 8px 0 0;
  color: #7b8d87;
  font-size: 14px;
}

.recommended-badge {
  background: #eaf4ec;
  color: #7aa284;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.availability-high {
  color: #4f7a62;
}

.availability-medium {
  color: #d9822b;
}

.availability-low {
  color: #d64545;
}

.tag-row {
  display: flex;
  gap: 8px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.tag-chip {
  background: #eef5ef;
  color: #678072;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-top: 18px;
  padding: 18px 0;
  border-top: 1px solid #ece7dd;
  border-bottom: 1px solid #ece7dd;
}

.metric-block {
  text-align: center;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
}

.metric-caption {
  margin-top: 4px;
  font-size: 11px;
  color: #7b8d87;
}

.wait-time .metric-value {
  color: #c98a3d;
}

.facility-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.places-line {
  margin: 0;
  color: #7b8d87;
  font-size: 14px;
}

.details-btn {
  border: none;
  background: #557067;
  color: white;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 600;
  cursor: pointer;
}
</style>