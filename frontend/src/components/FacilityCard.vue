<template>
  <article class="facility-card">
    <div class="facility-image-wrap">
      <img
        :src="facility.image"
        :alt="facility.name"
        class="facility-image"
      />
    </div>

    <div class="facility-body">
      <div class="facility-top-row">
        <div class="facility-main-info">
          <h3>{{ facility.name }}</h3>
          <p class="facility-address">
            <svg class="location-icon" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
              <circle cx="12" cy="9" r="2.5" />
            </svg>
            <span>{{ displayAddress }}</span>
          </p>

          <div class="tag-row">
            <span v-if="facility.careType" class="tag-chip" :class="careTypeClass">
              {{ facility.careType }}
            </span>
          </div>
        </div>

      </div>

      <div class="metrics-row">
        <div class="metric-block availability">
          <div class="metric-value" :class="availabilityClass">
            {{ availabilityLevel || 'N/A' }}
          </div>
          <div class="metric-caption">AVAILABILITY</div>
        </div>

        <div class="metric-block">
          <div class="metric-value beds-value">{{ facility.totalBeds ?? 0 }}</div>
          <div class="metric-caption">TOTAL BEDS</div>
        </div>
      </div>

      <div class="facility-footer">
        <p v-if="facility.distance !== null && facility.distance !== undefined" class="distance-line">
          <svg class="location-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
            <circle cx="12" cy="9" r="2.5" />
          </svg>
          <span>{{ facility.distance }} km away</span>
        </p>

        <button class="details-btn" @click.stop="goToDetail">
          <span>View details</span>
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
  const v = availabilityLevel.value
  if (v === 'Likely Available') return 'availability-likely'
  if (v === 'Potentially Available') return 'availability-potential'
  if (v === 'Constrained by Market' || v === 'Constrained by Size') return 'availability-constrained'
  if (v === 'Highly Constrained') return 'availability-highly-constrained'
  if (v === 'Does Not Provide This Service') return 'availability-none'
  return 'availability-default'
})
</script>

<style scoped>
.facility-card {
  background: #ffffff;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(31, 45, 42, 0.08);
  font-family: var(--font-sans);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.facility-image-wrap {
  position: relative;
  height: 190px;
  overflow: hidden;
}

.facility-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.facility-body {
  padding: 18px 26px 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.facility-top-row {
  display: flex;
  min-height: 150px;
  padding-bottom: 24px;
  box-sizing: border-box;
}

.facility-main-info {
  flex: 1;
  min-width: 0;
  text-align: left;
  display: flex;
  flex-direction: column;
}

.facility-top-row h3 {
  margin: 0;
  font-size: 20px;
  line-height: 1.25;
  font-weight: 800;
  color: #24332f;
  font-family: var(--font-display);
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.facility-address {
  margin: 8px 0 0;
  color: #5f736b;
  font-size: 14px;
  line-height: 1.55;
  overflow-wrap: anywhere;
  display: flex;
  align-items: flex-start;
  gap: 7px;
}

.location-icon {
  width: 16px;
  height: 16px;
  flex: 0 0 auto;
  margin-top: 2px;
  color: #6f9181;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.tag-row {
  display: flex;
  gap: 10px;
  margin-top: auto;
  margin-bottom: 0;
  flex-wrap: wrap;
}

.tag-chip {
  background: #eef5ef;
  color: #4f6f60;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-top: 0;
  padding: 0;
  border-top: 1px solid #ece7dd;
  border-bottom: 1px solid #ece7dd;
}

.metric-block {
  min-height: 62px;
  padding: 12px 8px 3px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
}

.metric-block.availability {
  padding-top: 12px;
}

.metric-block + .metric-block {
  border-left: 1px solid #ece7dd;
}

.metric-value {
  font-size: 18px;
  line-height: 1.1;
  font-weight: 700;
  font-family: var(--font-display);
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-block.availability .metric-value {
  max-width: 100%;
  font-size: 16px;
  white-space: nowrap;
}

.beds-value {
  color: #24332f;
}

.metric-caption {
  margin-top: 2px;
  font-size: 9px;
  color: #4f655d;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-weight: 600;
}

.availability-likely {
  color: #4f7a62;
}

.availability-potential {
color: #c9a200;
}

.availability-constrained {
  color: #d9822b;
}

.availability-highly-constrained {
  color: #c53b2c;
}

.availability-none {
  color: #9e9e9e;
}

.metric-block.availability .availability-none {
  font-size: 12px;
}

.availability-default {
  color: #4f6a63;
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
  padding: 7px 24px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.details-btn:hover {
  background: #486158;
}

.details-arrow {
  font-size: 20px;
  line-height: 1;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .facility-image-wrap {
    height: 180px;
  }

  .facility-body {
    padding: 18px 18px 0;
  }

  .facility-top-row {
    min-height: auto;
    padding-bottom: 18px;
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

