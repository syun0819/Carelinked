<template>
  <article class="facility-card">
    <img
      :src="facility.image"
      :alt="facility.name"
      class="facility-image"
    />

    <div class="facility-body">
      <div class="facility-top-row">
        <div class="facility-main-info">
          <h3>{{ facility.name }}</h3>
          <p class="facility-address">📍 {{ facility.address }}</p>

          <div class="tag-row">
            <span v-if="facility.careType" class="tag-chip">
              {{ facility.careType }}
            </span>
          </div>
        </div>

        <span class="recommended-badge">Recommended</span>
      </div>

      <div class="metrics-row">
        <div class="metric-block availability">
          <div class="metric-value" :class="availabilityClass">
            {{ availabilityLevel || 'N/A' }}
          </div>
          <div class="metric-caption">BED AVAILABILITY ESTIMATION</div>
        </div>
      </div>

      <div class="info-line">
        <span>
          {{ facility.funding || `Residential places: ${facility.totalBeds ?? 0}` }}
        </span>
      </div>

      <div class="facility-footer">
        <p class="distance-line">
          📍
          <span v-if="facility.distance !== null && facility.distance !== undefined">
            {{ facility.distance }} km away
          </span>
          <span v-else>
            {{ facility.suburb || facility.postcode || 'Location unavailable' }}
          </span>
        </p>

        <button class="details-btn" @click.stop="goToDetail">
          View Details
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

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

const availabilityLevel = computed(() => {
  return props.facility.bedAvailability || 'Unknown'
})

const availabilityClass = computed(() => {
  if (availabilityLevel.value === 'High') return 'availability-high'
  if (availabilityLevel.value === 'Medium') return 'availability-medium'
  if (availabilityLevel.value === 'Low') return 'availability-low'
  return ''
})
</script>

<style scoped>
.facility-card {
  background: #ffffff;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.02);
}

.facility-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 16px 26px 0;
}

.facility-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  min-height: 100px;
}

.facility-main-info {
  flex: 1;
  min-width: 0;
  text-align: left;
}

.facility-top-row h3 {
  margin: 0;
  font-size: 18px;
  line-height: 1.3;
  font-weight: 700;
  color: #24332f;
  font-family: Georgia, serif;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.facility-address {
  margin: 10px 0 0;
  color: #7b8d87;
  font-size: 12px;
  line-height: 1.4;
  overflow-wrap: anywhere;
}

.recommended-badge {
  flex-shrink: 0;
  background: #eaf4ec;
  color: #7aa284;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  align-self: flex-start;
}

.tag-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  margin-bottom: 2px;
  flex-wrap: wrap;
}

.tag-chip {
  background: #eef5ef;
  color: #678072;
  border-radius: 999px;
  padding: 5px 12px;
  font-size: 10px;
  font-weight: 600;
  line-height: 1;
}

.provider-chip {
  background: #f1f0fb;
  color: #6c63b6;
}

.metrics-row {
  margin-top: 4px;
  padding: 4px 0;
  border-top: 1px solid #ece7dd;
  border-bottom: 1px solid #ece7dd;
}

.metric-block {
  text-align: center;
}

.metric-value {
  font-size: 24px;
  line-height: 1;
  font-weight: 700;
  font-family: Georgia, serif;
}

.metric-caption {
  font-size: 10px;
  color: #5f756d;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-weight: 600;
}

.availability-high {
  color: #4f7a62;
}

.availability-medium {
  color: #d9822b;
}

.availability-low {
  color: #c53b2c;
}

.availability-default {
  color: #4f6a63;
}

.info-line {
  padding: 10px 0 10px;
  border-bottom: 1px solid #ece7dd;
  color: #7b8d87;
  font-size: 12px;
  line-height: 1.4;
}

.facility-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 4px 0 4px;
}

.distance-line {
  margin: 0;
  color: #5f756d;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-wrap: anywhere;
}

.details-btn {
  border: none;
  background: #557067;
  color: white;
  border-radius: 999px;
  padding: 12px 22px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.details-btn:hover {
  background: #486158;
}

@media (max-width: 768px) {
  .facility-image {
    height: 180px;
  }

  .facility-body {
    padding: 18px 18px 0;
  }

  .facility-top-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .facility-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .details-btn {
    width: 100%;
  }
}
</style>