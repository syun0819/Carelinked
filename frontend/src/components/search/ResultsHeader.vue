<template>
  <div class="results-header">
    <p class="results-count">
      Showing {{ start }}–{{ end }} of {{ count }} care facilities
    </p>

    <div v-if="viewMode === 'list'" class="header-actions">
      <button
        v-if="matchingActive"
        class="clear-match-btn"
        type="button"
        @click="$emit('clear-match')"
      >
        Clear
      </button>

      <span v-if="matchingActive" class="match-sort-note">Ranked by your priorities</span>

      <label v-else class="sort-box">
        <span>Sort by:</span>
        <select :value="sortBy" @change="$emit('update:sortBy', $event.target.value)">
          <option value="">None</option>
          <option value="name">A to Z</option>
          <option value="beds_desc">Most beds</option>
          <option value="beds_asc">Fewest beds</option>
          <option value="distance">Closest to me</option>
        </select>
      </label>
    </div>
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
  matchingActive: {
    type: Boolean,
    default: false
  },
  viewMode: String 
})

defineEmits(['update:sortBy', 'clear-match'])
</script>

<style scoped>
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.clear-match-btn {
  border: 1px solid #ddd8cf;
  border-radius: 999px;
  background: #fff;
  color: #65736e;
  padding: 7px 13px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.match-sort-note {
  color: #65736e;
  font-size: 13px;
  font-weight: 700;
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

@media (max-width: 760px) {
  .results-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    justify-content: flex-start;
  }
}
</style>
