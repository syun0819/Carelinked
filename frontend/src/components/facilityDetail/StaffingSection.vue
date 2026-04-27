<template>
  <div class="info-card staffing-card">
    <div class="staffing-title-row">
      <svg class="staffing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
      <h2 class="section-title">Staffing &amp; Compliance</h2>
    </div>

    <div v-for="metric in metrics" :key="metric.label" class="staffing-metric">
      <div class="staffing-metric-header">
        <span class="staffing-metric-label">{{ metric.label }}</span>
        <span class="staffing-badge badge-unmet">
          <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          Target not met
        </span>
      </div>
      <div class="staffing-bar-track">
        <div class="staffing-bar-fill" :style="{ width: metric.percent + '%' }"></div>
      </div>
      <div class="staffing-metric-footer">
        <span>Actual: {{ metric.actual }}</span>
        <span>Target: {{ metric.target }}</span>
      </div>
    </div>

    <div class="staffing-compliance-row">
      <div class="staffing-compliance-left">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#c07a40" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <span class="staffing-compliance-label">Compliance status</span>
      </div>
      <span class="staffing-badge badge-action">Action taken</span>
    </div>
    <p class="staffing-compliance-note">Compliance notice issued; remediation underway.</p>
  </div>
</template>

<script setup>
const metrics = [
  { label: 'Registered Nurse care minutes', actual: '36 mins/day', target: '44 mins/day', percent: 81 },
  { label: 'Total care minutes',            actual: '195 mins/day', target: '215 mins/day', percent: 91 },
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

.badge-unmet { background: #fdecea; color: #c0392b; }
.badge-action { background: #fef3e2; color: #c07a40; }

.staffing-bar-track {
  width: 100%;
  height: 8px;
  background: #e8e2d8;
  border-radius: 999px;
  overflow: hidden;
}

.staffing-bar-fill {
  height: 100%;
  background: #3d6b59;
  border-radius: 999px;
  transition: width 0.4s ease;
}

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

.staffing-compliance-note { margin: 0; font-size: 13px; color: #7f8d87; }
</style>
