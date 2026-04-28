<template>
  <div class="compare-page">
    <Header />
    <div class="compare-container">

      <!-- Page header -->
      <div class="compare-header">
        <div class="compare-header-left">
          <h1 class="compare-title">Compare {{ facilities.length }} facilit{{ facilities.length === 1 ? 'y' : 'ies' }}</h1>
          <p class="compare-subtitle">Side-by-side view of wait times, quality, staffing and compliance.</p>
        </div>
        <div class="compare-header-actions">
          <button class="action-btn-outline" @click="goBack">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
            Back to search
          </button>
          <button class="action-btn-outline" @click="clearAll">Clear all</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="state-box">
        <div class="loading-spinner"></div>
        <p>Loading facilities…</p>
      </div>

      <!-- Table (always shown when not loading) -->
      <div v-else class="compare-table-wrap">
        <table class="compare-table">
          <colgroup>
            <col class="col-label" />
            <col class="col-facility" />
            <col class="col-facility" />
          </colgroup>

          <!-- Facility header row: filled cards + search slots -->
          <thead>
            <tr class="facility-header-row">
              <th class="label-cell"><span class="facility-label-head">FACILITY</span></th>

              <!-- Filled facility slots -->
              <th v-for="f in facilities" :key="f.id" class="facility-cell">
                <div class="facility-card-head">
                  <button class="remove-btn" @click="removeFacility(f.id)" aria-label="Remove">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                  <img :src="f.image" :alt="f.name" class="facility-thumb" />
                  <div class="facility-name">{{ f.name }}</div>
                  <div class="facility-location">{{ f.suburb }}, {{ f.state }} {{ f.postcode }}</div>
                </div>
              </th>

              <!-- Empty search slots -->
              <th v-for="i in (2 - facilities.length)" :key="'slot-' + i" class="facility-cell search-slot-cell">
                <div class="facility-search-slot">
                  <div class="slot-placeholder">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#c8c2b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                    <span>Search a facility</span>
                  </div>
                  <div class="slot-search-wrap">
                    <svg class="search-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                    <input
                      v-model="searchQuery"
                      class="slot-search-input"
                      placeholder="Type facility name…"
                      @input="onSearchInput"
                    />
                    <div v-if="searchLoading" class="search-spinner"></div>
                  </div>
                  <div v-if="searchResults.length > 0" class="slot-results">
                    <div v-for="r in searchResults" :key="r.id" class="slot-result-item" @click="addFromSearch(r)">
                      <div class="slot-result-name">{{ r.name }}</div>
                      <div class="slot-result-meta">{{ r.suburb }}, {{ r.state }}</div>
                    </div>
                  </div>
                  <p v-else-if="searchQuery && !searchLoading" class="search-empty">No results found.</p>
                </div>
              </th>
            </tr>
          </thead>

          <tbody v-if="facilities.length === 2">
            <!-- Care type -->
            <tr class="compare-row">
              <td class="label-cell">Care type</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span class="value-text">{{ f.careType || 'N/A' }}</span>
              </td>
            </tr>

            <!-- Estimated wait time -->
            <tr class="compare-row">
              <td class="label-cell">Estimated wait time</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span class="na-text">Unknown</span>
              </td>
            </tr>

            <!-- Overall rating -->
            <tr class="compare-row">
              <td class="label-cell">Overall rating</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <div class="stars-row">
                  <template v-if="f.overallStarRating != null">
                    <span v-for="i in starsFor(f.overallStarRating).full" :key="'f'+i" class="star filled">★</span>
                    <span v-for="i in starsFor(f.overallStarRating).empty" :key="'e'+i" class="star empty">★</span>
                    <span class="star-num">{{ f.overallStarRating.toFixed(1) }}</span>
                    <span v-if="isHighest(f, 'overallStarRating')" class="best-badge">
                      <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                      Highest rated
                    </span>
                  </template>
                  <span v-else class="na-text">N/A</span>
                </div>
              </td>
            </tr>

            <!-- Resident experience rating -->
            <tr class="compare-row">
              <td class="label-cell">Resident experience rating</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <div class="stars-row">
                  <template v-if="f.residentsExperienceRating != null">
                    <span v-for="i in starsFor(f.residentsExperienceRating).full" :key="'f'+i" class="star filled">★</span>
                    <span v-for="i in starsFor(f.residentsExperienceRating).empty" :key="'e'+i" class="star empty">★</span>
                    <span class="star-num">{{ f.residentsExperienceRating.toFixed(1) }}</span>
                  </template>
                  <span v-else class="na-text">N/A</span>
                </div>
              </td>
            </tr>

            <!-- Staffing rating -->
            <tr class="compare-row">
              <td class="label-cell">Staffing rating</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <div class="stars-row">
                  <template v-if="f.staffingRating != null">
                    <span v-for="i in starsFor(f.staffingRating).full" :key="'f'+i" class="star filled">★</span>
                    <span v-for="i in starsFor(f.staffingRating).empty" :key="'e'+i" class="star empty">★</span>
                    <span class="star-num">{{ f.staffingRating.toFixed(1) }}</span>
                  </template>
                  <span v-else class="na-text">N/A</span>
                </div>
              </td>
            </tr>

            <!-- Compliance rating -->
            <tr class="compare-row">
              <td class="label-cell">Compliance rating</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <div class="stars-row">
                  <template v-if="f.complianceRating != null">
                    <span v-for="i in starsFor(f.complianceRating).full" :key="'f'+i" class="star filled">★</span>
                    <span v-for="i in starsFor(f.complianceRating).empty" :key="'e'+i" class="star empty">★</span>
                    <span class="star-num">{{ f.complianceRating.toFixed(1) }}</span>
                  </template>
                  <span v-else class="na-text">N/A</span>
                </div>
              </td>
            </tr>

            <!-- Quality measures rating -->
            <tr class="compare-row">
              <td class="label-cell">Quality measures rating</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <div class="stars-row">
                  <template v-if="f.qualityMeasuresRating != null">
                    <span v-for="i in starsFor(f.qualityMeasuresRating).full" :key="'f'+i" class="star filled">★</span>
                    <span v-for="i in starsFor(f.qualityMeasuresRating).empty" :key="'e'+i" class="star empty">★</span>
                    <span class="star-num">{{ f.qualityMeasuresRating.toFixed(1) }}</span>
                  </template>
                  <span v-else class="na-text">N/A</span>
                </div>
              </td>
            </tr>

            <!-- Total beds -->
            <tr class="compare-row">
              <td class="label-cell">Total beds</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span class="value-text">{{ f.totalBeds ?? 'N/A' }}</span>
              </td>
            </tr>

            <!-- RN care minutes -->
            <tr class="compare-row">
              <td class="label-cell">RN care minutes<br /><span class="label-sub">(actual / target)</span></td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span v-if="f.sRnCareMinutesActual != null" class="value-text">
                  {{ Math.round(f.sRnCareMinutesActual) }} / {{ Math.round(f.sRnCareMinutesTarget) }} mins
                </span>
                <span v-else class="na-text">N/A</span>
                <span v-if="f.sRnCareMinutesActual != null" class="met-badge" :class="f.rnMinutesMet ? 'badge-met' : 'badge-unmet'">
                  <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline v-if="f.rnMinutesMet" points="20 6 9 17 4 12"/>
                    <circle v-else cx="12" cy="12" r="10"/><line v-if="!f.rnMinutesMet" x1="12" y1="8" x2="12" y2="12"/><line v-if="!f.rnMinutesMet" x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  {{ f.rnMinutesMet ? 'Met' : 'Not met' }}
                </span>
              </td>
            </tr>

            <!-- Total care minutes -->
            <tr class="compare-row">
              <td class="label-cell">Total care minutes<br /><span class="label-sub">(actual / target)</span></td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span v-if="f.sTotalCareMinutesActual != null" class="value-text">
                  {{ Math.round(f.sTotalCareMinutesActual) }} / {{ Math.round(f.sTotalCareMinutesTarget) }} mins
                </span>
                <span v-else class="na-text">N/A</span>
                <span v-if="f.sTotalCareMinutesActual != null" class="met-badge" :class="f.totalMinutesMet ? 'badge-met' : 'badge-unmet'">
                  <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline v-if="f.totalMinutesMet" points="20 6 9 17 4 12"/>
                    <circle v-else cx="12" cy="12" r="10"/><line v-if="!f.totalMinutesMet" x1="12" y1="8" x2="12" y2="12"/><line v-if="!f.totalMinutesMet" x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  {{ f.totalMinutesMet ? 'Met' : 'Not met' }}
                </span>
              </td>
            </tr>

            <!-- Compliance status -->
            <tr class="compare-row">
              <td class="label-cell">Compliance status</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span v-if="f.sRnCareMinutesActual != null" class="compliance-badge" :class="(f.rnMinutesMet && f.totalMinutesMet) ? 'compliance-ok' : 'compliance-action'">
                  {{ (f.rnMinutesMet && f.totalMinutesMet) ? 'No issues' : 'Action taken' }}
                </span>
                <span v-else class="na-text">N/A</span>
              </td>
            </tr>

            <!-- Resident scores -->
            <tr v-for="rs in residentScoreRows" :key="rs.key" class="compare-row">
              <td class="label-cell">{{ rs.label }}</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span v-if="f[rs.key] != null" class="value-text">{{ Math.round((f[rs.key] / 5) * 100) }}%</span>
                <span v-else class="na-text">N/A</span>
              </td>
            </tr>

            <!-- Government funding -->
            <tr class="compare-row">
              <td class="label-cell">Government funding</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span class="value-text">{{ formatFunding(f.governmentFunding) }}</span>
              </td>
            </tr>

            <!-- Provider -->
            <tr class="compare-row">
              <td class="label-cell">Provider</td>
              <td v-for="f in facilities" :key="f.id" class="data-cell">
                <span class="value-text">{{ f.provider || 'N/A' }}</span>
              </td>
            </tr>
          </tbody>

          <!-- View details footer -->
          <tfoot v-if="facilities.length === 2">
            <tr>
              <td class="label-cell"></td>
              <td v-for="f in facilities" :key="f.id" class="data-cell footer-cell">
                <button class="view-btn" @click="goToDetail(f.id)">View full details</button>
              </td>
            </tr>
          </tfoot>
        </table>

      </div>
    </div>
    <FooterSection />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import { useCompareStore } from '../stores/compareStore'
import { getFacilityDetail, searchFacilities } from '../services/facilitiesApi'
import { mapFacilityDetail, mapFacilityCard } from '../utils/facilityMappers'

const router = useRouter()
const compareStore = useCompareStore()

const facilities = ref([])
const loading = ref(false)

const searchQuery = ref('')
const searchResults = ref([])
const searchLoading = ref(false)
let searchTimer = null

function onSearchInput() {
  clearTimeout(searchTimer)
  const q = searchQuery.value.trim()
  if (!q) { searchResults.value = []; return }
  searchLoading.value = true
  searchTimer = setTimeout(async () => {
    try {
      const data = await searchFacilities({ keyword: q, limit: 6 })
      searchResults.value = (data.results || data.items || []).map(mapFacilityCard)
    } finally {
      searchLoading.value = false
    }
  }, 350)
}

async function addFromSearch(r) {
  if (compareStore.has(r.id) || compareStore.isFull) return
  compareStore.add(r.id, r.name)
  loading.value = true
  try {
    const detail = await getFacilityDetail(r.id).then(mapFacilityDetail)
    facilities.value = [...facilities.value, detail]
  } finally {
    loading.value = false
  }
  searchQuery.value = ''
  searchResults.value = []
}

const residentScoreRows = [
  { key: 'reFoodScore',    label: 'Resident - Food' },
  { key: 'reSafetyScore',  label: 'Resident - Safety' },
  { key: 'reRespectScore', label: 'Resident - Respect' },
  { key: 'reCaringScore',  label: 'Resident - Caring' },
  { key: 'reHomeScore',    label: 'Resident - Feeling at Home' },
]

onUnmounted(() => {
  compareStore.clear()
})

onMounted(async () => {
  if (compareStore.items.length === 0) return
  loading.value = true
  try {
    const results = await Promise.all(
      compareStore.items.map(({ id }) => getFacilityDetail(id).then(mapFacilityDetail))
    )
    facilities.value = results
  } finally {
    loading.value = false
  }
})

function starsFor(val) {
  const full = Math.max(0, Math.min(5, Math.round(val ?? 0)))
  return { full, empty: 5 - full }
}

function isHighest(facility, key) {
  if (facilities.value.length < 2) return false
  const vals = facilities.value.map(f => f[key] ?? -Infinity)
  const max = Math.max(...vals)
  return facility[key] === max && vals.filter(v => v === max).length === 1
}

const availOrder = ['Likely Available', 'Potentially Available', 'Constrained by Market', 'Constrained by Size', 'Highly Constrained', 'Does Not Provide This Service']

function isBestAvailability(facility) {
  if (facilities.value.length < 2) return false
  const ranks = facilities.value.map(f => availOrder.indexOf(f.bedAvailability ?? ''))
  const myRank = availOrder.indexOf(facility.bedAvailability ?? '')
  const minRank = Math.min(...ranks)
  return myRank === minRank && myRank !== -1 && ranks.filter(r => r === minRank).length === 1
}

function availClass(val) {
  if (val === 'Likely Available') return 'avail-likely'
  if (val === 'Potentially Available') return 'avail-potential'
  if (val === 'Constrained by Market' || val === 'Constrained by Size') return 'avail-constrained'
  if (val === 'Highly Constrained') return 'avail-high'
  if (val === 'Does Not Provide This Service') return 'avail-none'
  return 'avail-default'
}

function formatFunding(val) {
  if (val == null || val === '') return 'N/A'
  return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 }).format(val)
}

function removeFacility(id) {
  compareStore.remove(id)
  facilities.value = facilities.value.filter(f => f.id !== id)
}

function clearAll() {
  compareStore.clear()
  facilities.value = []
}

function goBack() {
  router.push('/find-bed')
}

function goToDetail(id) {
  router.push(`/facility/${id}`)
}
</script>

<style scoped>
.compare-page {
  background: #f7f4ee;
  min-height: 100vh;
}

.compare-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 110px 32px 80px;
}

/* ── Header ── */
.compare-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 28px;
}

.compare-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  color: #22332e;
  margin: 0 0 4px;
}

.compare-subtitle {
  font-size: 14px;
  color: #7f8d87;
  margin: 0;
}

.compare-header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.action-btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #c8c1b8;
  background: #fff;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: #4a5e57;
  cursor: pointer;
  transition: background 0.15s;
}

.action-btn-outline:hover { background: #f0ece4; }

/* ── State boxes ── */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: #7f8d87;
}

.state-msg { font-size: 15px; }

.primary-btn {
  background: #3d6b59;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 10px 28px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Table ── */
.compare-table-wrap {
  overflow-x: auto;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 14px;
  overflow: hidden;
  table-layout: fixed;
}

col.col-label    { width: 160px; }
col.col-facility { width: calc((100% - 160px) / 2); }

/* ── Facility header ── */
.facility-header-row th {
  background: #fff;
  padding: 0;
  vertical-align: middle;
  border-bottom: 1px solid #e8e2d8;
}

.label-cell {
  padding: 12px 14px;
  font-size: 14px;
  font-weight: 500;
  color: #7f8d87;
  text-align: left;
  vertical-align: middle;
  border-right: 1px solid #e8e2d8;
  background: #faf8f4;
  line-height: 1.4;
}

.facility-label-head {
  font-size: 14px;
  font-weight: 700;
  color: #a0a8a4;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding-left: 12px;
}

.label-sub {
  font-size: 11px;
  font-weight: 400;
  color: #a0a8a4;
}

.facility-cell {
  padding: 0;
  text-align: center;
  border-right: 1px solid #e8e2d8;
  vertical-align: top;
}
.facility-cell:last-child { border-right: none; }

.facility-card-head {
  position: relative;
  padding: 20px 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1px solid #ddd5ca;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7f8d87;
}
.remove-btn:hover { background: #fdecea; color: #c0392b; border-color: #f5c6c6; }

.facility-thumb {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 10px;
}

.facility-name {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
  text-align: center;
  line-height: 1.3;
}

.facility-location {
  font-size: 12px;
  color: #a0a8a4;
  text-align: center;
}

/* ── Data rows ── */
.compare-row {
  height: 64px;
}

.compare-row td {
  border-bottom: 1px solid #ede8e0;
  vertical-align: middle;
}

.compare-row:last-child td { border-bottom: none; }

.data-cell {
  padding: 12px 20px;
  text-align: center;
  border-right: 1px solid #e8e2d8;
  font-size: 14px;
  vertical-align: middle;
}
.data-cell:last-child { border-right: none; }

.value-text { font-weight: 600; color: #22332e; }

.na-text { color: #b0bdb8; font-size: 13px; }

/* ── Stars ── */
.stars-row {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  flex-wrap: wrap;
  justify-content: center;
}
.star { font-size: 15px; line-height: 1; }
.star.filled { color: #e8a023; }
.star.empty  { color: #d8d0c4; }
.star-num { margin-left: 4px; font-size: 13px; font-weight: 700; color: #22332e; }

/* ── Badges ── */
.best-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
  background: #e6f4ed;
  color: #2e7d5a;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
  white-space: nowrap;
}

.avail-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.avail-likely     { background: #e6f4ed; color: #2e7d5a; }
.avail-potential  { background: #fef9e2; color: #a87c00; }
.avail-constrained{ background: #fef0e2; color: #b85c00; }
.avail-high       { background: #fdecea; color: #c0392b; }
.avail-none       { background: #f0f0f0; color: #888; }
.avail-default    { background: #f0f0f0; color: #555; }

.met-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
  white-space: nowrap;
}
.badge-met   { background: #e6f4ed; color: #2e7d5a; }
.badge-unmet { background: #fdecea; color: #c0392b; }

.compliance-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.compliance-ok     { background: #e6f4ed; color: #2e7d5a; }
.compliance-action { background: #fef3e2; color: #c07a40; }

/* ── Footer ── */
tfoot tr td {
  border-top: 1px solid #e8e2d8;
}

.footer-cell {
  padding: 18px 20px;
}

.view-btn {
  width: 100%;
  background: #3d6b59;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 11px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.view-btn:hover { background: #2e5244; }

/* ── Search slot in thead ── */
.search-slot-cell {
  vertical-align: top;
}

.facility-search-slot {
  padding: 20px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 220px;
}

.slot-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 0 8px;
  color: #b0bdb8;
  font-size: 13px;
}

.slot-search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.slot-search-input {
  width: 100%;
  padding: 9px 12px 9px 34px;
  border: 1px solid #ccc7be;
  border-radius: 8px;
  font-size: 13px;
  color: #22332e;
  background: #faf8f4;
  outline: none;
  box-sizing: border-box;
}
.slot-search-input:focus { border-color: #3d6b59; background: #fff; }

.search-icon {
  position: absolute;
  left: 10px;
  color: #8a9e96;
  pointer-events: none;
}

.search-spinner {
  position: absolute;
  right: 10px;
  width: 14px;
  height: 14px;
  border: 2px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.slot-results {
  border: 1px solid #ddd5ca;
  border-radius: 8px;
  overflow: hidden;
  max-height: 220px;
  overflow-y: auto;
}

.slot-result-item {
  padding: 10px 12px;
  cursor: pointer;
  border-bottom: 1px solid #ede8e0;
}
.slot-result-item:last-child { border-bottom: none; }
.slot-result-item:hover { background: #f3f0ea; }

.slot-result-name {
  font-size: 13px;
  font-weight: 600;
  color: #22332e;
}

.slot-result-meta {
  font-size: 11px;
  color: #8a9e96;
  margin-top: 2px;
}

/* ── Search add section ── */
.search-add-wrap {
  margin-top: 32px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 14px;
  padding: 28px 32px;
}

.search-add-wrap.inline {
  margin-top: 20px;
}

.search-add-title {
  font-size: 15px;
  font-weight: 600;
  color: #22332e;
  margin: 0 0 14px;
}

.search-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: #8a9e96;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 11px 14px 11px 40px;
  border: 1px solid #ccc7be;
  border-radius: 10px;
  font-size: 14px;
  color: #22332e;
  background: #faf8f4;
  outline: none;
  box-sizing: border-box;
}
.search-input:focus { border-color: #3d6b59; background: #fff; }

.search-spinner {
  position: absolute;
  right: 14px;
  width: 16px;
  height: 16px;
  border: 2px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.search-results {
  margin-top: 8px;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  overflow: hidden;
}

.search-result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  gap: 12px;
  border-bottom: 1px solid #ede8e0;
  background: #fff;
}
.search-result-item:last-child { border-bottom: none; }
.search-result-item:hover { background: #faf8f4; }

.result-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.result-name {
  font-size: 14px;
  font-weight: 600;
  color: #22332e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-meta {
  font-size: 12px;
  color: #8a9e96;
}

.result-add-btn {
  flex-shrink: 0;
  padding: 6px 16px;
  border-radius: 999px;
  border: 1px solid #3d6b59;
  background: transparent;
  color: #3d6b59;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.result-add-btn:hover:not(:disabled) { background: #3d6b59; color: #fff; }
.result-add-btn.added { background: #e6f4ed; border-color: #a8d4bc; color: #2e7d5a; cursor: default; }
.result-add-btn:disabled:not(.added) { opacity: 0.4; cursor: not-allowed; }

.search-empty {
  margin-top: 10px;
  font-size: 13px;
  color: #8a9e96;
}

@media (max-width: 768px) {
  .compare-container { padding: 90px 16px 60px; }
  col.col-label { width: 130px; }
  .label-cell { padding: 10px 12px; font-size: 12px; }
  .data-cell { padding: 10px 12px; font-size: 13px; }
  .search-add-wrap { padding: 20px 16px; }
}
</style>
