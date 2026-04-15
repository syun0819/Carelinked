<template>
  <aside class="filters-panel">
    <div class="filters-header">
      <h2>Filters</h2>
      <div class="filters-header-right">
        <button class="reset-btn" @click.stop="$emit('reset')">Reset all</button>
        <span class="toggle-icon" @click="toggleFilters">{{ filtersOpen ? '▲' : '▼' }}</span>
      </div>
    </div>

    <div class="filters-body" :class="{ collapsed: !filtersOpen }">
      <div class="filter-section">
        <p class="filter-title">CARE TYPE</p>
        <label
          v-for="item in careTypeOptions"
          :key="item.value"
          class="filter-option"
          :class="{ selected: selectedCareTypes.includes(item.value) }"
        >
          <input
            type="checkbox"
            :checked="selectedCareTypes.includes(item.value)"
            @change="toggleCareType(item.value)"
          />
          <span class="custom-checkbox">
            <span v-if="selectedCareTypes.includes(item.value)">✓</span>
          </span>
          <span class="option-text">{{ item.label }}</span>
        </label>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <div class="distance-header">
          <p class="filter-title">DISTANCE FILTER</p>
          <label class="toggle-switch">
            <input
              type="checkbox"
              :checked="distanceFilterEnabled"
              @change="$emit('update:distanceFilterEnabled', $event.target.checked)"
            />
            <span class="toggle-track"></span>
          </label>
        </div>
        <template v-if="distanceFilterEnabled">
          <div class="distance-top">
            <span>Within</span>
            <strong>{{ distance }} km</strong>
          </div>
          <div class="range-wrap">
            <input
              class="distance-range"
              type="range"
              :min="minDistance"
              :max="maxDistance"
              :value="distance"
              :style="rangeStyle"
              @input="$emit('update:distance', Number($event.target.value))"
            />
          </div>
          <p v-if="distanceWarning" class="distance-warning-hint">{{ distanceWarning }}</p>
        </template>
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <div class="filter-title">LOCATION TYPE</div>
        <select v-model="localRemoteness" class="filter-select">
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
        <div class="filter-title">MIN BEDS</div>
        <input
          type="number"
          v-model="localMinBeds"
          class="filter-input"
          placeholder="e.g. 20"
        />
      </div>

      <hr class="filter-divider" />

      <div class="filter-section">
        <div class="filter-title">MAX BEDS</div>
        <input
          type="number"
          v-model="localMaxBeds"
          class="filter-input"
          placeholder="e.g. 100"
        />
      </div>
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
  'update:selectedCareTypes',
  'update:distance',
  'update:selectedRemoteness',
  'update:minBeds',
  'update:maxBeds',
  'update:distanceFilterEnabled',
  'reset'
])

const localRemoteness = ref(props.selectedRemoteness || '')
const localMinBeds = ref(props.minBeds)
const localMaxBeds = ref(props.maxBeds)
const filtersOpen = ref(window.innerWidth > 768)

function toggleFilters() {
  if (window.innerWidth <= 768) {
    filtersOpen.value = !filtersOpen.value
  }
}

watch(localRemoteness, (val) => emit('update:selectedRemoteness', val))
watch(localMinBeds, (val) => emit('update:minBeds', val === '' ? null : Number(val)))
watch(localMaxBeds, (val) => emit('update:maxBeds', val === '' ? null : Number(val)))
watch(() => props.selectedRemoteness, (val) => { localRemoteness.value = val || '' })
watch(() => props.minBeds, (val) => { localMinBeds.value = val })
watch(() => props.maxBeds, (val) => { localMaxBeds.value = val })

function toggleCareType(value) {
  const next = props.selectedCareTypes.includes(value)
    ? props.selectedCareTypes.filter(item => item !== value)
    : [...props.selectedCareTypes, value]
  emit('update:selectedCareTypes', next)
}

const rangeStyle = computed(() => {
  const percentage =
    ((props.distance - props.minDistance) / (props.maxDistance - props.minDistance)) * 100
  return {
    background: `linear-gradient(to right, #4f7d6f 0%, #4f7d6f ${percentage}%, #dbd8d4 ${percentage}%, #dbd8d4 100%)`
  }
})
</script>

<style scoped>
.filters-panel {
  background: #ffffff;
  border: 1.5px solid #ddd5ca;
  border-radius: 8px;
  padding: 0 26px;
  width: 100%;
  box-sizing: border-box;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 56px;
  margin-bottom: 0;
}

.filters-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #22332e;
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
  padding-bottom: 16px;
}

.reset-btn {
  border: none;
  background: transparent;
  padding: 0;
  font-size: 14px;
  font-weight: 700;
  color: #5a8b72;
  cursor: pointer;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 18px;
}

.filter-title {
  margin: 0;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: #2D6A5F;
  text-align: left;
}

.filter-option {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  align-items: center;
  column-gap: 14px;
  min-height: 54px;
  padding: 0 12px;
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
  font-size: 16px;
  line-height: 1.4;
  font-weight: 500;
  color: #40534d;
  text-align: left;
  white-space: normal;
  word-break: normal;
  overflow-wrap: anywhere;
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
  margin: 0;
  font-size: 12px;
  color: #c07000;
  line-height: 1.4;
}

.distance-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
}

.range-wrap { padding-top: 2px; }

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
  width: 100%;
  height: 40px;
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
}
</style>