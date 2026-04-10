<template>
  <section class="map-section">
    <div class="map-placeholder">
      Map placeholder
    </div>
  </section>
</template>

<script setup>
defineProps({
  facilities: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.map-placeholder {
  min-height: 400px;
  background: white;
  border: 1px solid #ddd8cf;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7b8d87;
}
</style>