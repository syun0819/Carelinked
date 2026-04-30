<template>
  <div class="picker-section">

    <div class="picker-hero">
      <div class="picker-badge">✦ SIDE-BY-SIDE COMPARISON</div>
      <h1 class="picker-title">Compare aged care facilities</h1>
      <p class="picker-subtitle">Pick <strong>2 facilities</strong> below to compare wait times, ratings, staffing and compliance side-by-side.</p>
    </div>

    <div class="slot-cards">
      <div
        v-for="idx in [0, 1]"
        :key="idx"
        class="slot-card"
        :class="{
          'slot-card-filled': !!facilities[idx],
          'slot-card-searching': !facilities[idx] && slots[idx].results.length > 0
        }"
      >
        <!-- ── Filled slot ── -->
        <template v-if="facilities[idx]">
          <div class="slot-filled-inner">
            <div class="slot-filled-img-wrap">
              <span class="slot-num-badge-filled">{{ idx + 1 }}</span>
              <button class="slot-remove-btn" @click="$emit('remove-facility', facilities[idx].id)" aria-label="Remove facility">×</button>
              <img :src="facilities[idx].image" :alt="facilities[idx].name" class="slot-thumb" />
            </div>
            <div class="slot-info">
              <div class="slot-name">{{ facilities[idx].name }}</div>
              <div class="slot-loc">{{ facilities[idx].suburb }}, {{ facilities[idx].state }}</div>
            </div>
          </div>
        </template>

        <!-- ── Empty slot (search UI) ── -->
        <template v-else>
          <div class="slot-num-badge">{{ idx + 1 }}</div>

          <div class="slot-icon-wrap">
            <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="6" width="18" height="15" rx="2"/>
              <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              <line x1="9" y1="11" x2="9" y2="11.01"/>
              <line x1="15" y1="11" x2="15" y2="11.01"/>
              <line x1="9" y1="15" x2="9" y2="15.01"/>
              <line x1="15" y1="15" x2="15" y2="15.01"/>
            </svg>
          </div>

          <div class="slot-card-title">Choose {{ idx === 0 ? 'first' : 'second' }} facility</div>
          <div class="slot-card-desc">Search by name, suburb or provider to add it to your comparison.</div>

          <div class="slot-search-area">
            <div class="slot-search-wrap">
              <svg class="slot-search-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
              <input
                v-model="slots[idx].query"
                class="slot-search-input"
                placeholder="Search facilities..."
                @input="$emit('slot-search', idx)"
              />
              <div v-if="slots[idx].loading" class="slot-spinner"></div>
            </div>

            <div v-if="slots[idx].results.length > 0" class="slot-dropdown">
              <div
                v-for="r in slots[idx].results"
                :key="r.id"
                class="slot-dropdown-item"
                @click="$emit('add-from-slot', idx, r)"
              >
                <div class="dropdown-icon">
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="6" width="18" height="15" rx="2"/>
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                </div>
                <div class="dropdown-info">
                  <div class="dropdown-name">{{ r.name }}</div>
                  <div class="dropdown-meta">
                    <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.1 7-12A7 7 0 0 0 5 9c0 5.9 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg>
                    {{ r.suburb }}, {{ r.state }}
                  </div>
                </div>
                <button class="dropdown-add-btn" @click.stop="$emit('add-from-slot', idx, r)">+</button>
              </div>
            </div>
            <p v-else-if="slots[idx].query && !slots[idx].loading" class="slot-no-results">No results found.</p>
          </div>
        </template>
      </div>
    </div>

    <p class="picker-hint">
      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M3 9l9-6 9 6"/><path d="M6 9L3 18a3 3 0 0 0 6 0L6 9z"/><path d="M18 9l-3 9a3 3 0 0 0 6 0L18 9z"/><line x1="3" y1="21" x2="21" y2="21"/></svg>
      {{ facilities.length === 1 ? 'Add 1 more facility to start comparing' : 'Select at least 2 facilities to start comparing' }}
    </p>

    <div class="picker-actions">
      <button class="browse-btn" @click="$emit('go-back')">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Browse all facilities
      </button>
      <button v-if="facilities.length > 0" class="clear-selection-btn" @click="$emit('clear-selection')">
        Clear selection
      </button>
    </div>

  </div>
</template>

<script setup>
defineProps({
  slots: { type: Array, required: true },
  facilities: { type: Array, required: true }
})
defineEmits(['slot-search', 'add-from-slot', 'go-back', 'clear-selection', 'remove-facility'])
</script>

<style scoped>
/* ── PICKER SECTION ── */
.picker-section {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  padding: 20px 0 60px;
}

.picker-hero {
  margin-bottom: 40px;
}

.picker-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #3d6b59;
  background: #e6f4ed;
  border-radius: 999px;
  padding: 5px 14px;
  margin-bottom: 18px;
}

.picker-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 800;
  color: #22332e;
  margin: 0 0 12px;
  line-height: 1.2;
}

.picker-subtitle {
  font-size: 15px;
  color: #7f8d87;
  margin: 0;
}

/* ── Slot cards ── */
.slot-cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(320px, 400px));
  justify-content: center;
  align-items: start;
  gap: 18px;
  text-align: center;
  margin-bottom: 28px;
}

.slot-card {
  background: #fff;
  border: 2px dashed #d9d5cc;
  border-radius: 16px;
  padding: 66px 32px 16px;
  height: 340px;
  width: 100%;
  max-width: none;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.slot-card.slot-card-searching {
  height: auto;
  min-height: 340px;
}

.slot-card:focus-within {
  border-color: #5d8374;
  box-shadow: 0 10px 24px rgba(61, 107, 89, 0.12);
}

.slot-card.slot-card-filled {
  border-color: #b8cec9;
  border-style: solid;
  padding: 0;
  overflow: hidden;
  align-items: stretch;
}

/* Number badge */
.slot-num-badge {
  position: absolute;
  top: 22px;
  left: 22px;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #fff;
  border: 1px solid #e3ded5;
  color: #7f8d87;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(31, 45, 42, 0.06);
}

/* Building icon */
.slot-icon-wrap {
  width: 74px;
  height: 74px;
  background: #3d6b59;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-bottom: 22px;
  flex-shrink: 0;
  box-shadow: 0 10px 20px rgba(61, 107, 89, 0.22);
}

.slot-icon-wrap svg {
  width: 36px;
  height: 36px;
  stroke-width: 1.8;
}

.slot-card-title {
  font-size: 18px;
  font-weight: 800;
  color: #22332e;
  margin-bottom: 8px;
  line-height: 1.25;
}

.slot-card-desc {
  max-width: 220px;
  font-size: 13px;
  color: #7f8d87;
  line-height: 1.45;
  margin: 0 auto 22px;
}

/* Search area */
.slot-search-area {
  margin-top: 0;
  position: relative;
  width: 100%;
  max-width: 420px;
}

.slot-search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.slot-search-icon {
  position: absolute;
  left: 20px;
  color: #8a9e96;
  pointer-events: none;
  z-index: 1;
}

.slot-search-input {
  width: 100%;
  height: 52px;
  padding: 0 18px 0 54px;
  border: 1px solid #e1ddd5;
  border-radius: 999px;
  font-size: 14px;
  color: #22332e;
  background: #fff;
  outline: none;
  box-sizing: border-box;
  box-shadow: 0 4px 14px rgba(31, 45, 42, 0.06);
}
.slot-search-input:focus {
  border-color: #3d6b59;
  box-shadow: 0 0 0 3px rgba(61, 107, 89, 0.12), 0 6px 18px rgba(31, 45, 42, 0.08);
}

.slot-spinner {
  position: absolute;
  right: 20px;
  width: 14px;
  height: 14px;
  border: 2px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Dropdown */
.slot-dropdown {
  margin-top: 10px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  overflow: hidden;
  max-height: 260px;
  overflow-y: auto;
  box-shadow: 0 10px 24px rgba(31, 45, 42, 0.14);
  position: relative;
  z-index: 10;
  text-align: left;
}

.slot-dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  cursor: pointer;
  border-bottom: 1px solid #ede8e0;
  transition: background 0.1s;
}
.slot-dropdown-item:last-child { border-bottom: none; }
.slot-dropdown-item:hover { background: #f3f0ea; }

.dropdown-icon {
  width: 36px;
  height: 36px;
  background: #eef5ef;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3d6b59;
  flex-shrink: 0;
}

.dropdown-info {
  flex: 1;
  min-width: 0;
}

.dropdown-name {
  font-size: 13px;
  font-weight: 700;
  color: #22332e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-meta {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 10.5px;
  color: #8a9e96;
  margin-top: 2px;
}

.dropdown-add-btn {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1.5px solid #3d6b59;
  background: transparent;
  color: #3d6b59;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.1s, color 0.1s;
}
.dropdown-add-btn:hover { background: #3d6b59; color: #fff; }

.slot-no-results {
  font-size: 12px;
  color: #a0a8a4;
  margin: 8px 0 0;
  text-align: center;
}

/* Filled slot content */
.slot-filled-inner {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.slot-filled-img-wrap {
  position: relative;
  width: 100%;
}

.slot-thumb {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 0;
  display: block;
}

.slot-num-badge-filled {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3d6b59;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(31, 45, 42, 0.28);
}

.slot-remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.7);
  background: rgba(255,255,255,0.85);
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7f8d87;
  transition: background 0.1s, color 0.1s;
  z-index: 2;
}
.slot-remove-btn:hover { background: #fdecea; color: #c0392b; border-color: #f5c6c6; }

.slot-info {
  padding: 18px 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.slot-name {
  font-size: 17px;
  font-weight: 700;
  color: #22332e;
  text-align: left;
  line-height: 1.3;
}

.slot-loc {
  font-size: 13px;
  color: #a0a8a4;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

/* Hint & browse */
.picker-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: #8a9e96;
  margin: 0 0 20px;
}

.picker-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}

.browse-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  border: 1.5px solid #c8c1b8;
  background: transparent;
  border-radius: 999px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  color: #4a5e57;
  cursor: pointer;
  transition: background 0.15s;
}
.browse-btn:hover { background: #f0ece4; }

.clear-selection-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 14px;
  font-weight: 500;
  color: #7f8d87;
  cursor: pointer;
  transition: color 0.15s;
}
.clear-selection-btn:hover { color: #22332e; }

/* ── Responsive ── */
@media (max-width: 900px) {
  .slot-cards { grid-template-columns: 1fr 1fr; }
}

@media (min-width: 769px) and (max-width: 1100px) {
  /* Picker slot cards */
  .picker-title { font-size: 28px; }
  .slot-card { height: auto; min-height: 300px; padding: 50px 20px 16px; }
}

@media (max-width: 768px) {
  /* Picker */
  .picker-title { font-size: 26px; }
  .slot-cards { grid-template-columns: 1fr; }
  .slot-card { height: auto; min-height: 300px; padding: 50px 20px 16px; }
}
</style>
