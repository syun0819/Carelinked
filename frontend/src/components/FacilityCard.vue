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
          <p class="facility-address">📍 {{ displayAddress }}</p>

          <div class="tag-row">
            <span v-if="facility.careType" class="tag-chip" :class="careTypeClass">
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
        <p v-if="facility.distance !== null && facility.distance !== undefined" class="distance-line">
          📍
          <span>{{ facility.distance }} km away</span>
        </p>

        <button class="details-btn" @click.stop="goToDetail">
          View details →
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
  facility: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const route = useRoute()


const goToDetail = () => {
  router.push({
    path: `/facility/${props.facility.id}`,
    query: route.query
  })
}

const availabilityLevel = computed(() => {
  return props.facility.bedAvailability || 'Unknown'
})

const displayAddress = computed(() => {
  const locationParts = [props.facility.suburb, props.facility.postcode].filter(Boolean)
  const locationText = locationParts.join(' ')

  if (!props.facility.address) {
    return locationText || 'Location unavailable'
  }

  if (!locationText || props.facility.address.includes(locationText)) {
    return props.facility.address
  }

  return `${props.facility.address}, ${locationText}`
})

const careTypeClass = computed(() => {
  const type = (props.facility.careType || '').toLowerCase()

  if (type.includes('residential')) return 'tag-residential'
  if (type.includes('home care') || type.includes('hcp')) return 'tag-home-care'
  if (type.includes('transition')) return 'tag-transition'
  if (type.includes('restorative') || type.includes('strc')) return 'tag-restorative'
  if (type.includes('multi-purpose')) return 'tag-multi-purpose'
  if (type.includes('aboriginal') || type.includes('torres strait')) return 'tag-indigenous'

  return 'tag-default'
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
  font-family: var(--font-sans);
}

.facility-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 20px 28px 0;
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
  font-size: 24px;
  line-height: 1.25;
  font-weight: 700;
  color: #24332f;
  font-family: var(--font-display);

  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.facility-address {
  margin: 10px 0 0;
  color: #5f736b;
  font-size: 16px;
  line-height: 1.55;
  overflow-wrap: anywhere;
}

.recommended-badge {
  flex-shrink: 0;
  background: #eaf4ec;
  color: #537764;
  padding: 9px 14px;
  border-radius: 999px;
  font-size: 14px;
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
  color: #4f6f60;
  border-radius: 999px;
  padding: 9px 14px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.1;
  white-space: nowrap;
}

.tag-residential {
  background: #e4efe8;
  color: #376c57;
}

.tag-home-care {
  background: #e7eff5;
  color: #416987;
}

.tag-transition {
  background: #f0ebf9;
  color: #6752a1;
}

.tag-restorative {
  background: #f7eadf;
  color: #9a6228;
}

.tag-multi-purpose {
  background: #ecefe7;
  color: #617053;
}

.tag-indigenous {
  background: #f3e8dc;
  color: #8a5931;
}

.tag-default {
  background: #eef5ef;
  color: #4f6f60;
}

.metrics-row {
  margin-top: 8px;
  padding: 10px 0;
  border-top: 1px solid #ece7dd;
  border-bottom: 1px solid #ece7dd;
}

.metric-block {
  text-align: center;
}

.metric-value {
  font-size: 30px;
  line-height: 1;
  font-weight: 700;
  font-family: var(--font-display);
}

.metric-caption {
  font-size: 13px;
  color: #4f655d;
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
  padding: 14px 0;
  border-bottom: 1px solid #ece7dd;
  color: #5e706a;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.55;
}

.facility-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px 0 14px;
}

.distance-line {
  margin: 0;
  color: #4d645c;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-wrap: anywhere;
}

.details-btn {
  margin-left: auto;
  border: none;
  background: #557067;
  color: white;
  border-radius: 999px;
  padding: 13px 24px;
  font-weight: 600;
  font-size: 16px;
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
    margin-left: 0;
  }
}
</style>
