<template>
  <section id="explore-care" class="explore-section">
    <div class="explore-header">
      <h1 class="explore-title">Explore Aged Care</h1>
      <p class="explore-subtitle">
        Find the right aged care for you
      </p>
      <button class="location-request-btn" type="button" @click="$emit('request-location')">
        Use my location
      </button>
    </div>

    <div class="explore-results-header">
      <ResultsHeader
        :count="displayFacilities.length"
        :start="displayFacilities.length ? 1 : 0"
        :end="displayFacilities.length"
        :sort-by="sortOption"
        :distance="distance"
        @update:sortBy="sortOption = $event"
      />
    </div>

    <div v-if="loading" class="status-message">
      Loading recommended facilities...
    </div>

    <div v-else class="explore-grid">
      <FacilityCard
        v-for="facility in displayFacilities"
        :key="facility.id"
        :facility="facility"
      />
    </div>

    <div class="explore-actions">
      <button class="more-btn" @click="goToFindBed">
        View more facilities
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import FacilityCard from './FacilityCard.vue'
import ResultsHeader from './search/ResultsHeader.vue'
import { getRecommendedFacilities } from '../services/facilitiesApi'
import { mapFacilityCard } from '../utils/facilityMappers'

const router = useRouter()

const props = defineProps({
  userLocation: {
    type: Object,
    default: null
  }
})

defineEmits(['request-location'])

const recommendedFacilities = ref([])
const distance = ref(10)
const sortOption = ref('distance')
const loading = ref(false)

async function loadRecommendedFacilities() {
  loading.value = true

  try {
    const params = {
      limit: 6
    }

    if (
      props.userLocation &&
      props.userLocation.lat != null &&
      props.userLocation.lng != null
    ) {
      params.user_lat = props.userLocation.lat
      params.user_lng = props.userLocation.lng
    }

    const data = await getRecommendedFacilities(params)
    recommendedFacilities.value = (data.results || []).map(mapFacilityCard)
  } catch (error) {
    console.error('Failed to load recommended facilities:', error)
    recommendedFacilities.value = []
  } finally {
    loading.value = false
  }
}

function goToFindBed() {
  router.push('/find-bed')
}

const displayFacilities = computed(() => {
  let result = [...recommendedFacilities.value]

  if (sortOption.value === 'name') {
    result.sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortOption.value === 'distance') {
    result.sort((a, b) => {
      const aDistance = a.distanceKm ?? a.distance ?? Number.MAX_SAFE_INTEGER
      const bDistance = b.distanceKm ?? b.distance ?? Number.MAX_SAFE_INTEGER
      return aDistance - bDistance
    })
  }

  return result
})

watch(
  () => props.userLocation,
  () => {
    loadRecommendedFacilities()
  },
  { immediate: true, deep: true }
)
</script>

<style scoped>
.explore-section {
  padding: 120px 40px 56px;
  background: #f7f4ee;
}

.explore-header {
  text-align: center;
  margin: 0 0 20px;
}

.explore-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2d2a;
  margin: 0;
  font-family: var(--font-display);
  line-height: 1.1;
}

.location-request-btn {
  margin-top: 14px;
  border: 1px solid #cfd8d4;
  border-radius: 999px;
  background: #fff;
  color: #2d6a5f;
  padding: 7px 13px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: var(--font-sans);
  white-space: nowrap;
  box-shadow: 0 6px 14px rgba(31, 45, 42, 0.08);
}

.location-request-btn:hover {
  border-color: #557067;
  background: #f5f8f6;
}

.explore-subtitle {
  font-size: 15px;
  color: #6b736f;
  margin-top: 8px;
  line-height: 1.45;
  font-family: var(--font-sans);
}

.explore-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  justify-content: center;
  gap: 24px;
  width: min(100%, 1544px);
  margin: 0 auto;
}

.explore-results-header {
  width: min(100%, 1544px);
  margin: 0 auto 24px;
}

.explore-actions {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.more-btn {
  border: none;
  border-radius: 999px;
  padding: 12px 22px;
  background: #557067;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.more-btn:hover {
  background: #486158;
}

.status-message {
  text-align: center;
  color: #6b736f;
  padding: 24px 0;
}

@media (max-width: 1024px) {
  .explore-section {
    padding: 40px 24px 56px;
  }

  .explore-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .explore-title-row {
    flex-direction: column;
    gap: 10px;
  }

  .explore-grid {
    grid-template-columns: 1fr;
  }
}
</style>
