<template>
  <div class="info-card staffing-card">
    <div class="staffing-title-row">
      <svg class="staffing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
      <h2 class="section-title">Staffing &amp; Compliance</h2>
    </div>

    <div v-if="hasData">
      <div v-for="metric in metrics" :key="metric.label" class="staffing-metric">
        <div class="staffing-metric-header">
          <span class="staffing-metric-label">{{ metric.label }}</span>
          <span v-if="metric.met" class="staffing-badge badge-met">
            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            Target met
          </span>
          <span v-else class="staffing-badge badge-unmet">
            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            Target not met
          </span>
        </div>
        <div class="staffing-bar-track">
          <div class="staffing-bar-fill" :class="metric.met ? 'bar-met' : 'bar-unmet'" :style="{ width: Math.min(metric.percent, 100) + '%' }"></div>
        </div>
        <div class="staffing-metric-footer">
          <span>Actual: {{ metric.actual }}</span>
          <span>Target: {{ metric.target }}</span>
        </div>
      </div>

      <div class="staffing-compliance-row">
        <div class="staffing-compliance-left">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" :stroke="complianceColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
          <span class="staffing-compliance-label">Compliance status</span>
        </div>
        <span class="staffing-badge" :class="complianceBadgeClass">{{ complianceLabel }}</span>
      </div>
    </div>

    <div v-else class="no-data-msg">
      No staffing data available for this facility.
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  facility: { type: Object, required: true }
})

const hasData = computed(() =>
  props.facility?.sRnCareMinutesActual != null ||
  props.facility?.sTotalCareMinutesActual != null
)

function fmtMins(val) {
  if (val == null) return 'N/A'
  return `${Math.round(val)} mins/day`
}

function pct(actual, target) {
  if (!actual || !target) return 0
  return Math.round((actual / target) * 100)
}

const metrics = computed(() => [
  {
    label: 'Registered Nurse care minutes',
    actual: fmtMins(props.facility?.sRnCareMinutesActual),
    target: fmtMins(props.facility?.sRnCareMinutesTarget),
    percent: pct(props.facility?.sRnCareMinutesActual, props.facility?.sRnCareMinutesTarget),
    met: props.facility?.rnMinutesMet === true,
  },
  {
    label: 'Total care minutes',
    actual: fmtMins(props.facility?.sTotalCareMinutesActual),
    target: fmtMins(props.facility?.sTotalCareMinutesTarget),
    percent: pct(props.facility?.sTotalCareMinutesActual, props.facility?.sTotalCareMinutesTarget),
    met: props.facility?.totalMinutesMet === true,
  },
])

const allMet = computed(() =>
  props.facility?.rnMinutesMet === true && props.facility?.totalMinutesMet === true
)

const complianceLabel = computed(() => allMet.value ? 'Compliant' : 'Action taken')
const complianceBadgeClass = computed(() => allMet.value ? 'badge-compliant' : 'badge-action')
const complianceColor = computed(() => allMet.value ? '#3d6b59' : '#c07a40')
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

.staffing-card { display: flex; flex-direction: column; gap: 20px; }

.staffing-title-row { display: flex; align-items: center; gap: 10px; }

.staffing-icon {
  width: 20px;
  height: 20px;
  color: #3d6b59;
  flex: 0 0 auto;
}

.staffing-metric { display: flex; flex-direction: column; gap: 6px; }

.staffing-metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.staffing-metric-label { font-size: 14px; font-weight: 600; color: #3a4e47; }

.staffing-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  white-space: nowrap;
}

.badge-unmet   { background: #fdecea; color: #c0392b; }
.badge-met     { background: #e6f4ed; color: #2e7d5a; }
.badge-action  { background: #fef3e2; color: #c07a40; }
.badge-compliant { background: #e6f4ed; color: #2e7d5a; }

.staffing-bar-track {
  width: 100%;
  height: 8px;
  background: #e8e2d8;
  border-radius: 999px;
  overflow: hidden;
}

.staffing-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.4s ease;
}

.bar-met   { background: #3d6b59; }
.bar-unmet { background: #c0392b; }

.staffing-metric-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #7f8d87;
}

.staffing-compliance-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding-top: 4px;
  border-top: 1px solid #ede8e0;
}

.staffing-compliance-left { display: flex; align-items: center; gap: 8px; }

.staffing-compliance-label { font-size: 14px; font-weight: 600; color: #3a4e47; }

.no-data-msg {
  font-size: 14px;
  color: #a0a8a4;
  padding: 8px 0;
}
</style>
