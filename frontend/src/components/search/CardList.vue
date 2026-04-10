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
  display: flex;
  flex-direction: column;
  gap: 18px;
}
</style>