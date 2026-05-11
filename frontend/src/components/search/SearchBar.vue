<template>
  <section class="search-top">
    <div class="search-bar">
      <span class="search-icon">⌕</span>

      <input
        v-model="inputValue"
        class="search-input"
        type="text"
        placeholder="Search by suburb, postcode or region..."
        @focus="showSuggestions = true"
        @blur="hideSuggestions"
        @keyup.enter="handleSearch"
      />

      <button class="search-btn" @click="handleSearch">
        Search
      </button>

      <button
        class="match-me-btn"
        :class="{ active: matchingActive }"
        type="button"
        @click="$emit('open-match-modal')"
      >
        <span aria-hidden="true">✦</span>
        {{ matchingActive ? 'Edit matches' : 'Match me' }}
      </button>

      <ul
        v-if="showSuggestions && suggestions.length"
        class="search-suggestions"
      >
        <li
          v-for="suggestion in suggestions"
          :key="`${suggestion.type}-${suggestion.searchValue}-${suggestion.value}`"
          class="search-suggestion"
          @mousedown.prevent="selectSuggestion(suggestion)"
        >
          <span class="suggestion-main">
            <span class="suggestion-icon" aria-hidden="true">{{ getSuggestionIcon(suggestion.type) }}</span>
            <span class="suggestion-value">{{ suggestion.value }}</span>
          </span>
          <span class="suggestion-type">{{ suggestion.type }}</span>
        </li>
      </ul>
    </div>
    <p v-if="!matchingActive" class="match-helper">
      <span aria-hidden="true">✦</span>
      Not sure where to start? Tap <strong>Match Me</strong> to rank facilities by what matters most to you.
    </p>
    <div v-else class="match-summary">
      <div class="summary-label">
        <span class="summary-icon" aria-hidden="true">✦</span>
        <span>Matched on your priorities:</span>
      </div>

      <ol class="summary-chips" aria-label="Selected match priorities">
        <li
          v-for="(item, index) in rankedMatchPreferences"
          :key="item.key"
          class="summary-chip"
          :style="{ '--pref-color': item.color }"
        >
          <span class="chip-rank">{{ index + 1 }}.</span>
          <span class="chip-marker">{{ item.marker }}</span>
          <span class="chip-label">{{ item.label }}</span>
          <strong>{{ item.points }}</strong>
        </li>
      </ol>

      <div class="summary-actions">
        <button class="summary-action" type="button" @click="$emit('open-match-modal')">
          <span aria-hidden="true">✎</span>
          Edit
        </button>
        <button class="summary-action" type="button" @click="$emit('clear-match')">
          <span aria-hidden="true">×</span>
          Clear
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { getSearchAutocomplete } from '../../services/facilitiesApi'
import { MATCH_PREFERENCES } from '../../constants/matchPreferences'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  searchType: {
    type: String,
    default: ''
  },
  matchingActive: {
    type: Boolean,
    default: false
  },
  matchWeights: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'update:searchType', 'open-match-modal', 'clear-match'])

const inputValue = ref(props.modelValue)
const suggestions = ref([])
const showSuggestions = ref(false)
const activeSearchType = ref(props.searchType)
let autocompleteTimer = null
let autocompleteController = null
let selectingSuggestion = false
let syncingFromModel = false

const rankedMatchPreferences = computed(() =>
  MATCH_PREFERENCES
    .map(pref => ({
      ...pref,
      points: Number(props.matchWeights?.[pref.key] || 0)
    }))
    .filter(pref => pref.points > 0)
    .sort((a, b) => b.points - a.points || a.label.localeCompare(b.label))
)

watch(
  () => props.modelValue,
  (val) => {
    syncingFromModel = true
    inputValue.value = val
  }
)

watch(
  () => props.searchType,
  (val) => {
    activeSearchType.value = val
  }
)

watch(inputValue, (val) => {
  clearTimeout(autocompleteTimer)

  if (selectingSuggestion) {
    selectingSuggestion = false
    return
  }

  if (syncingFromModel) {
    syncingFromModel = false
    return
  }

  activeSearchType.value = ''
  emit('update:searchType', '')

  const q = val.trim()
  if (!q) {
    suggestions.value = []
    return
  }

  autocompleteTimer = setTimeout(() => {
    fetchSuggestions(q)
  }, 250)
})

async function fetchSuggestions(q) {
  if (autocompleteController) {
    autocompleteController.abort()
  }

  autocompleteController = new AbortController()

  try {
    const data = await getSearchAutocomplete(q, {
      signal: autocompleteController.signal
    })
    suggestions.value = normalizeSuggestions(data)
    showSuggestions.value = true
  } catch (err) {
    if (err.name !== 'AbortError') {
      suggestions.value = []
    }
  }
}

function normalizeSuggestions(data) {
  const values = [
    ...toArray(data.facilities).map(item => makeSuggestion(item, 'Facility')),
    ...toArray(data.suburbs).map(item => makeSuggestion(item, 'Suburb')),
    ...toArray(data.regions).map(item => makeSuggestion(item, 'Region')),
    ...toArray(data.region).map(item => makeSuggestion(item, 'Region')),
    ...toArray(data.postcodes).map(makePostcodeSuggestion)
  ]
  const seen = new Set()

  return values
    .filter(suggestion => {
      const key = `${suggestion.type}-${suggestion.value}`
      if (!suggestion.value || seen.has(key)) return false
      seen.add(key)
      return true
    })
    .slice(0, 8)
}

function toArray(value) {
  if (!value) return []
  return Array.isArray(value) ? value : [value]
}

function makeSuggestion(item, type) {
  if (typeof item === 'string' || typeof item === 'number') {
    const value = String(item)
    return {
      value,
      searchValue: value,
      type,
      searchType: getSearchParamType(type)
    }
  }

  const value =
    item?.name ||
    item?.facility_name ||
    item?.suburb ||
    item?.region ||
    item?.postcode ||
    item?.label ||
    ''

  return {
    value,
    searchValue: value,
    type: item?.type || type,
    searchType: getSearchParamType(item?.type || type)
  }
}

function makePostcodeSuggestion(item) {
  if (typeof item === 'string' || typeof item === 'number') {
    const value = String(item)
    return {
      value,
      searchValue: value,
      type: 'Postcode',
      searchType: 'postcode'
    }
  }

  const postcode = item?.postcode || item?.postal_code || item?.zip || ''
  const suburb = item?.suburb || item?.name || item?.locality || item?.region || item?.label || ''
  const value = [suburb, postcode].filter(Boolean).join(', ')

  return {
    value,
    searchValue: postcode || suburb || value,
    type: item?.type || 'Postcode',
    searchType: 'postcode'
  }
}

function getSearchParamType(type) {
  const normalizedType = String(type).toLowerCase()
  if (normalizedType === 'suburb') return 'suburb'
  if (normalizedType === 'postcode') return 'postcode'
  if (normalizedType === 'region') return 'region'
  return 'keyword'
}

function getSuggestionIcon(type) {
  const normalizedType = String(type).toLowerCase()
  if (normalizedType === 'facility') return '⌂'
  if (normalizedType === 'suburb') return '⌖'
  if (normalizedType === 'postcode') return '#'
  if (normalizedType === 'region') return '□'
  return '⌕'
}

function handleSearch() {
  clearTimeout(autocompleteTimer)
  if (autocompleteController) {
    autocompleteController.abort()
  }

  emit('update:modelValue', inputValue.value)
  emit('update:searchType', activeSearchType.value)
  suggestions.value = []
  showSuggestions.value = false
}

function selectSuggestion(suggestion) {
  selectingSuggestion = true
  inputValue.value = suggestion.searchValue
  activeSearchType.value = suggestion.searchType
  handleSearch()
}

function hideSuggestions() {
  setTimeout(() => {
    showSuggestions.value = false
  }, 150)
}
</script>

<style scoped>
.search-top {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto 30px;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2200;
}

.search-bar {
  width: 100%;
  max-width: 1180px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 10px;
  padding: 6px 16px;
  position: relative;
}

.search-icon {
  color: #7b8d87;
  font-size: 30px;
  margin-bottom: 8px;
}

.search-input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #030303;
}

.search-input::placeholder {
  color: #bec5c2;
}

.search-btn {
  background: #f3f1ec;
  color: #1f2d2a;
  border: none;
  padding: 12px 28px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 800;
}

.search-btn:hover {
  background: #ebe7df;
}

.match-me-btn {
  border: none;
  border-radius: 6px;
  background: linear-gradient(90deg, #4ea283, #4f7f80);
  color: #fff;
  padding: 12px 22px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  white-space: nowrap;
}

.match-me-btn:hover,
.match-me-btn.active {
  background: #23695e;
}

.match-me-btn span,
.match-helper span {
  color: currentColor;
  font-size: 20px;
  line-height: 1;
}

.match-helper {
  margin: 18px 0 0;
  color: #24463f;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 18px;
  line-height: 1.4;
  text-align: center;
}

.match-helper strong {
  color: #1f4039;
  font-weight: 900;
}

.match-summary {
  width: 100%;
  max-width: 1180px;
  margin: 28px auto 0;
  min-height: 78px;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  border: 1px solid #cbd8d2;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  padding: 14px 22px;
  box-shadow: 0 8px 26px rgba(31, 45, 42, 0.06);
}

.summary-label {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #1f2d2a;
  font-size: 15px;
  font-weight: 700;
  white-space: nowrap;
}

.summary-icon {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #dbece5;
  color: #2d6a5f;
  font-size: 20px;
}

.summary-chips {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  list-style: none;
  margin: 0;
  padding: 0;
  min-width: 0;
}

.summary-chip {
  min-width: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #ddd8cf;
  border-radius: 999px;
  background: #fff;
  padding: 5px 10px;
  color: #1f2d2a;
  font-size: 13px;
  line-height: 1;
  box-shadow: 0 1px 3px rgba(31, 45, 42, 0.05);
}

.chip-rank {
  color: #65736e;
  font-weight: 800;
}

.chip-marker {
  color: var(--pref-color);
  font-size: 11px;
  font-weight: 900;
}

.chip-label {
  max-width: 190px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-chip strong {
  color: var(--pref-color);
  font-weight: 900;
}

.summary-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  white-space: nowrap;
}

.summary-action {
  border: none;
  background: transparent;
  color: #374843;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  padding: 6px;
}

.summary-action:hover {
  color: #23695e;
}

.search-suggestions {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  z-index: 3000;
  margin: 0;
  padding: 6px 0;
  list-style: none;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(31, 45, 42, 0.12);
}

.search-suggestion {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 16px;
  color: #030303;
  font-size: 14px;
  cursor: pointer;
  text-align: left;
}

.search-suggestion:hover {
  background: #f7f4ee;
}

.suggestion-main {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 11px;
}

.suggestion-icon {
  width: 32px;
  height: 32px;
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #dfece5;
  color: #34594f;
  font-size: 17px;
  font-weight: 800;
}

.suggestion-value {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
}

.suggestion-type {
  flex: 0 0 auto;
  color: #7b8d87;
  font-size: 12px;
}

@media (max-width: 760px) {
  .search-bar {
    align-items: stretch;
    flex-wrap: wrap;
  }

  .search-input {
    min-width: 0;
    flex: 1 1 220px;
  }

  .search-btn,
  .match-me-btn {
    flex: 1 1 auto;
    justify-content: center;
  }

  .match-helper {
    font-size: 15px;
    align-items: flex-start;
  }

  .match-summary {
    grid-template-columns: 1fr;
    align-items: start;
    gap: 12px;
    padding: 16px;
  }

  .summary-label,
  .summary-actions {
    white-space: normal;
  }

  .summary-actions {
    justify-content: flex-start;
  }
}
</style>
