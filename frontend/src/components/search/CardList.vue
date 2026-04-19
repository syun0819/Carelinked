<template>
  <div class="results-list">
    <FacilityCard
      v-for="facility in facilities"
      :key="facility.id"
      :facility="facility"
    />
  </div>
</template>

<script setup>
import FacilityCard from '../FacilityCard.vue'

defineProps({
  facilities: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.results-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

@media (max-width: 900px) {
  .results-list {
    grid-template-columns: 1fr;
  }
}
</style>
