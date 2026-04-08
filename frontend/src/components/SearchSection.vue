<template>
  <section class="search-section">
    <div class="search-toolbar">
      <input
        type="text"
        placeholder="Search by facility name, suburb, or care type..."
      />
    </div>

    <div class="view-toggle">
      <button class="active">List View</button>
      <button>Map View</button>
    </div>

    <div class="search-content">
      <aside class="filters-column">
        <FilterPanel />
      </aside>

      <main class="results-column">
        <div class="results-header">
          <p>Showing {{ facilities.length }} care facilities within 10km</p>
          <select>
            <option>Closest to me</option>
          </select>
        </div>

        <FacilityList :facilities="facilities" />
      </main>
    </div>
  </section>
</template>

<script setup>
import FilterPanel from './FilterPanel.vue'
import FacilityList from './FacilityList.vue'

defineProps({
  facilities: {
    type: Array,
    required: true
  }
})
</script>