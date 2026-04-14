<template>
  <aside class="filters-panel">
    <div class="filters-header">
      <h2>Filters</h2>
      <button class="reset-btn" @click="$emit('reset')">Reset all</button>
    </div>

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
        <span class="option-icon">{{ item.icon }}</span>
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
      <p class="filter-title">BED AVAILABILITY</p>

      <label
        v-for="item in availabilityOptions"
        :key="item.value"
        class="filter-option"
        :class="{ selected: selectedAvailability.includes(item.value) }"
      >
        <input
          type="checkbox"
          :checked="selectedAvailability.includes(item.value)"
          @change="toggleAvailability(item.value)"
        />
        <span class="custom-checkbox">
          <span v-if="selectedAvailability.includes(item.value)">✓</span>
        </span>
        <span class="option-text">{{ item.label }}</span>
      </label>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  selectedCareTypes: {
    type: Array,
    default: () => []
  },
  distance: {
    type: Number,
    default: 10
  },
  distanceFilterEnabled: {
    type: Boolean,
    default: false
  },
  distanceWarning: {
    type: String,
    default: ''
  },
  careTypeOptions: {
    type: Array,
    default: () => []
  },
  minDistance: {
    type: Number,
    default: 1
  },
  maxDistance: {
    type: Number,
    default: 20
  },
  selectedAvailability: {
    type: Array,
    default: () => []
  },
  availabilityOptions: {
    type: Array,
    default: () => []
  },
})

const emit = defineEmits([
  'update:selectedCareTypes',
  'update:distance',
  'update:distanceFilterEnabled',
  'update:selectedAvailability',
  'reset'
])

function toggleCareType(value) {
  const next = props.selectedCareTypes.includes(value)
    ? props.selectedCareTypes.filter(item => item !== value)
    : [...props.selectedCareTypes, value]

  emit('update:selectedCareTypes', next)
}

function toggleAvailability(value) {
  const next = props.selectedAvailability.includes(value)
    ? props.selectedAvailability.filter(item => item !== value)
    : [...props.selectedAvailability, value]

  emit('update:selectedAvailability', next)
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
  padding: 26px 26px 30px;
  width: 100%;
  box-sizing: border-box;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.filters-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #22332e;
  margin-top: -10px;
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
  gap: 10px;
  margin-bottom: 18px;
}

.filter-title {
  margin: 0;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: #a4afa9;
  text-align: left;
}

.filter-option {
  display: grid;
  grid-template-columns: 28px 24px 1fr;
  align-items: center;
  column-gap: 4px;
  min-height: 40px;
  padding: 0 15px;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  box-sizing: border-box;
}

.filter-option input[type="checkbox"] {
  display: none;
}

.filter-option.selected {
  background: #edf5ef;
  border-color: #4f7d6f;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
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

.option-icon {
  width: 22px;
  text-align: center;
  font-size: 19px;
}

.option-text {
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
  color: #40534d;
  text-align: left;
}

.funding-option {
  grid-template-columns: 28px 1fr;
}

.funding-text {
  white-space: normal;
  word-break: keep-all;
}

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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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

.toggle-switch input:checked + .toggle-track {
  background: #4f7d6f;
}

.toggle-switch input:checked + .toggle-track::before {
  transform: translateX(18px);
}

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

.range-wrap {
  padding-top: 2px;
}

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
</style>