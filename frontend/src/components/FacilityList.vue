<template>
  <div class="facility-list">
    <FacilityCard
      v-for="facility in facilities"
      :key="facility.id"
      :facility="facility"
    />
  </div>
</template>

<script setup>
import FacilityCard from './FacilityCard.vue'

defineProps({
  facilities: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.facility-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
</style>