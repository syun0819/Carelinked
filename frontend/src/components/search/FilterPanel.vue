<template>
  <aside class="filters-panel">
    <div class="filters-header" @click="toggleFilters">
      <h2>Filters</h2>
      <div class="filters-header-right">
        <button class="reset-btn" @click.stop="resetFilters">Reset all</button>
        <span class="toggle-icon">{{ filtersOpen ? '▲' : '▼' }}</span>
      </div>
    </div>

    <div class="filters-body" :class="{ collapsed: !filtersOpen }">
      <div class="filter-section">
        <button class="section-toggle" :class="{ active: sectionOpen.careType }" type="button" @click="toggleSection('careType')">
          <svg class="filter-section-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 7h16"/>
            <path d="M7 12h10"/>
            <path d="M10 17h4"/>
          </svg>
          <span class="filter-title">Care type</span>
          <span class="section-toggle-icon" :class="{ open: sectionOpen.careType }"></span>
        </button>
        <label
          v-for="item in careTypeOptions"
          :key="item.value"
          v-show="sectionOpen.careType"
          class="filter-option"
          :class="{ selected: localCareTypes.includes(item.value) }"
        >
          <input
            type="checkbox"
            :checked="localCareTypes.includes(item.value)"
            @change="toggleCareType(item.value)"
          />
          <span class="custom-checkbox">
            <span v-if="localCareTypes.includes(item.value)">✓</span>
          </span>
          <span class="option-text">{{ item.label }}</span>
          <span
            class="care-info"
            tabindex="0"
            role="button"
            aria-label="Care type information"
            @click.stop.prevent
          >
            i
            <span class="care-tooltip">{{ getCareTypeDescription(item.value) }}</span>
          </span>
        </label>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <div class="distance-header">
          <button class="section-toggle" :class="{ active: sectionOpen.distance }" type="button" @click="toggleSection('distance')">
            <svg class="filter-section-icon" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z"/>
              <circle cx="12" cy="9" r="2.5"/>
            </svg>
            <span class="filter-title">Distance filter</span>
            <span class="section-toggle-icon" :class="{ open: sectionOpen.distance }"></span>
          </button>
        </div>
        <template v-if="sectionOpen.distance">
          <div class="distance-top">
            <span>Within</span>
            <strong>{{ localDistance }} km</strong>
          </div>
          <div class="range-wrap">
            <input
              class="distance-range"
              type="range"
              :min="minDistance"
              :max="maxDistance"
              :value="localDistance"
              :style="rangeStyle"
              @input="localDistance = Number($event.target.value)"
            />
          </div>
          <p v-if="distanceWarning" class="distance-warning-hint">{{ distanceWarning }}</p>
        </template>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <button class="section-toggle" :class="{ active: sectionOpen.locationType }" type="button" @click="toggleSection('locationType')">
          <svg class="filter-section-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5Z"/>
            <path d="M9 21V12h6v9"/>
          </svg>
          <span class="filter-title">Location type</span>
          <span class="section-toggle-icon" :class="{ open: sectionOpen.locationType }"></span>
        </button>
        <select v-show="sectionOpen.locationType" v-model="localRemoteness" class="filter-select">
          <option value="">All</option>
          <option value="Major Cities">Major Cities</option>
          <option value="Inner Regional">Inner Regional</option>
          <option value="Outer Regional">Outer Regional</option>
          <option value="Remote">Remote</option>
          <option value="Very Remote">Very Remote</option>
        </select>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <button class="section-toggle" :class="{ active: sectionOpen.minBeds }" type="button" @click="toggleSection('minBeds')">
          <svg class="filter-section-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 20h16"/>
            <path d="M7 20V8h10v12"/>
            <path d="M9 11h2"/>
            <path d="M13 11h2"/>
            <path d="M9 15h2"/>
            <path d="M13 15h2"/>
          </svg>
          <span class="filter-title">Min beds</span>
          <span class="section-toggle-icon" :class="{ open: sectionOpen.minBeds }"></span>
        </button>
        <input
          v-show="sectionOpen.minBeds"
          type="number"
          v-model="localMinBeds"
          class="filter-input"
          :class="{ 'input-error': sectionOpen.minBeds && (minBedsError || bedsRangeError) }"
          placeholder="e.g. 20"
          min="0"
          @input="onMinBedsInput"
        />
        <p v-if="sectionOpen.minBeds && minBedsError" class="filter-field-error">{{ minBedsError }}</p>
        <p v-else-if="sectionOpen.minBeds && minBedsHint" class="filter-field-hint">Maximum 3 digits allowed</p>
        <p v-else-if="sectionOpen.minBeds && bedsRangeError" class="filter-field-error">{{ bedsRangeError }}</p>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <button class="section-toggle" :class="{ active: sectionOpen.maxBeds }" type="button" @click="toggleSection('maxBeds')">
          <svg class="filter-section-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 20h16"/>
            <path d="M6 20V5h12v15"/>
            <path d="M9 8h2"/>
            <path d="M13 8h2"/>
            <path d="M9 12h2"/>
            <path d="M13 12h2"/>
            <path d="M9 16h2"/>
            <path d="M13 16h2"/>
          </svg>
          <span class="filter-title">Max beds</span>
          <span class="section-toggle-icon" :class="{ open: sectionOpen.maxBeds }"></span>
        </button>
        <input
          v-show="sectionOpen.maxBeds"
          type="number"
          v-model="localMaxBeds"
          class="filter-input"
          :class="{ 'input-error': sectionOpen.maxBeds && (maxBedsError || bedsRangeError) }"
          placeholder="e.g. 100"
          min="0"
          @input="onMaxBedsInput"
        />
        <p v-if="sectionOpen.maxBeds && maxBedsError" class="filter-field-error">{{ maxBedsError }}</p>
        <p v-else-if="sectionOpen.maxBeds && maxBedsHint" class="filter-field-hint">Maximum 3 digits allowed</p>
        <p v-else-if="sectionOpen.maxBeds && bedsRangeError" class="filter-field-error">{{ bedsRangeError }}</p>
      </div>

      <button
        class="apply-btn"
        :disabled="!!minBedsError || !!maxBedsError || !!bedsRangeError"
        @click="applyFilters"
      >
        Apply filters
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed, watch, ref } from 'vue'

const props = defineProps({
  selectedCareTypes: { type: Array, default: () => [] },
  distance: { type: Number, default: 10 },
  distanceFilterEnabled: { type: Boolean, default: false },
  distanceWarning: { type: String, default: '' },
  careTypeOptions: { type: Array, default: () => [] },
  minDistance: { type: Number, default: 1 },
  maxDistance: { type: Number, default: 20 },
  selectedRemoteness: { type: String, default: '' },
  minBeds: { type: Number, default: null },
  maxBeds: { type: Number, default: null }
})

const emit = defineEmits([
  'apply',
  'reset'
])

const localCareTypes = ref([...props.selectedCareTypes])
const minBedsHint = ref(false)
const maxBedsHint = ref(false)
let minBedsHintTimer = null
let maxBedsHintTimer = null

function onMinBedsInput(event) {
  if (event.target.validity.badInput) {
    minBedsError.value = 'Please enter a valid number'
    return
  }
  minBedsError.value = ''
  const raw = event.target.value
  if (raw.length > 3) {
    event.target.value = raw.slice(0, 3)
    localMinBeds.value = Number(raw.slice(0, 3))
    minBedsHint.value = true
    clearTimeout(minBedsHintTimer)
    minBedsHintTimer = setTimeout(() => { minBedsHint.value = false }, 2000)
  }
}

function onMaxBedsInput(event) {
  if (event.target.validity.badInput) {
    maxBedsError.value = 'Please enter a valid number'
    return
  }
  maxBedsError.value = ''
  const raw = event.target.value
  if (raw.length > 3) {
    event.target.value = raw.slice(0, 3)
    localMaxBeds.value = Number(raw.slice(0, 3))
    maxBedsHint.value = true
    clearTimeout(maxBedsHintTimer)
    maxBedsHintTimer = setTimeout(() => { maxBedsHint.value = false }, 2000)
  }
}
const localRemoteness = ref(props.selectedRemoteness || '')
const localMinBeds = ref(props.minBeds)
const localMaxBeds = ref(props.maxBeds)
const minBedsError = ref('')
const maxBedsError = ref('')

const bedsRangeError = computed(() => {
  const min = toNullableNumber(localMinBeds.value)
  const max = toNullableNumber(localMaxBeds.value)
  if (min !== null && max !== null && min > max) {
    return 'Min beds cannot be greater than max beds'
  }
  return ''
})
const localDistance = ref(props.distance)
const localDistanceFilterEnabled = ref(props.distanceFilterEnabled)
const filtersOpen = ref(window.innerWidth > 768)
const sectionOpen = ref({
  careType: false,
  distance: false,
  locationType: false,
  minBeds: false,
  maxBeds: false
})

const careTypeDescriptions = {
  Residential:
    'Permanent live-in aged care for older people who can no longer live independently. Includes accommodation, meals, personal care, and 24/7 nursing support.',
  'Transition Care':
    'Short-term care after a hospital stay to help older people recover, regain confidence, and decide whether they can return home or need longer-term care.',
  'Short-Term Restorative Care (STRC)':
    'Time-limited restorative care focused on improving independence and daily function so older people can continue living at home.',
  'Multi-Purpose Service':
    'Flexible care services for regional and remote communities where aged care, health care, and community support may be delivered together.',
  'National Aboriginal and Torres Strait Islander Aged Care Program':
    'Culturally appropriate aged care for Aboriginal and Torres Strait Islander older people, often delivered by community-based providers.'
}

function toggleFilters() {
  if (window.innerWidth <= 768) {
    filtersOpen.value = !filtersOpen.value
  }
}

function toggleSection(section) {
  const nextValue = !sectionOpen.value[section]
  sectionOpen.value[section] = nextValue

  if (section === 'distance') {
    localDistanceFilterEnabled.value = nextValue
  }
}

watch(() => props.selectedCareTypes, (val) => { localCareTypes.value = [...val] })
watch(() => props.selectedRemoteness, (val) => { localRemoteness.value = val || '' })
watch(() => props.minBeds, (val) => { localMinBeds.value = val })
watch(() => props.maxBeds, (val) => { localMaxBeds.value = val })
watch(() => props.distance, (val) => { localDistance.value = val })
watch(() => props.distanceFilterEnabled, (val) => { localDistanceFilterEnabled.value = val })

function toggleCareType(value) {
  localCareTypes.value = localCareTypes.value.includes(value)
    ? localCareTypes.value.filter(item => item !== value)
    : [...localCareTypes.value, value]
}

function closeFilterSections() {
  Object.keys(sectionOpen.value).forEach((section) => {
    sectionOpen.value[section] = false
  })
  localDistanceFilterEnabled.value = false
}

function resetFilters() {
  closeFilterSections()
  emit('reset')
}

function getCareTypeDescription(value) {
  return careTypeDescriptions[value] || 'Care services available under this care type.'
}

function toNullableNumber(value) {
  return value === '' || value == null ? null : Number(value)
}

function applyFilters() {
  emit('apply', {
    selectedCareTypes: [...localCareTypes.value],
    selectedRemoteness: localRemoteness.value,
    minBeds: toNullableNumber(localMinBeds.value),
    maxBeds: toNullableNumber(localMaxBeds.value),
    distance: localDistance.value,
    distanceFilterEnabled: localDistanceFilterEnabled.value
  })
}

const rangeStyle = computed(() => {
  const percentage =
    ((localDistance.value - props.minDistance) / (props.maxDistance - props.minDistance)) * 100
  return {
    background: `linear-gradient(to right, #4f7d6f 0%, #4f7d6f ${percentage}%, #dbd8d4 ${percentage}%, #dbd8d4 100%)`
  }
})
</script>

<style scoped>
.filters-panel {
  position: relative;
  z-index: 2000;
  background: #ffffff;
  border: 1px solid #ddd5ca;
  border-radius: 12px;
  padding: 6px;
  width: 100%;
  box-sizing: border-box;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 52px;
  margin-bottom: 0;
  padding: 8px 12px;
}

.filters-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #22332e;
  font-family: var(--font-display);
}

.filters-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-icon {
  display: none;
  font-size: 12px;
  color: #6a7d76;
}

.filters-body.collapsed {
  display: none;
}

.filters-body {
  padding: 0 0 10px;
}

.reset-btn {
  border: none;
  background: transparent;
  padding: 0;
  font-size: 14px;
  font-weight: 600;
  color: #667871;
  cursor: pointer;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 2px;
}

.filter-divider {
  display: none;
}

.filter-title {
  flex: 1;
  margin: 0;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 0;
  color: currentColor;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.section-toggle {
  width: 100%;
  border: none;
  background: transparent;
  padding: 11px 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-family: var(--font-sans);
  color: #667871;
  transition: background 0.15s, color 0.15s;
}

.section-toggle:hover {
  background: #f3f0ea;
}

.section-toggle.active {
  background: #3d6b59;
  color: #fff;
  font-weight: 600;
}

.filter-section-icon {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.section-toggle-icon {
  width: 9px;
  height: 9px;
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-right: 1.9px solid currentColor;
  border-bottom: 1.9px solid currentColor;
  transform: rotate(45deg);
  transition: transform 0.16s ease;
  opacity: 0.7;
}

.section-toggle-icon.open {
  transform: rotate(225deg);
}

.filter-option {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr) 20px;
  align-items: center;
  column-gap: 14px;
  min-height: 44px;
  padding: 0 10px;
  margin: 0 8px;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  box-sizing: border-box;
}

.filter-option input[type="checkbox"] { display: none; }

.filter-option.selected {
  background: #edf5ef;
  border-color: #4f7d6f;
}

.custom-checkbox {
  width: 18px;
  height: 18px;
  border: 2px solid #c5d1ca;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  font-weight: 900;
  background: white;
}

.filter-option.selected .custom-checkbox {
  background: #4f7d6f;
  border-color: #4f7d6f;
}

.option-text {
  font-size: 15px;
  line-height: 1.3;
  font-weight: 500;
  color: #40534d;
  text-align: left;
  white-space: normal;
  word-break: normal;
  overflow-wrap: anywhere;
}

.care-info {
  position: relative;
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid #6f9181;
  border-radius: 999px;
  color: #4f6f67;
  font-size: 11px;
  font-weight: 800;
  line-height: 1;
  cursor: help;
  background: #ffffff;
}

.care-info:hover,
.care-info:focus {
  background: #edf5ef;
  outline: none;
}

.care-tooltip {
  position: absolute;
  left: calc(100% + 14px);
  top: 50%;
  z-index: 2100;
  width: 460px;
  max-width: min(460px, calc(100vw - 48px));
  padding: 16px 18px;
  border: 1px solid #e3ded5;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 8px 22px rgba(31, 45, 42, 0.16);
  color: #2b3633;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.7;
  text-align: left;
  white-space: normal;
  transform: translateY(-50%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease;
}

.care-tooltip::before {
  content: '';
  position: absolute;
  left: -7px;
  top: 50%;
  width: 12px;
  height: 12px;
  background: #ffffff;
  border-left: 1px solid #e3ded5;
  border-bottom: 1px solid #e3ded5;
  transform: translateY(-50%) rotate(45deg);
}

.care-info:hover .care-tooltip,
.care-info:focus .care-tooltip {
  opacity: 1;
}

.funding-option { grid-template-columns: 28px 1fr; }
.funding-text { white-space: normal; word-break: keep-all; }

.distance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
  cursor: pointer;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.toggle-track {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: #dbd8d4;
  border-radius: 22px;
  transition: background 0.2s;
}

.toggle-track::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  left: 3px;
  top: 3px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
}

.toggle-switch input:checked + .toggle-track { background: #4f7d6f; }
.toggle-switch input:checked + .toggle-track::before { transform: translateX(18px); }

.distance-warning-hint {
  margin: 0 8px;
  font-size: 12px;
  color: #c07000;
  line-height: 1.4;
}

.distance-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  margin: 0 8px;
}

.range-wrap { padding: 2px 8px 0; }

.distance-range {
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
  background: transparent;
}

.distance-range::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 999px;
  background: transparent;
}

.distance-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f8f8f6;
  border: 4px solid #4f7d6f;
  margin-top: -8px;
  cursor: pointer;
}

.filter-select,
.filter-input {
  width: calc(100% - 16px);
  height: 40px;
  margin: 0 8px;
  padding: 0 14px;
  border: 1px solid #cfd6cf;
  border-radius: 8px;
  background: #fffdfa;
  color: #33413c;
  font-size: 15px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.filter-select:focus,
.filter-input:focus {
  border-color: #6f8f80;
  box-shadow: 0 0 0 3px rgba(111, 143, 128, 0.12);
  background: #ffffff;
}

.filter-input::placeholder { color: #a8b0ab; }

.filter-field-hint {
  margin: 4px 8px 0;
  font-size: 12px;
  color: #a8b0ab;
}

.filter-field-error {
  margin: 4px 8px 0;
  font-size: 12px;
  color: #c0392b;
  line-height: 1.4;
}

.filter-input.input-error {
  border-color: #c0392b;
  box-shadow: 0 0 0 3px rgba(192, 57, 43, 0.1);
}

.apply-btn {
  width: calc(100% - 24px);
  margin: 14px 12px 4px;
  border: none;
  border-radius: 8px;
  padding: 13px 16px;
  background: #557067;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  font-family: var(--font-sans);
}

.apply-btn:hover {
  background: #3d6b59;
}

.apply-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #557067;
}

.filter-select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, #6b736f 50%),
    linear-gradient(135deg, #6b736f 50%, transparent 50%);
  background-position: calc(100% - 18px) calc(50% - 3px),
    calc(100% - 12px) calc(50% - 3px);
  background-size: 6px 6px, 6px 6px;
  background-repeat: no-repeat;
  padding-right: 38px;
}

@media (max-width: 768px) {
  .toggle-icon { display: inline; }
  .filters-body.collapsed { display: none; }

  .care-tooltip {
    left: auto;
    right: 0;
    top: calc(100% + 10px);
    width: min(280px, calc(100vw - 48px));
    transform: none;
  }

  .care-tooltip::before {
    left: auto;
    right: 5px;
    top: -7px;
    transform: rotate(135deg);
  }
}
</style>
