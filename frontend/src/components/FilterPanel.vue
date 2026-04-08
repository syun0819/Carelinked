<template>
  <div class="filters">
    <h3>Filters</h3>

    <div class="filter-group">
      <label><input type="checkbox" /> Residential Care</label>
      <label><input type="checkbox" /> Memory Care</label>
      <label><input type="checkbox" /> Respite Care</label>
      <label><input type="checkbox" /> High-Level Care</label>
    </div>

    <div class="filter-group">
      <label>Availability</label>
      <select>
        <option>All</option>
        <option>High</option>
        <option>Medium</option>
        <option>Low</option>
      </select>
    </div>

    <div class="filter-group">
      <label>Sort By</label>
      <select>
        <option>Closest to me</option>
        <option>Shortest wait time</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.filters h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  color: #1f2d2a;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 18px;
}

label {
  font-size: 14px;
  color: #1f2d2a;
}

select {
  padding: 8px 10px;
  border: 1px solid #d8d3ca;
  border-radius: 8px;
  background: white;
}
</style>