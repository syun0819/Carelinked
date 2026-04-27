<template>
  <div class="summary-section">
    <div class="summary-cards">
      <div class="summary-card">
        <div class="summary-value" :class="availabilityClass">
          {{ facility.bedAvailability }}
        </div>
        <div class="summary-label">BED AVAILABILITY ESTIMATION</div>
      </div>
      <div class="summary-card">
        <div class="summary-value wait-text">
          {{ facility.estimatedWait || 'Unknown' }}
        </div>
        <div class="summary-label">ESTIMATED WAIT</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">{{ facility.totalBeds }}</div>
        <div class="summary-label">TOTAL BEDS</div>
      </div>
    </div>

    <div class="info-card">
      <h2 class="section-title">Aged Care Details</h2>
      <div class="detail-overview">
        <div class="detail-overview-top">
          <section class="detail-tile detail-location-tile">
            <div class="detail-tile-heading">
              <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z" />
                <circle cx="12" cy="9" r="2.5" />
              </svg>
              <span>Location</span>
            </div>
            <div class="detail-location-grid">
              <div class="detail-stat">
                <span class="detail-stat-label">Suburbs</span>
                <span class="detail-stat-value">{{ facility.suburb || 'N/A' }}</span>
              </div>
              <div class="detail-stat">
                <span class="detail-stat-label">State</span>
                <span class="detail-stat-value">{{ stateAbbreviation }}</span>
              </div>
              <div class="detail-stat">
                <span class="detail-stat-label">Postcode</span>
                <span class="detail-stat-value">{{ facility.postcode || 'N/A' }}</span>
              </div>
            </div>
          </section>

          <section class="detail-tile detail-funding-tile">
            <div class="detail-tile-heading">
              <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="3.5" y="6.5" width="17" height="11" rx="2.5" />
                <circle cx="12" cy="12" r="2.2" />
              </svg>
              <span>Gov. Funding</span>
            </div>
            <div class="detail-funding-value">{{ formattedFunding }}</div>
          </section>
        </div>

        <div class="detail-overview-bottom">
          <section class="detail-tile detail-meta-tile">
            <div class="detail-tile-heading">
              <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 21s-6-3.8-8-8.6A5.2 5.2 0 0 1 12 5a5.2 5.2 0 0 1 8 7.4C18 17.2 12 21 12 21Z" />
                <path d="M9.5 12.5 11.2 14 14.8 10" />
              </svg>
              <span>Care Type</span>
            </div>
            <div class="detail-meta-value">{{ facility.careType || 'N/A' }}</div>
          </section>

          <section class="detail-tile detail-meta-tile">
            <div class="detail-tile-heading">
              <svg class="detail-tile-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M6 20V8.5h12V20" />
                <path d="M4 20h16" />
                <path d="M9 8.5V5h6v3.5" />
                <path d="M9 12h.01M15 12h.01M9 15.5h.01M15 15.5h.01" />
              </svg>
              <span>Organisation</span>
            </div>
            <div class="detail-meta-value">{{ facility.organisationType || 'N/A' }}</div>
          </section>
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

const availabilityClass = computed(() => {
  const value = props.facility?.bedAvailability
  if (value === 'Likely Available') return 'availability-likely'
  if (value === 'Potentially Available') return 'availability-potential'
  if (value === 'Constrained by Market' || value === 'Constrained by Size') return 'availability-constrained'
  if (value === 'Highly Constrained') return 'availability-highly-constrained'
  if (value === 'Does Not Provide This Service') return 'availability-none'
  return 'availability-default'
})

const stateAbbreviation = computed(() => {
  const state = props.facility?.state?.trim()
  if (!state) return 'N/A'
  const stateMap = {
    'New South Wales': 'NSW', Victoria: 'VIC', Queensland: 'QLD',
    'South Australia': 'SA', 'Western Australia': 'WA', Tasmania: 'TAS',
    'Northern Territory': 'NT', 'Australian Capital Territory': 'ACT'
  }
  return stateMap[state] || state.toUpperCase()
})

const formattedFunding = computed(() => {
  const funding = props.facility?.governmentFunding
  if (funding == null || funding === '') return 'N/A'
  const num = Number(funding)
  if (Number.isNaN(num)) return String(funding)
  return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 }).format(num)
})
</script>

<style scoped>
.summary-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.summary-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  min-height: 72px;
  padding: 16px 18px 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.summary-value {
  font-size: 19px;
  font-weight: 700;
  line-height: 1.15;
  color: #22332e;
}

.wait-text { color: #22332e; }

.availability-likely    { color: #4f7a62; }
.availability-potential { color: #c9a200; }
.availability-constrained { color: #d9822b; }
.availability-highly-constrained { color: #c53b2c; }
.availability-none      { color: #9e9e9e; }
.availability-default   { color: #4f6a63; }

.summary-label {
  margin-top: 6px;
  font-size: 11px;
  line-height: 1.35;
  color: #7f8d87;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.info-card {
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 18px 18px 16px;
}

.section-title {
  margin: 0 0 16px;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: #22332e;
}

.detail-overview { display: flex; flex-direction: column; gap: 12px; }

.detail-overview-top {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(180px, 1fr);
  gap: 12px;
}

.detail-overview-bottom {
  display: grid;
  grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr);
  gap: 12px;
}

.detail-tile {
  border: 1px solid #e3ddd3;
  border-radius: 12px;
  background: #fff;
  padding: 12px 16px;
}

.detail-location-tile { background: #f3f0ea; padding: 10px 22px; }

.detail-funding-tile {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #f3f0ea;
  padding: 10px;
}

.detail-tile-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8a9791;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.detail-funding-tile .detail-tile-heading { justify-content: center; }

.detail-tile-icon {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.detail-location-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 10px;
}

.detail-stat { display: flex; flex-direction: column; gap: 4px; }

.detail-location-grid .detail-stat:first-child {
  align-items: flex-start;
  text-align: left;
  padding-left: 12px;
}

.detail-location-grid .detail-stat:not(:first-child) {
  align-items: flex-end;
  text-align: right;
}

.detail-location-grid .detail-stat:last-child {
  align-items: center;
  text-align: center;
  padding-right: 16px;
}

.detail-stat-label {
  font-size: 12px;
  font-weight: 700;
  color: #7b8882;
  text-transform: uppercase;
}

.detail-stat-value,
.detail-meta-value {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.15;
  color: #22332e;
}

.detail-meta-value { margin-top: 12px; text-align: left; }

.detail-funding-value {
  margin-top: 10px;
  font-size: 20px;
  font-weight: 800;
  color: #22332e;
}

@media (max-width: 768px) {
  .summary-cards { grid-template-columns: 1fr; }
  .detail-overview-top,
  .detail-overview-bottom,
  .detail-location-grid { grid-template-columns: 1fr; }
  .detail-location-grid .detail-stat:not(:first-child),
  .detail-location-grid .detail-stat:last-child {
    align-items: flex-start;
    text-align: left;
  }
}
</style>
