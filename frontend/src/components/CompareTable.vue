<template>
  <div class="compare-content-frame">
    <!-- Page header -->
    <div class="compare-header">
      <div class="compare-header-left">
        <h1 class="compare-title">Compare facilities</h1>
        <p class="compare-subtitle">Side-by-side view of quality, staffing, compliance and more.</p>
      </div>
      <div class="compare-header-actions">
        <button class="action-btn-outline" @click="$emit('go-back')">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          Back to search
        </button>
        <button class="action-btn-outline" @click="$emit('clear-all')">Clear all</button>
      </div>
    </div>

    <div v-if="!isFull" class="add-third-row">
      <button class="add-third-btn" @click="showAddPanel = !showAddPanel">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Add a 3rd facility
      </button>
    </div>

    <!-- Add the optional third facility without leaving compare mode -->
    <div v-if="showAddPanel && !isFull" class="table-add-panel">
      <div class="table-add-copy">
        <span class="table-add-kicker">Facility {{ nextFacilityNumber }}</span>
        <strong>Add another facility</strong>
      </div>
      <div class="table-add-search">
        <div class="slot-search-wrap">
          <svg class="slot-search-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <input
            v-model="slots[activeAddSlot].query"
            class="slot-search-input"
            :placeholder="'Search facility ' + nextFacilityNumber + '…'"
            @input="$emit('slot-search', activeAddSlot)"
          />
          <div v-if="slots[activeAddSlot].loading" class="slot-spinner"></div>
        </div>

        <div v-if="slots[activeAddSlot].results.length > 0" class="slot-dropdown table-add-dropdown">
          <div
            v-for="r in slots[activeAddSlot].results"
            :key="r.id"
            class="slot-dropdown-item"
            @click="showAddPanel = false; $emit('add-from-add-panel', r)"
          >
            <div class="dropdown-icon">
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="6" width="18" height="15" rx="2"/>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </div>
            <div class="dropdown-info">
              <div class="dropdown-name">{{ r.name }}</div>
              <div class="dropdown-meta">
                <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg>
                {{ r.suburb }}, {{ r.state }}
              </div>
            </div>
            <button class="dropdown-add-btn" @click.stop="showAddPanel = false; $emit('add-from-add-panel', r)">+</button>
          </div>
        </div>
        <p v-else-if="slots[activeAddSlot].query && !slots[activeAddSlot].loading" class="slot-no-results">No results found.</p>
      </div>
    </div>

    <!-- Table -->
    <div class="compare-table-wrap">
      <table class="compare-table">
      <colgroup>
        <col class="col-label" />
        <col v-for="(f, i) in facilities" :key="i" :style="{ width: facilityColWidth }" />
      </colgroup>

      <thead>
        <tr class="facility-header-row">
          <th class="label-cell"><span class="facility-label-head">FACILITY</span></th>
          <th v-for="f in facilities" :key="f.id" class="facility-cell">
            <div class="facility-card-head">
              <button class="remove-btn" @click="$emit('remove-facility', f.id)" aria-label="Remove">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
              <img :src="f.image" :alt="f.name" class="facility-thumb" />
              <div class="facility-name">{{ f.name }}</div>
              <div class="facility-location">{{ f.suburb }}, {{ f.state }} {{ f.postcode }}</div>
            </div>
          </th>
        </tr>
      </thead>

      <tbody>
        <tr class="compare-section-row">
          <td :colspan="sectionColspan">
            <button class="compare-section-toggle" type="button" @click="toggleCompareSection('overview')">
              <span class="compare-section-icon" :class="{ open: isSectionOpen('overview') }"></span>
              <span>Overview</span>
            </button>
          </td>
        </tr>
        <tr v-if="!isSectionOpen('overview')" class="compare-summary-row">
          <td class="label-cell summary-label-cell">Summary</td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div class="section-summary">{{ sectionSummary('overview', f) }}</div>
          </td>
        </tr>

        <!-- Care type -->
        <tr v-if="isSectionOpen('overview')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Care type</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.careType">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.careType }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span class="value-text">{{ f.careType || 'N/A' }}</span>
          </td>
        </tr>

        <!-- Total beds -->
        <tr v-if="isSectionOpen('overview')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Total beds</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.totalBeds">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.totalBeds }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span class="value-text">{{ f.totalBeds ?? 'N/A' }}</span>
          </td>
        </tr>

        <!-- Availability (inside Overview) -->
        <tr v-if="isSectionOpen('overview')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Availability</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.availability">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.availability }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span class="value-text" :class="availabilityClass(f.bedAvailability)">{{ f.bedAvailability || 'Unknown' }}</span>
          </td>
        </tr>

        <tr class="compare-section-row">
          <td :colspan="sectionColspan">
            <button class="compare-section-toggle" type="button" @click="toggleCompareSection('qualityRatings')">
              <span class="compare-section-icon" :class="{ open: isSectionOpen('qualityRatings') }"></span>
              <span>Quality Ratings</span>
            </button>
          </td>
        </tr>
        <tr v-if="!isSectionOpen('qualityRatings')" class="compare-summary-row">
          <td class="label-cell summary-label-cell">Summary</td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div class="section-summary">
              {{ sectionSummary('qualityRatings', f) }}
              <span v-if="isHighest(f, 'overallStarRating')" class="summary-badge">Highest</span>
            </div>
          </td>
        </tr>

        <!-- Overall rating -->
        <tr v-if="isSectionOpen('qualityRatings')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Overall rating</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.overallRating">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.overallRating }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('qualityRatings')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Resident experience rating</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.residentExperienceRating">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.residentExperienceRating }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('qualityRatings')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Staffing rating</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.staffingRating">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.staffingRating }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('qualityRatings')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Compliance rating</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.complianceRating">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.complianceRating }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('qualityRatings')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Quality measures rating</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.qualityMeasuresRating">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.qualityMeasuresRating }}</span>
              </button>
            </span>
          </td>
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

        <tr class="compare-section-row">
          <td :colspan="sectionColspan">
            <button class="compare-section-toggle" type="button" @click="toggleCompareSection('staffingCompliance')">
              <span class="compare-section-icon" :class="{ open: isSectionOpen('staffingCompliance') }"></span>
              <span>Staffing & Compliance</span>
            </button>
          </td>
        </tr>
        <tr v-if="!isSectionOpen('staffingCompliance')" class="compare-summary-row">
          <td class="label-cell summary-label-cell">Summary</td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div class="section-summary">{{ sectionSummary('staffingCompliance', f) }}</div>
          </td>
        </tr>

        <!-- RN care minutes -->
        <tr v-if="isSectionOpen('staffingCompliance')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>RN care minutes <span class="label-sub">(actual / target)</span></span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.rnCareMinutes">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.rnCareMinutes }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('staffingCompliance')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Total care minutes <span class="label-sub">(actual / target)</span></span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.totalCareMinutes">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.totalCareMinutes }}</span>
              </button>
            </span>
          </td>
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
        <tr v-if="isSectionOpen('staffingCompliance')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Compliance status</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.complianceStatus">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.complianceStatus }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span v-if="f.sRnCareMinutesActual != null" class="compliance-badge" :class="(f.rnMinutesMet && f.totalMinutesMet) ? 'compliance-ok' : 'compliance-action'">
              {{ (f.rnMinutesMet && f.totalMinutesMet) ? 'No issues' : 'Action taken' }}
            </span>
            <span v-else class="na-text">N/A</span>
          </td>
        </tr>

        <tr class="compare-section-row">
          <td :colspan="sectionColspan">
            <button class="compare-section-toggle" type="button" @click="toggleCompareSection('residentExperience')">
              <span class="compare-section-icon" :class="{ open: isSectionOpen('residentExperience') }"></span>
              <span>Resident Experience</span>
            </button>
          </td>
        </tr>
        <tr v-if="!isSectionOpen('residentExperience')" class="compare-summary-row">
          <td class="label-cell summary-label-cell">Summary</td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div class="section-summary">{{ sectionSummary('residentExperience', f) }}</div>
          </td>
        </tr>

        <!-- Resident scores -->
        <tr v-if="isSectionOpen('residentExperience')" v-for="rs in residentScoreRows" :key="rs.key" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>{{ rs.label }}</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo[rs.key]">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo[rs.key] }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div
              v-if="f[rs.key] != null"
              class="stars-row"
              :aria-label="`${rs.label} rating ${Number(f[rs.key]).toFixed(1)} out of 5`"
            >
              <span v-for="i in starsFor(f[rs.key]).full" :key="'f'+i" class="star filled">★</span>
              <span v-for="i in starsFor(f[rs.key]).empty" :key="'e'+i" class="star empty">★</span>
              <span class="star-num">{{ Number(f[rs.key]).toFixed(1) }}</span>
            </div>
            <span v-else class="na-text">N/A</span>
          </td>
        </tr>

        <tr class="compare-section-row">
          <td :colspan="sectionColspan">
            <button class="compare-section-toggle" type="button" @click="toggleCompareSection('providerFunding')">
              <span class="compare-section-icon" :class="{ open: isSectionOpen('providerFunding') }"></span>
              <span>Provider & Funding</span>
            </button>
          </td>
        </tr>
        <tr v-if="!isSectionOpen('providerFunding')" class="compare-summary-row">
          <td class="label-cell summary-label-cell">Summary</td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <div class="section-summary">{{ sectionSummary('providerFunding', f) }}</div>
          </td>
        </tr>

        <!-- Government funding -->
        <tr v-if="isSectionOpen('providerFunding')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Government funding</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.governmentFunding">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.governmentFunding }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span class="value-text">{{ formatFunding(f.governmentFunding) }}</span>
          </td>
        </tr>

        <!-- Provider -->
        <tr v-if="isSectionOpen('providerFunding')" class="compare-row">
          <td class="label-cell">
            <span class="label-with-help">
              <span>Provider</span>
              <button class="info-dot" type="button" :aria-label="fieldInfo.provider">
                i
                <span class="info-tooltip" role="tooltip">{{ fieldInfo.provider }}</span>
              </button>
            </span>
          </td>
          <td v-for="f in facilities" :key="f.id" class="data-cell">
            <span class="value-text">{{ f.provider || 'N/A' }}</span>
          </td>
        </tr>
      </tbody>

      <tfoot>
        <tr>
          <td class="label-cell"></td>
          <td v-for="f in facilities" :key="f.id" class="data-cell footer-cell">
            <button class="view-btn" @click="$emit('go-to-detail', f.id)">View full details</button>
          </td>
        </tr>
      </tfoot>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  facilities: { type: Array, required: true },
  slots: { type: Array, required: true },
  isFull: { type: Boolean, required: true }
})
defineEmits(['remove-facility', 'go-back', 'clear-all', 'go-to-detail', 'add-from-add-panel', 'slot-search'])

const facilityColWidth = computed(() =>
  `calc((100% - 160px) / ${props.facilities.length || 1})`
)
const sectionColspan = computed(() => props.facilities.length + 1)
const activeAddSlot = computed(() => Math.min(props.facilities.length, props.slots.length - 1))
const nextFacilityNumber = computed(() => props.facilities.length + 1)

const showAddPanel = ref(false)

const collapsedSections = ref(new Set([
  'overview',
  'qualityRatings',
  'staffingCompliance',
  'residentExperience',
  'providerFunding'
]))

const fieldInfo = {
  careType: 'The type of aged care service offered, such as residential care.',
  availability: 'Bed availability estimation based on current occupancy data. Indicates how likely a place is available at this facility.',
  overallRating: 'The overall star rating summarising quality, care, staffing and compliance signals.',
  residentExperienceRating: 'A rating based on resident experience feedback, including how residents feel about daily life and care.',
  staffingRating: 'A star rating that reflects staffing performance and care minute information.',
  complianceRating: 'A rating that reflects compliance history and whether regulatory concerns have been identified.',
  qualityMeasuresRating: 'A rating based on reported quality measures and care outcome indicators.',
  totalBeds: 'The total number of approved aged care places or beds available at the facility.',
  rnCareMinutes: 'Registered nurse care minutes delivered per resident per day compared with the target.',
  totalCareMinutes: 'Total direct care minutes delivered per resident per day compared with the target.',
  complianceStatus: 'A summary of whether staffing targets are met or whether action may be needed.',
  reFoodScore: 'Resident feedback score for food quality and meal experience.',
  reSafetyScore: 'Resident feedback score for feeling safe at the facility.',
  reRespectScore: 'Resident feedback score for being treated with respect.',
  reCaringScore: 'Resident feedback score for whether staff are caring and supportive.',
  reHomeScore: 'Resident feedback score for whether the facility feels like home.',
  governmentFunding: 'The amount of government funding reported for the facility.',
  provider: 'The organisation responsible for operating the facility.'
}

const residentScoreRows = [
  { key: 'reFoodScore',    label: 'Resident - Food' },
  { key: 'reSafetyScore',  label: 'Resident - Safety' },
  { key: 'reRespectScore', label: 'Resident - Respect' },
  { key: 'reCaringScore',  label: 'Resident - Caring' },
  { key: 'reHomeScore',    label: 'Resident - Feeling at Home' },
]

function isSectionOpen(key) {
  return !collapsedSections.value.has(key)
}

function toggleCompareSection(key) {
  const next = new Set(collapsedSections.value)
  next.has(key) ? next.delete(key) : next.add(key)
  collapsedSections.value = next
}

function availabilityClass(val) {
  if (val === 'Likely Available') return 'avail-likely'
  if (val === 'Potentially Available') return 'avail-potential'
  if (val === 'Constrained by Market' || val === 'Constrained by Size') return 'avail-constrained'
  if (val === 'Highly Constrained') return 'avail-highly-constrained'
  if (val === 'Does Not Provide This Service') return 'avail-none'
  return ''
}

function starsFor(val) {
  const full = Math.max(0, Math.min(5, Math.round(val ?? 0)))
  return { full, empty: 5 - full }
}

function formatRating(val) {
  if (val == null || Number.isNaN(Number(val))) return 'No rating'
  return `${Number(val).toFixed(1)} stars`
}

function residentAverage(facility) {
  const vals = residentScoreRows
    .map(row => facility[row.key])
    .filter(val => val != null && !Number.isNaN(Number(val)))
    .map(Number)
  if (!vals.length) return null
  return vals.reduce((sum, val) => sum + val, 0) / vals.length
}

function sectionSummary(sectionKey, facility) {
  if (sectionKey === 'overview') {
    const beds = facility.totalBeds != null ? `${facility.totalBeds} beds` : 'Beds unknown'
    return `${beds} · ${facility.bedAvailability || 'Availability unknown'}`
  }

  if (sectionKey === 'qualityRatings') {
    return `Overall ${formatRating(facility.overallStarRating)}`
  }

  if (sectionKey === 'staffingCompliance') {
    if (facility.sRnCareMinutesActual == null && facility.sTotalCareMinutesActual == null) return 'Staffing data unavailable'
    const rn = facility.rnMinutesMet ? 'RN met' : 'RN not met'
    const total = facility.totalMinutesMet ? 'Total met' : 'Total not met'
    return `${rn} · ${total}`
  }

  if (sectionKey === 'residentExperience') {
    const average = residentAverage(facility)
    return average == null ? 'Resident feedback unavailable' : `Average ${formatRating(average)}`
  }

  if (sectionKey === 'providerFunding') {
    return formatFunding(facility.governmentFunding)
  }

  return 'Summary unavailable'
}

function isHighest(facility, key) {
  if (props.facilities.length < 3) return false
  if (facility[key] == null) return false
  const vals = props.facilities.map(f => f[key] ?? -Infinity)
  const max = Math.max(...vals)
  return facility[key] === max
}

function formatFunding(val) {
  if (val == null || val === '') return 'N/A'
  return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 }).format(val)
}
</script>

<style scoped>
/* ── COMPARE TABLE HEADER ── */
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
  border-radius: 7px;
  padding: 4px 16px;
  font-size: 13px;
  font-weight: 500;
  color: #4a5e57;
  cursor: pointer;
  transition: background 0.15s;
}
.action-btn-outline:hover { background: #f0ece4; }

.add-third-row {
  display: flex;
  justify-content: flex-end;
  margin: -16px 0 16px;
  padding-right: 2px;
}

.add-third-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1.5px dashed #aeb9b3;
  background: transparent;
  border-radius: 999px;
  padding: 7px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #4a6659;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.add-third-btn:hover {
  background: #eef5ef;
  border-color: #4a6659;
  color: #2e5244;
}

.table-add-panel {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 16px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  padding: 14px 16px;
}

.table-add-copy {
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  color: #22332e;
}

.table-add-copy strong {
  font-size: 14px;
}

.table-add-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #3d6b59;
}

.table-add-search {
  flex: 1;
  min-width: 240px;
  position: relative;
}

.table-add-dropdown {
  position: absolute;
  left: 0;
  right: 0;
}

.table-add-dropdown .slot-dropdown-item {
  gap: 16px;
  padding: 14px 20px;
}

.table-add-dropdown .dropdown-info {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) minmax(160px, 0.65fr);
  align-items: center;
  gap: 20px;
}

.table-add-dropdown .dropdown-name {
  font-size: 14px;
  line-height: 1.25;
}

.table-add-dropdown .dropdown-meta {
  margin-top: 0;
  justify-content: flex-start;
  text-transform: uppercase;
  white-space: nowrap;
}

.table-add-dropdown .dropdown-add-btn {
  width: 30px;
  height: 30px;
  font-size: 20px;
}

/* ── Section filter chips ── */
.compare-content-frame {
  width: min(100%, 1160px);
  margin: 0 auto;
}

/* ── Table ── */
.compare-table-wrap {
  overflow-x: auto;
  padding: 0;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #ece9e3;
  border-radius: 14px;
  overflow: hidden;
  table-layout: fixed;
}

col.col-label { width: 160px; }

.facility-header-row th {
  background: #fff;
  padding: 0;
  vertical-align: middle;
  border-bottom: 1px solid #ece9e3;
}

.facility-header-row th.label-cell {
  background: #f7f7f6;
}

.label-cell {
  padding: 0 14px;
  font-size: 14px;
  font-weight: 400;
  color: #6f6f6f;
  text-align: left;
  vertical-align: middle;
  border-right: 1px solid #ece9e3;
  background: #f7f7f6;
  line-height: 1.4;
  position: relative;
}

.facility-label-head {
  font-size: 14px;
  font-weight: 500;
  color: #6f6f6f;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding-left: 12px;
}

.label-sub {
  font-size: 11px;
  font-weight: 400;
  color: #7f7f7f;
}

.label-with-help {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  width: 100%;
}

.info-dot {
  width: 15px;
  height: 15px;
  border: 1.5px solid #7b817e;
  border-radius: 50%;
  background: transparent;
  color: #6f7471;
  font-size: 10px;
  font-weight: 700;
  line-height: 1;
  padding: 0;
  cursor: help;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  position: relative;
}

.info-tooltip {
  position: absolute;
  left: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
  width: 230px;
  padding: 9px 11px;
  border-radius: 8px;
  background: #22332e;
  color: #fff;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.35;
  text-align: left;
  box-shadow: 0 8px 22px rgba(31, 45, 42, 0.18);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  z-index: 30;
}

.info-tooltip::before {
  content: "";
  position: absolute;
  left: -5px;
  top: 50%;
  width: 10px;
  height: 10px;
  background: #22332e;
  transform: translateY(-50%) rotate(45deg);
}

.info-dot:hover .info-tooltip,
.info-dot:focus-visible .info-tooltip {
  opacity: 1;
  visibility: visible;
}

.facility-cell {
  padding: 0;
  text-align: center;
  border-right: 1px solid #ece9e3;
  vertical-align: top;
}
.facility-cell:last-child { border-right: none; }

.facility-card-head {
  position: relative;
  padding: 20px 20px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
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
  flex: 0 0 140px;
  object-fit: cover;
  border-radius: 10px;
}

.facility-name {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
  text-align: center;
  line-height: 1.3;
  height: calc(2 * 1.3em);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.facility-location {
  font-size: 12px;
  color: #a0a8a4;
  text-align: center;
  min-height: 0;
  margin-top: 0;
}

/* ── Data rows ── */
.compare-section-row td {
  padding: 0;
  background: #fff;
  border-bottom: 1px solid #ece9e3;
}

.compare-section-toggle {
  width: 100%;
  min-height: 46px;
  border: none;
  background: transparent;
  color: #22332e;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  padding: 0 18px;
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  text-align: left;
}

.compare-section-toggle:hover {
  background: #f7f7f6;
}

.compare-section-icon {
  width: 8px;
  height: 8px;
  flex: 0 0 auto;
  border-right: 2px solid #4f665e;
  border-bottom: 2px solid #4f665e;
  transform: rotate(-45deg);
  transition: transform 0.16s ease;
  margin-bottom: 1px;
}

.compare-section-icon.open {
  transform: rotate(45deg);
}

.compare-row { height: 62px; }

.compare-row td {
  height: 62px;
  border-bottom: 1px solid #ece9e3;
  vertical-align: middle;
}

.compare-row:last-child td { border-bottom: none; }

.compare-summary-row td {
  height: 48px;
  border-bottom: 1px solid #ece9e3;
  background: #fbfaf7;
  vertical-align: middle;
}

.summary-label-cell {
  color: #7f8d87;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.section-summary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  max-width: 100%;
  color: #33443e;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.35;
}

.summary-badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 2px 8px;
  background: #e6f4ed;
  color: #2e7d5a;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.data-cell {
  padding: 0 20px;
  text-align: center;
  border-right: 1px solid #ece9e3;
  font-size: 14px;
  vertical-align: middle;
  position: relative;
}
.data-cell:last-child { border-right: none; }

.value-text { font-weight: 600; color: #22332e; }

.avail-likely              { color: #4f7a62; }
.avail-potential           { color: #c9a200; }
.avail-constrained         { color: #d9822b; }
.avail-highly-constrained  { color: #c53b2c; }
.avail-none                { color: #9e9e9e; }
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
  white-space: nowrap;
  margin-top: 4px;
}

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
  border-top: 1px solid #ece9e3;
}

.footer-cell { padding: 18px 20px; }

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

/* ── Shared dropdown styles (also used in add panel) ── */
.slot-search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.slot-search-icon {
  position: absolute;
  left: 20px;
  color: #8a9e96;
  pointer-events: none;
  z-index: 1;
}

.slot-search-input {
  width: 100%;
  height: 52px;
  padding: 0 18px 0 54px;
  border: 1px solid #e1ddd5;
  border-radius: 999px;
  font-size: 14px;
  color: #22332e;
  background: #fff;
  outline: none;
  box-sizing: border-box;
  box-shadow: 0 4px 14px rgba(31, 45, 42, 0.06);
}
.slot-search-input:focus {
  border-color: #3d6b59;
  box-shadow: 0 0 0 3px rgba(61, 107, 89, 0.12), 0 6px 18px rgba(31, 45, 42, 0.08);
}

.slot-spinner {
  position: absolute;
  right: 20px;
  width: 14px;
  height: 14px;
  border: 2px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.slot-dropdown {
  margin-top: 10px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  overflow: hidden;
  max-height: 260px;
  overflow-y: auto;
  box-shadow: 0 10px 24px rgba(31, 45, 42, 0.14);
  position: relative;
  z-index: 10;
  text-align: left;
}

.slot-dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  cursor: pointer;
  border-bottom: 1px solid #ede8e0;
  transition: background 0.1s;
}
.slot-dropdown-item:last-child { border-bottom: none; }
.slot-dropdown-item:hover { background: #f3f0ea; }

.dropdown-icon {
  width: 36px;
  height: 36px;
  background: #eef5ef;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3d6b59;
  flex-shrink: 0;
}

.dropdown-info {
  flex: 1;
  min-width: 0;
}

.dropdown-name {
  font-size: 13px;
  font-weight: 700;
  color: #22332e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-meta {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 10.5px;
  color: #8a9e96;
  margin-top: 2px;
}

.dropdown-add-btn {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1.5px solid #3d6b59;
  background: transparent;
  color: #3d6b59;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.1s, color 0.1s;
}
.dropdown-add-btn:hover { background: #3d6b59; color: #fff; }

.slot-no-results {
  font-size: 12px;
  color: #a0a8a4;
  margin: 8px 0 0;
  text-align: center;
}

/* ── Tablet (769px – 1100px) ── */
@media (min-width: 769px) and (max-width: 1100px) {
  /* Stack header so action buttons never overflow */
  .compare-header { flex-direction: column; align-items: flex-start; gap: 10px; }
  .compare-header-actions { flex-wrap: wrap; gap: 8px; }
  .compare-title { font-size: 22px; }
  .compare-subtitle { font-size: 13px; }

  /* Narrow label column frees space for 3 facility cols */
  col.col-label { width: 100px; }
  .label-cell { padding: 8px 8px; font-size: 11px; }
  .label-sub { font-size: 9.5px; }
  .facility-label-head { font-size: 11px; padding-left: 6px; letter-spacing: 0.04em; }

  /* Tighter data cells */
  .data-cell { padding: 6px 8px; font-size: 12px; }

  /* Facility header card */
  .facility-card-head { padding: 10px 10px 4px; gap: 3px; }
  .facility-thumb { height: 100px; }
  .facility-name { font-size: 11px; }
  .facility-location { font-size: 10px; }
  .remove-btn { top: 8px; right: 8px; width: 22px; height: 22px; }

  /* Allow rows to breathe vertically (content may wrap on narrow cols) */
  .compare-row { height: auto; }
  .compare-row td { height: auto; min-height: 50px; padding-top: 6px; padding-bottom: 6px; }

  /* Stars */
  .star { font-size: 12px; }
  .star-num { font-size: 11px; }

  /* best-badge: smaller on tablet */
  .best-badge { font-size: 10px; padding: 1px 6px; }

  /* met-badge: block so it wraps under the minutes text cleanly */
  .met-badge {
    display: inline-flex;
    margin-left: 0;
    margin-top: 3px;
    font-size: 10px;
    padding: 1px 6px;
  }
  /* Wrap the care-minutes cell content vertically */
  .data-cell .value-text + .met-badge { display: block; }

  .compliance-badge { font-size: 11px; padding: 3px 8px; }

  /* Footer buttons */
  .footer-cell { padding: 12px 8px; }
  .view-btn { font-size: 12px; padding: 8px 8px; }

  .compare-section-toggle { min-height: 42px; font-size: 13px; padding: 0 14px; }
}

@media (max-width: 768px) {
  /* Add-third panel */
  .add-third-row { justify-content: flex-start; margin: -8px 0 14px; }
  .table-add-panel { flex-direction: column; }
  .table-add-copy,
  .table-add-search { width: 100%; min-width: 0; }
  .table-add-dropdown .dropdown-info { display: block; }
  .table-add-dropdown .dropdown-meta { margin-top: 2px; white-space: normal; }

  /* Compare header */
  .compare-header { flex-direction: column; align-items: flex-start; gap: 10px; }
  .compare-header-actions { flex-wrap: wrap; gap: 8px; }

  /* Table */
  col.col-label { width: 90px; }
  .label-cell { padding: 8px 6px; font-size: 10px; }
  .facility-label-head { font-size: 10px; padding-left: 4px; }
  .data-cell { padding: 6px 6px; font-size: 11px; }
  .facility-card-head { padding: 8px 8px 4px; gap: 2px; }
  .facility-thumb { height: 80px; }
  .facility-name { font-size: 10px; }
  .facility-location { font-size: 9px; }
  .remove-btn { top: 6px; right: 6px; width: 20px; height: 20px; }

  /* Allow rows to auto-size so wrapped content isn't clipped */
  .compare-row { height: auto; }
  .compare-row td { height: auto; min-height: 46px; padding-top: 6px; padding-bottom: 6px; }

  /* Stars */
  .star { font-size: 11px; }
  .star-num { font-size: 10px; }
  .best-badge { font-size: 10px; padding: 1px 6px; margin-top: 2px; }

  /* Met badge on its own line */
  .data-cell .value-text + .met-badge { display: block; margin-top: 2px; }
  .met-badge { font-size: 10px; padding: 1px 6px; margin-left: 0; }

  .compliance-badge { font-size: 10px; padding: 2px 7px; }
  .footer-cell { padding: 10px 6px; }
  .view-btn { font-size: 11px; padding: 7px 6px; }

  .compare-section-toggle { min-height: 40px; font-size: 12px; padding: 0 10px; }
}
</style>
