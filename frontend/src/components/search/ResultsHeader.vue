<template>
  <div class="results-header">
    <p class="results-count">
      Showing {{ count }} care facilities
    </p>

    <label class="sort-box">
      <span>Sort by:</span>
      <select :value="sortBy" @change="$emit('update:sortBy', $event.target.value)">
        <option value="availability">Highest availability</option>
        <option value="wait">Shortest wait</option>
        <option value="name">A to Z</option>
      </select>
    </label>
  </div>
</template>

<script setup>
defineProps({
  count: {
    type: Number,
    default: 0
  },
  sortBy: {
    type: String,
    default: 'availability'
  }
})

defineEmits(['update:sortBy'])
</script>

<style scoped>
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-count {
  margin: 0;
  color: #77857f;
  font-size: 15px;
}

.sort-box {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-box span {
  color: #6b736f;
}

.sort-box select {
  padding: 6px 10px;
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  background: white;
  font-size: 13px;
  color: #1f2d2a;
  cursor: pointer;
}
</style>