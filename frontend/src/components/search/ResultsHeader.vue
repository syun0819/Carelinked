<template>
  <div class="results-header">
    <p class="results-count">
      Showing {{ start }}–{{ end }} of {{ count }} care facilities
    </p>

    <label v-if="viewMode === 'list'" class="sort-box">
      <span>Sort by:</span>
      <select :value="sortBy" @change="$emit('update:sortBy', $event.target.value)">
        <option value="name">A to Z</option>
        <option value="beds_desc">Most beds</option>
        <option value="beds_asc">Fewest beds</option>
        <option value="distance">Closest to me</option>
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
  distance: {
    type: Number,
    default: 10
  },
  start: {
    type: Number,
    default: 0
  },
  end: {
    type: Number,
    default: 0
  },
  sortBy: {
    type: String,
    default: 'name'
  },
  viewMode: String 
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
  font-size: 14px;
}

.sort-box select {
  padding: 3px 6px;
  border: 1px solid #ddd8cf;
  border-radius: 4px;
  background: white;
  font-size: 13px;
  color: #1f2d2a;
  cursor: pointer;
}
</style>