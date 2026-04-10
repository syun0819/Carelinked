<template>
  <section class="list-section">
    <CardList :facilities="facilities" />
  </section>
</template>

<script setup>
import CardList from './CardList.vue'

defineProps({
  facilities: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.list-section {
  width: 100%;
}
</style>