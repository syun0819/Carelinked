<template>
  <div class="compare-page">
    <Header />
    <div class="compare-container page-animate">

      <!-- Global loading (initial fetch when navigating with pre-filled store) -->
      <div v-if="loading" class="state-box">
        <div class="loading-spinner"></div>
        <p>Loading facilities…</p>
      </div>

      <!-- ── PICKER MODE (< 2 facilities loaded) ── -->
      <template v-else-if="!comparisonStarted || facilities.length < 2">
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
                    <button class="slot-remove-btn" @click="removeFacility(facilities[idx].id)" aria-label="Remove facility">×</button>
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
                      @input="onSlotSearch(idx)"
                    />
                    <div v-if="slots[idx].loading" class="slot-spinner"></div>
                  </div>

                  <div v-if="slots[idx].results.length > 0" class="slot-dropdown">
                    <div
                      v-for="r in slots[idx].results"
                      :key="r.id"
                      class="slot-dropdown-item"
                      @click="addFromSlot(idx, r)"
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
                      <button class="dropdown-add-btn" @click.stop="addFromSlot(idx, r)">+</button>
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
            <button class="browse-btn" @click="goBack">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
              Browse all facilities
            </button>
            <button v-if="facilities.length > 0" class="clear-selection-btn" @click="clearSelection">
              Clear selection
            </button>
          </div>

        </div>
      </template>

      <!-- ── COMPARE TABLE MODE (2 or 3 facilities loaded) ── -->
      <template v-else>

        <div class="compare-content-frame">
          <!-- Page header -->
          <div class="compare-header">
            <div class="compare-header-left">
              <h1 class="compare-title">Compare facilities</h1>
              <p class="compare-subtitle">Side-by-side view of wait times, quality, staffing and compliance.</p>
            </div>
            <div class="compare-header-actions">
              <button class="filter-count-btn" :class="{ inactive: !showSectionFilter }" @click="showSectionFilter = !showSectionFilter">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="11" y1="18" x2="13" y2="18"/>
                </svg>
                {{ visibleSections.size }}/{{ sections.length }}
              </button>
              <button class="action-btn-outline" @click="goBack">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                Back to search
              </button>
              <button class="action-btn-outline" @click="clearAll">Clear all</button>
            </div>
          </div>

          <div v-if="!compareStore.isFull" class="add-third-row">
            <button class="add-third-btn" @click="showAddPanel = !showAddPanel">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Add a 3rd facility
            </button>
          </div>

          <!-- Add the optional third facility without leaving compare mode -->
          <div v-if="showAddPanel && !compareStore.isFull" class="table-add-panel">
            <div class="table-add-copy">
              <span class="table-add-kicker">Facility {{ nextFacilityNumber }}</span>
              <strong>Add another facility</strong>
            </div>
            <div class="table-add-search">
              <div class="slot-search-wrap">
                <svg class="slot-search-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                <input
                  v-model="slots[activeAddSlot].query"
                  class="slot-search-input"
                  :placeholder="'Search facility ' + nextFacilityNumber + '…'"
                  @input="onSlotSearch(activeAddSlot)"
                />
                <div v-if="slots[activeAddSlot].loading" class="slot-spinner"></div>
              </div>

              <div v-if="slots[activeAddSlot].results.length > 0" class="slot-dropdown table-add-dropdown">
                <div
                  v-for="r in slots[activeAddSlot].results"
                  :key="r.id"
                  class="slot-dropdown-item"
                  @click="addFromAddPanel(r)"
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
                  <button class="dropdown-add-btn" @click.stop="addFromAddPanel(r)">+</button>
                </div>
              </div>
              <p v-else-if="slots[activeAddSlot].query && !slots[activeAddSlot].loading" class="slot-no-results">No results found.</p>
            </div>
          </div>

          <!-- Section filter chips -->
          <div v-if="showSectionFilter" class="section-filter">
            <span class="filter-label">Show:</span>
            <div class="filter-chips">
              <button
                v-for="s in sections"
                :key="s.key"
                class="filter-chip"
                :class="{ active: visibleSections.has(s.key) }"
                @click="toggleSection(s.key)"
              >{{ s.label }}</button>
            </div>
            <span class="filter-count">{{ visibleSections.size }}/{{ sections.length }}</span>
          </div>

          <!-- Table -->
          <div class="compare-table-wrap">
            <table class="compare-table">
            <colgroup>
              <col class="col-label" />
              <col v-for="(f, i) in facilities" :key="i" :style="{ width: facilityColWidth }" />
            </colgroup>

            <thead>
              <tr class="facility-header-row">
                <th class="label-cell"><span class="facility-label-head">FACILITY</span></th>
                <th v-for="f in facilities" :key="f.id" class="facility-cell">
                  <div class="facility-card-head">
                    <button class="remove-btn" @click="removeFacility(f.id)" aria-label="Remove">
                      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                    </button>
                    <img :src="f.image" :alt="f.name" class="facility-thumb" />
                    <div class="facility-name">{{ f.name }}</div>
                    <div class="facility-location">{{ f.suburb }}, {{ f.state }} {{ f.postcode }}</div>
                  </div>
                </th>
              </tr>
            </thead>

            <tbody>
              <!-- Care type -->
              <tr v-if="visibleSections.has('overview')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Care type</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.careType">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.careType }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span class="value-text">{{ f.careType || 'N/A' }}</span>
                </td>
              </tr>

              <!-- Availability -->
              <tr v-if="visibleSections.has('waitTime')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Availability</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.availability">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.availability }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span class="value-text" :class="availabilityClass(f.bedAvailability)">{{ f.bedAvailability || 'Unknown' }}</span>
                </td>
              </tr>

              <!-- Overall rating -->
              <tr v-if="visibleSections.has('qualityRatings')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Overall rating</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.overallRating">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.overallRating }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <div class="stars-row">
                    <template v-if="f.overallStarRating != null">
                      <span v-for="i in starsFor(f.overallStarRating).full" :key="'f'+i" class="star filled">★</span>
                      <span v-for="i in starsFor(f.overallStarRating).empty" :key="'e'+i" class="star empty">★</span>
                      <span class="star-num">{{ f.overallStarRating.toFixed(1) }}</span>
                      <span v-if="isHighest(f, 'overallStarRating')" class="best-badge">
                        <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                        Highest rated
                      </span>
                    </template>
                    <span v-else class="na-text">N/A</span>
                  </div>
                </td>
              </tr>

              <!-- Resident experience rating -->
              <tr v-if="visibleSections.has('qualityRatings')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Resident experience rating</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.residentExperienceRating">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.residentExperienceRating }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <div class="stars-row">
                    <template v-if="f.residentsExperienceRating != null">
                      <span v-for="i in starsFor(f.residentsExperienceRating).full" :key="'f'+i" class="star filled">★</span>
                      <span v-for="i in starsFor(f.residentsExperienceRating).empty" :key="'e'+i" class="star empty">★</span>
                      <span class="star-num">{{ f.residentsExperienceRating.toFixed(1) }}</span>
                    </template>
                    <span v-else class="na-text">N/A</span>
                  </div>
                </td>
              </tr>

              <!-- Staffing rating -->
              <tr v-if="visibleSections.has('qualityRatings')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Staffing rating</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.staffingRating">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.staffingRating }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <div class="stars-row">
                    <template v-if="f.staffingRating != null">
                      <span v-for="i in starsFor(f.staffingRating).full" :key="'f'+i" class="star filled">★</span>
                      <span v-for="i in starsFor(f.staffingRating).empty" :key="'e'+i" class="star empty">★</span>
                      <span class="star-num">{{ f.staffingRating.toFixed(1) }}</span>
                    </template>
                    <span v-else class="na-text">N/A</span>
                  </div>
                </td>
              </tr>

              <!-- Compliance rating -->
              <tr v-if="visibleSections.has('qualityRatings')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Compliance rating</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.complianceRating">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.complianceRating }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <div class="stars-row">
                    <template v-if="f.complianceRating != null">
                      <span v-for="i in starsFor(f.complianceRating).full" :key="'f'+i" class="star filled">★</span>
                      <span v-for="i in starsFor(f.complianceRating).empty" :key="'e'+i" class="star empty">★</span>
                      <span class="star-num">{{ f.complianceRating.toFixed(1) }}</span>
                    </template>
                    <span v-else class="na-text">N/A</span>
                  </div>
                </td>
              </tr>

              <!-- Quality measures rating -->
              <tr v-if="visibleSections.has('qualityRatings')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Quality measures rating</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.qualityMeasuresRating">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.qualityMeasuresRating }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <div class="stars-row">
                    <template v-if="f.qualityMeasuresRating != null">
                      <span v-for="i in starsFor(f.qualityMeasuresRating).full" :key="'f'+i" class="star filled">★</span>
                      <span v-for="i in starsFor(f.qualityMeasuresRating).empty" :key="'e'+i" class="star empty">★</span>
                      <span class="star-num">{{ f.qualityMeasuresRating.toFixed(1) }}</span>
                    </template>
                    <span v-else class="na-text">N/A</span>
                  </div>
                </td>
              </tr>

              <!-- Total beds -->
              <tr v-if="visibleSections.has('overview')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Total beds</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.totalBeds">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.totalBeds }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span class="value-text">{{ f.totalBeds ?? 'N/A' }}</span>
                </td>
              </tr>

              <!-- RN care minutes -->
              <tr v-if="visibleSections.has('staffing')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>RN care minutes <span class="label-sub">(actual / target)</span></span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.rnCareMinutes">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.rnCareMinutes }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span v-if="f.sRnCareMinutesActual != null" class="value-text">
                    {{ Math.round(f.sRnCareMinutesActual) }} / {{ Math.round(f.sRnCareMinutesTarget) }} mins
                  </span>
                  <span v-else class="na-text">N/A</span>
                  <span v-if="f.sRnCareMinutesActual != null" class="met-badge" :class="f.rnMinutesMet ? 'badge-met' : 'badge-unmet'">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline v-if="f.rnMinutesMet" points="20 6 9 17 4 12"/>
                      <circle v-else cx="12" cy="12" r="10"/><line v-if="!f.rnMinutesMet" x1="12" y1="8" x2="12" y2="12"/><line v-if="!f.rnMinutesMet" x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    {{ f.rnMinutesMet ? 'Met' : 'Not met' }}
                  </span>
                </td>
              </tr>

              <!-- Total care minutes -->
              <tr v-if="visibleSections.has('staffing')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Total care minutes <span class="label-sub">(actual / target)</span></span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.totalCareMinutes">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.totalCareMinutes }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span v-if="f.sTotalCareMinutesActual != null" class="value-text">
                    {{ Math.round(f.sTotalCareMinutesActual) }} / {{ Math.round(f.sTotalCareMinutesTarget) }} mins
                  </span>
                  <span v-else class="na-text">N/A</span>
                  <span v-if="f.sTotalCareMinutesActual != null" class="met-badge" :class="f.totalMinutesMet ? 'badge-met' : 'badge-unmet'">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline v-if="f.totalMinutesMet" points="20 6 9 17 4 12"/>
                      <circle v-else cx="12" cy="12" r="10"/><line v-if="!f.totalMinutesMet" x1="12" y1="8" x2="12" y2="12"/><line v-if="!f.totalMinutesMet" x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    {{ f.totalMinutesMet ? 'Met' : 'Not met' }}
                  </span>
                </td>
              </tr>

              <!-- Compliance status -->
              <tr v-if="visibleSections.has('compliance')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Compliance status</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.complianceStatus">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.complianceStatus }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span v-if="f.sRnCareMinutesActual != null" class="compliance-badge" :class="(f.rnMinutesMet && f.totalMinutesMet) ? 'compliance-ok' : 'compliance-action'">
                    {{ (f.rnMinutesMet && f.totalMinutesMet) ? 'No issues' : 'Action taken' }}
                  </span>
                  <span v-else class="na-text">N/A</span>
                </td>
              </tr>

              <!-- Resident scores -->
              <tr v-if="visibleSections.has('residentExperience')" v-for="rs in residentScoreRows" :key="rs.key" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>{{ rs.label }}</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo[rs.key]">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo[rs.key] }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span v-if="f[rs.key] != null" class="value-text">{{ Math.round((f[rs.key] / 5) * 100) }}%</span>
                  <span v-else class="na-text">N/A</span>
                </td>
              </tr>

              <!-- Government funding -->
              <tr v-if="visibleSections.has('providerFunding')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Government funding</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.governmentFunding">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.governmentFunding }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span class="value-text">{{ formatFunding(f.governmentFunding) }}</span>
                </td>
              </tr>

              <!-- Provider -->
              <tr v-if="visibleSections.has('providerFunding')" class="compare-row">
                <td class="label-cell">
                  <span class="label-with-help">
                    <span>Provider</span>
                    <button class="info-dot" type="button" :aria-label="fieldInfo.provider">
                      i
                      <span class="info-tooltip" role="tooltip">{{ fieldInfo.provider }}</span>
                    </button>
                  </span>
                </td>
                <td v-for="f in facilities" :key="f.id" class="data-cell">
                  <span class="value-text">{{ f.provider || 'N/A' }}</span>
                </td>
              </tr>
            </tbody>

            <tfoot>
              <tr>
                <td class="label-cell"></td>
                <td v-for="f in facilities" :key="f.id" class="data-cell footer-cell">
                  <button class="view-btn" @click="goToDetail(f.id)">View full details</button>
                </td>
              </tr>
            </tfoot>
            </table>
          </div>
        </div>

      </template>

    </div>
    <FooterSection />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import FooterSection from '../components/FooterSection.vue'
import { useCompareStore } from '../stores/compareStore'
import { getFacilityDetail, searchFacilities } from '../services/facilitiesApi'
import { mapFacilityDetail, mapFacilityCard } from '../utils/facilityMappers'

const router = useRouter()
const route = useRoute()
const compareStore = useCompareStore()

const shouldShowResults = computed(() =>
  route.query.mode === 'results' &&
  compareStore.count >= compareStore.initialSelectionLimit
)
const shouldKeepSelection = computed(() => route.query.keepSelection === '1')
const facilities = ref([])
const loading = ref(shouldShowResults.value && compareStore.items.length > 0)
const comparisonStarted = ref(shouldShowResults.value)

const sections = [
  { key: 'overview',           label: 'Overview' },
  { key: 'waitTime',           label: 'Availability' },
  { key: 'qualityRatings',     label: 'Quality Ratings' },
  { key: 'staffing',           label: 'Staffing' },
  { key: 'compliance',         label: 'Compliance' },
  { key: 'residentExperience', label: 'Resident Experience' },
  { key: 'providerFunding',    label: 'Provider & Funding' },
]

const fieldInfo = {
  careType: 'The type of aged care service offered, such as residential care.',
  availability: 'Bed availability estimation based on current occupancy data. Indicates how likely a place is available at this facility.',
  overallRating: 'The overall star rating summarising quality, care, staffing and compliance signals.',
  residentExperienceRating: 'A rating based on resident experience feedback, including how residents feel about daily life and care.',
  staffingRating: 'A star rating that reflects staffing performance and care minute information.',
  complianceRating: 'A rating that reflects compliance history and whether regulatory concerns have been identified.',
  qualityMeasuresRating: 'A rating based on reported quality measures and care outcome indicators.',
  totalBeds: 'The total number of approved aged care places or beds available at the facility.',
  rnCareMinutes: 'Registered nurse care minutes delivered per resident per day compared with the target.',
  totalCareMinutes: 'Total direct care minutes delivered per resident per day compared with the target.',
  complianceStatus: 'A summary of whether staffing targets are met or whether action may be needed.',
  reFoodScore: 'Resident feedback score for food quality and meal experience.',
  reSafetyScore: 'Resident feedback score for feeling safe at the facility.',
  reRespectScore: 'Resident feedback score for being treated with respect.',
  reCaringScore: 'Resident feedback score for whether staff are caring and supportive.',
  reHomeScore: 'Resident feedback score for whether the facility feels like home.',
  governmentFunding: 'The amount of government funding reported for the facility.',
  provider: 'The organisation responsible for operating the facility.'
}

const visibleSections = ref(new Set(sections.map(s => s.key)))
const showSectionFilter = ref(true)
const showAddPanel = ref(false)

function toggleSection(key) {
  const s = new Set(visibleSections.value)
  s.has(key) ? s.delete(key) : s.add(key)
  visibleSections.value = s
}

// Per-slot search state
const slots = reactive([
  { query: '', results: [], loading: false },
  { query: '', results: [], loading: false },
  { query: '', results: [], loading: false },
])
const slotTimers = [null, null, null]

const facilityColWidth = computed(() =>
  `calc((100% - 160px) / ${facilities.value.length || 1})`
)
const activeAddSlot = computed(() => Math.min(facilities.value.length, slots.length - 1))
const nextFacilityNumber = computed(() => facilities.value.length + 1)

function onSlotSearch(idx) {
  clearTimeout(slotTimers[idx])
  const q = slots[idx].query.trim()
  if (!q) { slots[idx].results = []; return }
  slots[idx].loading = true
  slotTimers[idx] = setTimeout(async () => {
    try {
      const data = await searchFacilities({ keyword: q, limit: 6 })
      slots[idx].results = (data.results || data.items || [])
        .map(mapFacilityCard)
        .filter(r => !compareStore.has(r.id))
    } finally {
      slots[idx].loading = false
    }
  }, 350)
}

async function addFromSlot(idx, r) {
  if (compareStore.has(r.id) || compareStore.isFull) return
  compareStore.add(r.id, r.name)
  slots[idx].loading = true
  try {
    const detail = await getFacilityDetail(r.id).then(mapFacilityDetail)
    facilities.value = [...facilities.value, detail]
    if (facilities.value.length >= compareStore.initialSelectionLimit) {
      comparisonStarted.value = true
      router.replace({ path: '/compare', query: { mode: 'results' } })
    }
  } finally {
    slots[idx].loading = false
  }
  slots[idx].query = ''
  slots[idx].results = []
}

async function addFromAddPanel(r) {
  await addFromSlot(activeAddSlot.value, r)
  showAddPanel.value = false
}

const residentScoreRows = [
  { key: 'reFoodScore',    label: 'Resident - Food' },
  { key: 'reSafetyScore',  label: 'Resident - Safety' },
  { key: 'reRespectScore', label: 'Resident - Respect' },
  { key: 'reCaringScore',  label: 'Resident - Caring' },
  { key: 'reHomeScore',    label: 'Resident - Feeling at Home' },
]

onUnmounted(() => {
  compareStore.clear()
})

async function loadSelectedFacilities() {
  if (compareStore.items.length === 0) return
  loading.value = true
  try {
    const results = await Promise.all(
      compareStore.items.map(({ id }) => getFacilityDetail(id).then(mapFacilityDetail))
    )
    facilities.value = results
    comparisonStarted.value = shouldShowResults.value
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!shouldShowResults.value && !shouldKeepSelection.value) {
    compareStore.clear()
    facilities.value = []
    comparisonStarted.value = false
    loading.value = false
    return
  }

  await loadSelectedFacilities()
})

watch(() => [route.query.mode, route.query.keepSelection], async ([mode, keepSelection]) => {
  if (mode === 'results' || keepSelection === '1') {
    await loadSelectedFacilities()
    return
  }

  compareStore.clear()
  facilities.value = []
  comparisonStarted.value = false
  loading.value = false
  showAddPanel.value = false
})

function availabilityClass(val) {
  if (val === 'Likely Available') return 'avail-likely'
  if (val === 'Potentially Available') return 'avail-potential'
  if (val === 'Constrained by Market' || val === 'Constrained by Size') return 'avail-constrained'
  if (val === 'Highly Constrained') return 'avail-highly-constrained'
  if (val === 'Does Not Provide This Service') return 'avail-none'
  return ''
}

function starsFor(val) {
  const full = Math.max(0, Math.min(5, Math.round(val ?? 0)))
  return { full, empty: 5 - full }
}

function isHighest(facility, key) {
  if (facilities.value.length < 3) return false
  if (facility[key] == null) return false
  const vals = facilities.value.map(f => f[key] ?? -Infinity)
  const max = Math.max(...vals)
  return facility[key] === max
}

function formatFunding(val) {
  if (val == null || val === '') return 'N/A'
  return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 }).format(val)
}

function removeFacility(id) {
  compareStore.remove(id)
  facilities.value = facilities.value.filter(f => f.id !== id)
}

function clearSelection() {
  compareStore.clear()
  facilities.value = []
  comparisonStarted.value = false
  showAddPanel.value = false
  slots.forEach(slot => {
    slot.query = ''
    slot.results = []
    slot.loading = false
  })
}

function clearAll() {
  compareStore.clear()
  facilities.value = []
  showAddPanel.value = false
  comparisonStarted.value = false
}

function goBack() {
  router.push('/find-bed')
}

function goToDetail(id) {
  router.push(`/facility/${id}`)
}
</script>

<style scoped>
.compare-page {
  background: #f7f4ee;
  min-height: 100vh;
}

.compare-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 110px 32px 80px;
}

/* ── Global loading ── */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: #7f8d87;
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #ddd5ca;
  border-top-color: #3d6b59;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

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

/* ── COMPARE TABLE HEADER ── */
.compare-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 28px;
}

.compare-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  color: #22332e;
  margin: 0 0 4px;
}

.compare-subtitle {
  font-size: 14px;
  color: #7f8d87;
  margin: 0;
}

.compare-header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.action-btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #c8c1b8;
  background: #fff;
  border-radius: 7px;
  padding: 4px 16px;
  font-size: 13px;
  font-weight: 500;
  color: #4a5e57;
  cursor: pointer;
  transition: background 0.15s;
}
.action-btn-outline:hover { background: #f0ece4; }

.add-third-row {
  display: flex;
  justify-content: flex-end;
  margin: -16px 0 16px;
  padding-right: 2px;
}

.add-third-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1.5px dashed #aeb9b3;
  background: transparent;
  border-radius: 999px;
  padding: 7px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #4a6659;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.add-third-btn:hover {
  background: #eef5ef;
  border-color: #4a6659;
  color: #2e5244;
}

.table-add-panel {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 16px;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  padding: 14px 16px;
}

.table-add-copy {
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  color: #22332e;
}

.table-add-copy strong {
  font-size: 14px;
}

.table-add-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #3d6b59;
}

.table-add-search {
  flex: 1;
  min-width: 240px;
  position: relative;
}

.table-add-dropdown {
  position: absolute;
  left: 0;
  right: 0;
}

.table-add-dropdown .slot-dropdown-item {
  gap: 16px;
  padding: 14px 20px;
}

.table-add-dropdown .dropdown-info {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) minmax(160px, 0.65fr);
  align-items: center;
  gap: 20px;
}

.table-add-dropdown .dropdown-name {
  font-size: 14px;
  line-height: 1.25;
}

.table-add-dropdown .dropdown-meta {
  margin-top: 0;
  justify-content: flex-start;
  text-transform: uppercase;
  white-space: nowrap;
}

.table-add-dropdown .dropdown-add-btn {
  width: 30px;
  height: 30px;
  font-size: 20px;
}

.filter-count-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #3d6b59;
  background: #3d6b59;
  color: #fff;
  border-radius: 7px;
  padding: 4px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.filter-count-btn.inactive {
  background: #fff;
  color: #4a5e57;
}

/* ── Section filter chips ── */
.compare-content-frame {
  width: min(100%, 1160px);
  margin: 0 auto;
}

.section-filter {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  flex-wrap: wrap;
  background: #fff;
  border: 1px solid #ddd5ca;
  border-radius: 10px;
  padding: 10px 16px;
}

.filter-label {
  font-size: 13px;
  font-weight: 600;
  color: #7f8d87;
  flex-shrink: 0;
}

.filter-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  flex: 1;
}

.filter-chip {
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid #ccc7be;
  background: transparent;
  color: #7f8d87;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.filter-chip:hover { border-color: #3d6b59; color: #3d6b59; }
.filter-chip.active { background: #3d6b59; border-color: #3d6b59; color: #fff; }

.filter-count {
  font-size: 13px;
  font-weight: 600;
  color: #7f8d87;
  flex-shrink: 0;
}

/* ── Table ── */
.compare-table-wrap {
  overflow-x: auto;
  padding: 0;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #ece9e3;
  border-radius: 14px;
  overflow: hidden;
  table-layout: fixed;
}

col.col-label { width: 160px; }

.facility-header-row th {
  background: #fff;
  padding: 0;
  vertical-align: middle;
  border-bottom: 1px solid #ece9e3;
}

.facility-header-row th.label-cell {
  background: #f7f7f6;
}

.label-cell {
  padding: 0 14px;
  font-size: 14px;
  font-weight: 400;
  color: #6f6f6f;
  text-align: left;
  vertical-align: middle;
  border-right: 1px solid #ece9e3;
  background: #f7f7f6;
  line-height: 1.4;
  position: relative;
}

.facility-label-head {
  font-size: 14px;
  font-weight: 500;
  color: #6f6f6f;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding-left: 12px;
}

.label-sub {
  font-size: 11px;
  font-weight: 400;
  color: #7f7f7f;
}

.label-with-help {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  width: 100%;
}

.info-dot {
  width: 15px;
  height: 15px;
  border: 1.5px solid #7b817e;
  border-radius: 50%;
  background: transparent;
  color: #6f7471;
  font-size: 10px;
  font-weight: 700;
  line-height: 1;
  padding: 0;
  cursor: help;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  position: relative;
}

.info-tooltip {
  position: absolute;
  left: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
  width: 230px;
  padding: 9px 11px;
  border-radius: 8px;
  background: #22332e;
  color: #fff;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.35;
  text-align: left;
  box-shadow: 0 8px 22px rgba(31, 45, 42, 0.18);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  z-index: 30;
}

.info-tooltip::before {
  content: "";
  position: absolute;
  left: -5px;
  top: 50%;
  width: 10px;
  height: 10px;
  background: #22332e;
  transform: translateY(-50%) rotate(45deg);
}

.info-dot:hover .info-tooltip,
.info-dot:focus-visible .info-tooltip {
  opacity: 1;
  visibility: visible;
}

.facility-cell {
  padding: 0;
  text-align: center;
  border-right: 1px solid #ece9e3;
  vertical-align: top;
}
.facility-cell:last-child { border-right: none; }

.facility-card-head {
  position: relative;
  padding: 20px 20px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1px solid #ddd5ca;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7f8d87;
}
.remove-btn:hover { background: #fdecea; color: #c0392b; border-color: #f5c6c6; }

.facility-thumb {
  width: 100%;
  height: 140px;
  flex: 0 0 140px;
  object-fit: cover;
  border-radius: 10px;
}

.facility-name {
  font-size: 14px;
  font-weight: 700;
  color: #22332e;
  text-align: center;
  line-height: 1.3;
  min-height: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.facility-location {
  font-size: 12px;
  color: #a0a8a4;
  text-align: center;
  min-height: 0;
  margin-top: 0;
}

/* ── Data rows ── */
.compare-row { height: 62px; }

.compare-row td {
  height: 62px;
  border-bottom: 1px solid #ece9e3;
  vertical-align: middle;
}

.compare-row:last-child td { border-bottom: none; }

.data-cell {
  padding: 0 20px;
  text-align: center;
  border-right: 1px solid #ece9e3;
  font-size: 14px;
  vertical-align: middle;
  position: relative;
}
.data-cell:last-child { border-right: none; }

.value-text { font-weight: 600; color: #22332e; }

.avail-likely              { color: #4f7a62; }
.avail-potential           { color: #c9a200; }
.avail-constrained         { color: #d9822b; }
.avail-highly-constrained  { color: #c53b2c; }
.avail-none                { color: #9e9e9e; }
.na-text { color: #b0bdb8; font-size: 13px; }

/* ── Stars ── */
.stars-row {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  flex-wrap: wrap;
  justify-content: center;
}
.star { font-size: 15px; line-height: 1; }
.star.filled { color: #e8a023; }
.star.empty  { color: #d8d0c4; }
.star-num { margin-left: 4px; font-size: 13px; font-weight: 700; color: #22332e; }

/* ── Badges ── */
.best-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
  background: #e6f4ed;
  color: #2e7d5a;
  padding: 2px 8px;
  border-radius: 999px;
  white-space: nowrap;
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
}

.met-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
  white-space: nowrap;
}
.badge-met   { background: #e6f4ed; color: #2e7d5a; }
.badge-unmet { background: #fdecea; color: #c0392b; }

.compliance-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.compliance-ok     { background: #e6f4ed; color: #2e7d5a; }
.compliance-action { background: #fef3e2; color: #c07a40; }

/* ── Footer ── */
tfoot tr td {
  border-top: 1px solid #ece9e3;
}

.footer-cell { padding: 18px 20px; }

.view-btn {
  width: 100%;
  background: #3d6b59;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 11px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.view-btn:hover { background: #2e5244; }

/* ── Responsive ── */
@media (max-width: 900px) {
  .slot-cards { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 768px) {
  .compare-container { padding: 90px 16px 60px; }
  .picker-title { font-size: 26px; }
  .slot-cards { grid-template-columns: 1fr; }
  .add-third-row { justify-content: flex-start; margin: -8px 0 14px; }
  .table-add-panel { flex-direction: column; }
  .table-add-copy,
  .table-add-search { width: 100%; min-width: 0; }
  .table-add-dropdown .dropdown-info {
    display: block;
  }
  .table-add-dropdown .dropdown-meta {
    margin-top: 2px;
    white-space: normal;
  }
  col.col-label { width: 120px; }
  .label-cell { padding: 10px 10px; font-size: 11px; }
  .data-cell { padding: 10px 10px; font-size: 12px; }
  .facility-thumb { height: 100px; }
}
</style>
