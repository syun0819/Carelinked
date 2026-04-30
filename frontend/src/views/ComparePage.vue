<template>
  <div class="compare-page">
    <Header />
    <div class="compare-container page-animate">
      <div v-if="loading" class="state-box">
        <div class="loading-spinner"></div>
        <p>Loading facilities…</p>
      </div>
      <ComparePicker
        v-else-if="!comparisonStarted || facilities.length < 2"
        :slots="slots"
        :facilities="facilities"
        @slot-search="onSlotSearch"
        @add-from-slot="addFromSlot"
        @remove-facility="removeFacility"
        @go-back="goBack"
        @clear-selection="clearSelection"
      />
      <CompareTable
        v-else
        :facilities="facilities"
        :slots="slots"
        :is-full="compareStore.isFull"
        @remove-facility="removeFacility"
        @go-back="goBack"
        @clear-all="clearAll"
        @go-to-detail="goToDetail"
        @add-from-add-panel="addFromAddPanel"
        @slot-search="onSlotSearch"
      />
    </div>
    <FooterSection />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import ComparePicker from '../components/ComparePicker.vue'
import CompareTable from '../components/CompareTable.vue'
import { useCompareStore } from '../stores/compareStore'
import { getFacilityDetail, getAutocomplete } from '../services/facilitiesApi'
import { mapFacilityDetail } from '../utils/facilityMappers'

const router = useRouter()
const route = useRoute()
const compareStore = useCompareStore()

const shouldShowResults = computed(() =>
  route.query.mode === 'results' &&
  compareStore.count >= compareStore.initialSelectionLimit
)
const shouldKeepSelection = computed(() => route.query.keepSelection === '1')
const facilities = ref([])
const loading = ref(shouldShowResults.value && compareStore.items.length > 0)
const comparisonStarted = ref(shouldShowResults.value)

// Per-slot search state
const slots = reactive([
  { query: '', results: [], loading: false },
  { query: '', results: [], loading: false },
  { query: '', results: [], loading: false },
])
const slotTimers = [null, null, null]

function onSlotSearch(idx) {
  clearTimeout(slotTimers[idx])
  const q = slots[idx].query.trim()
  if (!q || q.length < 2) { slots[idx].results = []; return }
  slots[idx].loading = true
  slotTimers[idx] = setTimeout(async () => {
    try {
      const data = await getAutocomplete(q)
      const facilityResults = (data.facilities || [])
        .filter(r => !compareStore.has(r.id))
        .map(r => ({
          id: r.id,
          name: r.name,
          suburb: '',
          state: '',
          postcode: '',
        }))
      slots[idx].results = facilityResults
    } catch (err) {
      console.error('Autocomplete error:', err)
      slots[idx].results = []
    } finally {
      slots[idx].loading = false
    }
  }, 250)
}

async function addFromSlot(idx, r) {
  if (compareStore.has(r.id) || compareStore.isFull) return
  compareStore.add(r.id, r.name)
  slots[idx].loading = true
  try {
    const detail = await getFacilityDetail(r.id).then(mapFacilityDetail)
    facilities.value = [...facilities.value, detail]
    if (facilities.value.length >= compareStore.initialSelectionLimit) {
      comparisonStarted.value = true
      router.replace({ path: '/compare', query: { mode: 'results' } })
    }
  } finally {
    slots[idx].loading = false
  }
  slots[idx].query = ''
  slots[idx].results = []
}

async function addFromAddPanel(r) {
  const activeAddSlot = Math.min(facilities.value.length, slots.length - 1)
  await addFromSlot(activeAddSlot, r)
}

onUnmounted(() => {
  compareStore.clear()
})

async function loadSelectedFacilities() {
  if (compareStore.items.length === 0) return
  loading.value = true
  try {
    const results = await Promise.all(
      compareStore.items.map(({ id }) => getFacilityDetail(id).then(mapFacilityDetail))
    )
    facilities.value = results
    comparisonStarted.value = shouldShowResults.value
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!shouldShowResults.value && !shouldKeepSelection.value) {
    compareStore.clear()
    facilities.value = []
    comparisonStarted.value = false
    loading.value = false
    return
  }

  await loadSelectedFacilities()
})

watch(() => [route.query.mode, route.query.keepSelection], async ([mode, keepSelection]) => {
  if (mode === 'results' || keepSelection === '1') {
    await loadSelectedFacilities()
    return
  }

  compareStore.clear()
  facilities.value = []
  comparisonStarted.value = false
  loading.value = false
})

function removeFacility(id) {
  compareStore.remove(id)
  facilities.value = facilities.value.filter(f => f.id !== id)
}

function clearSelection() {
  compareStore.clear()
  facilities.value = []
  comparisonStarted.value = false
  slots.forEach(slot => {
    slot.query = ''
    slot.results = []
    slot.loading = false
  })
}

function clearAll() {
  compareStore.clear()
  facilities.value = []
  comparisonStarted.value = false
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
  max-width: 1300px;
  margin: 0 auto;
  padding: 110px 32px 80px;
}

/* ── Global loading ── */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: #7f8d87;
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

/* ── Responsive ── */
@media (min-width: 769px) and (max-width: 1100px) {
  .compare-container { padding: 100px 20px 60px; }
}

@media (max-width: 768px) {
  .compare-container { padding: 90px 16px 60px; }
}
</style>
