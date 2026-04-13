<template>
  <section class="explore-section">
    <div class="explore-header">
      <h1 class="explore-title">Explore Aged Care</h1>
      <p class="explore-subtitle">
        Find the right aged care for you
      </p>
    </div>

    <ResultsHeader
      :count="displayFacilities.length"
      :sort-by="sortOption"
      :distance="distance"
      @update:sortBy="sortOption = $event"
    />

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

const recommendedFacilities = ref([])
const distance = ref(10)
const sortOption = ref('closest')
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
  } else if (sortOption.value === 'closest') {
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
  padding: 20px 80px 60px;
  background: #f7f4ee;
}

.explore-header {
  text-align: center;
  margin-bottom: 20px;
  margin-top: 30px;
}

.explore-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2d2a;
  margin: 0;
  font-family: 'Georgia', serif;
}

.explore-subtitle {
  font-size: 12px;
  color: #6b736f;
  margin-top: 10px;
  font-family: 'Inter', sans-serif;
}

.explore-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.explore-actions {
  display: flex;
  justify-content: center;
  margin-top: 28px;
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
    padding-left: 24px;
    padding-right: 24px;
  }

  .explore-grid {
    grid-template-columns: 1fr;
  }
}
</style>