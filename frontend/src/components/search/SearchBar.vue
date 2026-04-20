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
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getSearchAutocomplete } from '../../services/facilitiesApi'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  searchType: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'update:searchType'])

const inputValue = ref(props.modelValue)
const suggestions = ref([])
const showSuggestions = ref(false)
const activeSearchType = ref(props.searchType)
let autocompleteTimer = null
let autocompleteController = null
let selectingSuggestion = false
let syncingFromModel = false

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
  max-width: 1000px;
  margin: 0 auto 30px;
  padding: 0 24px;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 10;
}

.search-bar {
  width: 100%;
  max-width: 750px;
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
  background: #4f6f67;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.search-btn:hover {
  background: #3f5c55;
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
</style>
