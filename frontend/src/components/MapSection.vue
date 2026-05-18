<template>
  <div class="map-section">

    <div class="overlay-bar" aria-label="Map overlay selector">
      <div class="overlay-bar-left">
        <span class="overlay-label">Overlay</span>
        <button
          class="overlay-btn"
          :class="{ active: activeOverlay === 'environmental' }"
          :disabled="overlayLoading"
          @click="toggleOverlay('environmental')"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
            <path d="M13.5 2.5S8 1.5 5 4.5C2 7.5 3 13.5 3 13.5S9 12 12 9C15 6 13.5 2.5 13.5 2.5Z"/>
            <path d="M3 13.5L7.5 9" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" fill="none"/>
          </svg>
          Bushfire Risk
        </button>
        <button
          class="overlay-btn"
          :class="{ active: activeOverlay === 'demand' }"
          :disabled="overlayLoading"
          @click="toggleOverlay('demand')"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
            <rect x="0.5" y="6" width="4" height="9.5" rx="0.5"/>
            <rect x="6" y="3" width="4" height="12.5" rx="0.5"/>
            <rect x="11.5" y="0.5" width="4" height="15" rx="0.5"/>
          </svg>
          Demand
        </button>
        <button
          class="overlay-btn"
          :class="{ active: activeOverlay === 'crime' }"
          :disabled="overlayLoading"
          @click="toggleOverlay('crime')"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">
            <path d="M8 2L1.5 14H14.5L8 2Z"/>
            <line x1="8" y1="6.5" x2="8" y2="10"/>
            <circle cx="8" cy="12.2" r="0.7" fill="currentColor" stroke="none"/>
          </svg>
          Crime
        </button>
        <button
          class="overlay-btn"
          :class="{ active: activeOverlay === 'heatrisk' }"
          :disabled="overlayLoading"
          @click="toggleOverlay('heatrisk')"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
            <circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
            <path d="M8 4 Q10 6 8 8 Q6 10 8 12" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" fill="none"/>
          </svg>
          Heat Risk
        </button>
      </div>
      <span class="overlay-hint">Only one overlay allowed</span>
    </div>

    <div v-if="loading" class="map-state">Loading map...</div>
    <div v-else-if="error" class="map-state error">{{ error }}</div>
    <div v-show="!loading && !error" class="map-wrapper">
      <div
        v-if="!loading && !error && markers.length === 0 && hasSearched"
        class="map-no-results"
      >
        No facilities found. Try adjusting filters.
      </div>
      <div ref="mapEl" class="map-container"></div>

      <div
        v-if="activeOverlay === 'crime'"
        class="crime-year-control"
        @click.stop
        @mousedown.stop
        @dblclick.stop
        @wheel.stop
      >
        <label class="crime-year-label" for="crime-year-select">Year</label>
        <select
          id="crime-year-select"
          v-model.number="selectedCrimeYear"
          class="crime-year-select"
          :disabled="crimeYears.length === 0"
        >
          <option v-for="year in crimeYears" :key="year" :value="year">
            {{ year }}
          </option>
          <option v-if="crimeYears.length === 0" value="">
            Loading
          </option>
        </select>
      </div>

      <div class="map-legends-container">
        <!-- Overlay-specific legend -->
        <div v-if="activeOverlay === 'environmental'" class="map-legend choropleth-legend" aria-label="Bushfire legend">
          <div class="legend-title">Bushfire Activity</div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#9d0208"></span>
            <span>Extreme (&gt; 85th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f94144"></span>
            <span>Very High (70–85th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f3722c"></span>
            <span>High (55–70th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f9c74f"></span>
            <span>Moderate (40–55th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#a7c957"></span>
            <span>Low (25–40th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#52b788"></span>
            <span>Very Low (10–25th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#1e7145"></span>
            <span>Minimal (≤ 10th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#e9ecef"></span>
            <span>No data</span>
          </div>
        </div>

        <div v-else-if="activeOverlay === 'demand'" class="map-legend choropleth-legend" aria-label="Demand legend">
          <div class="legend-title">Supply / Demand Ratio</div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#1a7a4a"></span>
            <span>Very High (&gt; 80th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#74c476"></span>
            <span>High (60–80th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f7e07a"></span>
            <span>Medium (40–60th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f4923a"></span>
            <span>Low (20–40th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#d64545"></span>
            <span>Very Low (≤ 20th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#cccccc"></span>
            <span>No data</span>
          </div>
        </div>

        <div v-else-if="activeOverlay === 'crime'" class="map-legend choropleth-legend" aria-label="Crime rate legend">
          <div class="legend-title legend-title-spread">
            <span>Crime Rate</span>
            <span class="legend-info" tabindex="0" aria-label="Average normalised offence rate">
              i
              <span class="legend-info-tooltip" role="tooltip">Average normalised offence rate</span>
            </span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#d64545"></span>
            <span>&gt; 15,000</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f4923a"></span>
            <span>7,001 - 15,000</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f7e07a"></span>
            <span>3,001 - 7,000</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#74c476"></span>
            <span>1,001 - 3,000</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#1a7a4a"></span>
            <span>0 - 1,000</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#cccccc"></span>
            <span>No data</span>
          </div>
        </div>

        <div v-else-if="activeOverlay === 'heatrisk'" class="map-legend choropleth-legend" aria-label="Heat risk legend">
          <div class="legend-title">Facility Heat Risk</div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#9d0208"></span>
            <span>Very High (&gt; 80th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f3722c"></span>
            <span>High (60–80th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f9c74f"></span>
            <span>Moderate (40–60th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#52b788"></span>
            <span>Low (20–40th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#1e7145"></span>
            <span>Very Low (≤ 20th pct)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#adb5bd"></span>
            <span>No score data</span>
          </div>
        </div>

        <!-- Availability legend — always shown -->
        <div class="map-legend" aria-label="Availability legend">
          <div class="legend-title">
            Availability
            <svg width="11" height="11" viewBox="0 0 16 16" fill="#5e706a" aria-hidden="true">
              <path d="M8 1a5 5 0 0 0-5 5c0 3.5 5 9 5 9s5-5.5 5-9a5 5 0 0 0-5-5zm0 6.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
            </svg>
          </div>
          <div class="legend-item">
            <span class="legend-dot legend-likely"></span>
            <span>Likely Available</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot legend-potential"></span>
            <span>Potentially Available</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot legend-constrained"></span>
            <span>Constrained</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot legend-highly-constrained"></span>
            <span>Highly Constrained</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot legend-unavailable"></span>
            <span>Not Provided / Unknown</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import L from 'leaflet'
import { getMapFacilities, getHeatmapDemand, getHeatmapBushfire, getHeatmapCrime, getHeatmapLgaBoundaries, getHeatmapHeatRisk } from '../services/facilitiesApi'
import { mapFacilityMarker } from '../utils/facilityMappers'

const props = defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  selectedCareTypes: {
    type: Array,
    default: () => []
  },
  distance: {
    type: Number,
    default: 10
  },
  userLat: {
    type: Number,
    default: null
  },
  userLng: {
    type: Number,
    default: null
  },
  focusLat: {
    type: Number,
    default: null
  },
  focusLng: {
    type: Number,
    default: null
  },
  isActive: {
    type: Boolean,
    default: true
  },
  distanceFilterEnabled: {
    type: Boolean,
    default: false
  },
  searchType: {
    type: String,
    default: ''
  }
})

const mapEl = ref(null)
const loading = ref(false)
const error = ref('')
const hasSearched = ref(false)
const markers = ref([])
const allMarkersCache = ref([])

let map = null
let markersLayer = null
let userMarker = null
let preCreatedMarkers = []
const visibleSet = new Set()
let choropletheLayer = null
let lgaGeoJson = null
let environmentalLayer = null
let heatRiskLayer = null
let heatRiskCache = null
let bushfireCache = null
const crimeCache = new Map()

const activeOverlay = ref(null)
const overlayLoading = ref(false)
const fallbackCrimeYears = Array.from({ length: 12 }, (_, index) => 2024 - index)
const selectedCrimeYear = ref(fallbackCrimeYears[0])
const crimeYears = ref([...fallbackCrimeYears])

const defaultCenter = [-37.8136, 144.9631]
const defaultZoom = 12
function escapeHtml(str) {
  if (str == null) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

const emit = defineEmits(['update:count'])

const careTypeMap = {
  'Residential Aged Care': 'Residential',
  'Residential Care': 'Residential',
  'Residential': 'Residential',
  'Home Care Package (HCP)': 'Home Care',
  'Home Care': 'Home Care',
  'Transition Care': 'Transition Care',
  'Short-Term Restorative Care (STRC)': 'Short-Term Restorative Care (STRC)',
  'Multi-Purpose Service': 'Multi-Purpose Service',
  'National Aboriginal and Torres Strait Islander Aged Care Program':
    'National Aboriginal and Torres Strait Islander Aged Care Program',
  'Indigenous Care': 'National Aboriginal and Torres Strait Islander Aged Care Program'
}

function buildParams() {
  const params = {}
  const q = props.searchQuery.trim()

  if (q) {
    const type = (props.searchType || '').toLowerCase()
    if (type === 'suburb') {
      params.suburb = q
    } else if (type === 'region') {
      params.region = q
    } else if (type === 'postcode' || /^\d+$/.test(q)) {
      params.postcode = q
    } else {
      params.keyword = q
    }
  }

  if (props.selectedCareTypes.length > 0) {
    const mappedTypes = props.selectedCareTypes
      .map(t => careTypeMap[t])
      .filter(Boolean)
    if (mappedTypes.length > 0) {
      params.care_type = mappedTypes
    }
  }

  if (props.distanceFilterEnabled && props.distance != null) {
    params.max_distance_km = props.distance
  }

  return params
}

function getMarkerColor(availability) {
 if (availability === 'Likely Available') return '#4f7a62'
  if (availability === 'Potentially Available') return '#f5c518'
  if (availability === 'Constrained by Market' || availability === 'Constrained by Size') return '#d9822b'
  if (availability === 'Highly Constrained') return '#d64545'
  if (availability === 'Does Not Provide This Service') return '#9e9e9e'
  return '#9e9e9e'
}

function createCustomIcon(color) {
  return L.divIcon({
    className: 'custom-marker-wrapper',
    html: `
      <div class="custom-marker" style="background:${color}">
        <div class="custom-marker-inner"></div>
      </div>
    `,
    iconSize: [26, 26],
    iconAnchor: [13, 26],
    popupAnchor: [0, -28]
  })
}

function initMap() {
  if (map || !mapEl.value) return

  map = L.map(mapEl.value).setView(defaultCenter, defaultZoom)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)

  const hrPane = map.createPane('heatRiskPane')
  hrPane.style.zIndex = 650
  map.getPane('tooltipPane').style.zIndex = 700
  map.getPane('popupPane').style.zIndex = 750

  let _filterTimer = null
  map.on('moveend zoomend', () => {
    clearTimeout(_filterTimer)
    _filterTimer = setTimeout(filterByViewport, 150)
  })

  renderUserMarker()
}

function invalidateMapSize() {
  nextTick(() => {
    setTimeout(() => {
      if (map) {
        map.invalidateSize()
      }
    }, 150)
  })
}

function hasFocusCoordinates() {
  return Number.isFinite(props.focusLat) && Number.isFinite(props.focusLng)
}

function focusMapOnSelectedFacility() {
  if (!map || !hasFocusCoordinates()) return
  map.setView([props.focusLat, props.focusLng], 15)
}

function clearMarkers() {
  if (markersLayer) {
    markersLayer.clearLayers()
  }

  if (map && userMarker) {
    map.removeLayer(userMarker)
    userMarker = null
  }
}

function renderUserMarker() {
  if (!map) return

  if (userMarker) {
    map.removeLayer(userMarker)
    userMarker = null
  }

  if (props.userLat != null && props.userLng != null) {
    userMarker = L.circleMarker([props.userLat, props.userLng], {
      radius: 8,
      weight: 2,
      color: '#2f5d50',
      fillColor: '#2f5d50',
      fillOpacity: 0.9
    }).addTo(map)

    userMarker.bindPopup('Your location')
  }
}

function offsetDuplicateCoordinates(facilities) {
  const countMap = {}

  facilities.forEach(facility => {
    if (facility.latitude == null || facility.longitude == null) return
    const key = `${facility.latitude},${facility.longitude}`
    countMap[key] = (countMap[key] || 0) + 1
  })

  const indexMap = {}
  const result = facilities.map(facility => {
    if (facility.latitude == null || facility.longitude == null) {
      return facility
    }
    const key = `${facility.latitude},${facility.longitude}`

    if (countMap[key] === 1) return facility

    indexMap[key] = (indexMap[key] ?? -1) + 1
    const index = indexMap[key]
    const total = countMap[key]
    const offset = 0.0008
    const angle = (2 * Math.PI * index) / total

    return {
      ...facility,
      latitude: facility.latitude + offset * Math.cos(angle),
      longitude: facility.longitude + offset * Math.sin(angle)
    }
  })
  return result
}

function renderMarkers() {
  if (!map || !markersLayer) return

  markersLayer.clearLayers()
  renderUserMarker()

  const validMarkers = offsetDuplicateCoordinates(
    markers.value.filter((item) => item.latitude != null && item.longitude != null)
  )

  if (validMarkers.length === 0) {
    markersLayer.clearLayers()
    invalidateMapSize()
    return
  }

  validMarkers.forEach((item) => {
    const icon = createCustomIcon(getMarkerColor(item.availability))

    const marker = L.marker([item.latitude, item.longitude], { icon })

    marker.bindPopup(`
      <div class="facility-popup">
        <div class="popup-title">${escapeHtml(item.name) || 'Unnamed facility'}</div>
        <div class="popup-line">${escapeHtml(item.suburb)} ${escapeHtml(item.postcode)}</div>
        <div class="popup-line">${escapeHtml(item.careType)}</div>
        <div class="popup-line">Beds: ${item.totalBeds ?? 'N/A'}</div>
        <div class="popup-line">
          ${item.availability ? `Availability: ${escapeHtml(item.availability)}` : 'Availability: Unknown'}
        </div>
        <div class="popup-actions">
          <a class="popup-detail-btn" href="/facility/${item.id}">
            SHOW DETAIL
          </a>
        </div>
      </div>
`   )

    marker.addTo(markersLayer)
  })

  invalidateMapSize()
}

function buildLeafletMarkers() {
  visibleSet.forEach(m => markersLayer.removeLayer(m))
  visibleSet.clear()

  const withCoords = allMarkersCache.value.filter(
    item => item.latitude != null && item.longitude != null
  )
  const offsetted = offsetDuplicateCoordinates(withCoords)

  preCreatedMarkers = offsetted.map(item => {
    const icon = createCustomIcon(getMarkerColor(item.availability))
    const leafletMarker = L.marker([item.latitude, item.longitude], { icon })
    leafletMarker.bindPopup(`
      <div class="facility-popup">
        <div class="popup-title">${escapeHtml(item.name) || 'Unnamed facility'}</div>
        <div class="popup-line">${escapeHtml(item.suburb)} ${escapeHtml(item.postcode)}</div>
        <div class="popup-line">${escapeHtml(item.careType)}</div>
        <div class="popup-line">Beds: ${item.totalBeds ?? 'N/A'}</div>
        <div class="popup-line">
          ${item.availability ? `Availability: ${escapeHtml(item.availability)}` : 'Availability: Unknown'}
        </div>
        <div class="popup-actions">
          <a class="popup-detail-btn" href="/facility/${item.id}">SHOW DETAIL</a>
        </div>
      </div>
    `)
    return { leafletMarker, lat: item.latitude, lng: item.longitude }
  })
}

function filterByViewport() {
  if (!map || !markersLayer) return

  if (preCreatedMarkers.length === 0 && allMarkersCache.value.length > 0) {
    buildLeafletMarkers()
  }

  const bounds = map.getBounds()

  preCreatedMarkers.forEach(({ leafletMarker, lat, lng }) => {
    const inView = bounds.contains([lat, lng])
    const shown = visibleSet.has(leafletMarker)
    if (inView && !shown) {
      markersLayer.addLayer(leafletMarker)
      visibleSet.add(leafletMarker)
    } else if (!inView && shown) {
      markersLayer.removeLayer(leafletMarker)
      visibleSet.delete(leafletMarker)
    }
  })

  markers.value = new Array(visibleSet.size)
  emit('update:count', visibleSet.size)
  renderUserMarker()
  invalidateMapSize()
}

async function fetchMarkers() {
  loading.value = true
  error.value = ''

  try {
    const params = buildParams()
    const isInitialLoad = !params.keyword && !params.postcode && !params.suburb && !params.region

    if (isInitialLoad) {
      const data = await getMapFacilities({})
      allMarkersCache.value = (data.results || []).map(mapFacilityMarker)
      hasSearched.value = false
      buildLeafletMarkers()
    } else {
      hasSearched.value = true

      // If cache is empty (e.g. user switched from list view), fetch all facilities in parallel
      const cacheEmpty = allMarkersCache.value.length === 0
      const [searchData, allData] = await Promise.all([
        getMapFacilities(params),
        cacheEmpty ? getMapFacilities({}) : Promise.resolve(null),
      ])

      if (cacheEmpty && allData) {
        allMarkersCache.value = (allData.results || []).map(mapFacilityMarker)
        buildLeafletMarkers()
      }

      const results = (searchData.results || []).map(mapFacilityMarker)
      const valid = results.filter(m => m.latitude != null && m.longitude != null)

      if (valid.length > 0) {
        if (params.keyword) {
          // facility name search: zoom to level 15 (~2.5km wide) centered on first result
          map.setView([valid[0].latitude, valid[0].longitude], 15, { animate: false })
        } else {
          // postcode / suburb / region search: fitBounds to all results
          const group = L.featureGroup(valid.map(m => L.marker([m.latitude, m.longitude])))
          map.fitBounds(group.getBounds().pad(0.2), { animate: false })
        }
      }
    }

    await nextTick()
    filterByViewport()
  } catch (err) {
    console.error('Failed to load map facilities:', err)
    error.value = 'Failed to load map facilities.'
    allMarkersCache.value = []
    markers.value = []
    emit('update:count', 0)
    clearMarkers()
  } finally {
    loading.value = false
    invalidateMapSize()
  }
}

function removeCurrentOverlay() {
  if (choropletheLayer) { map.removeLayer(choropletheLayer); choropletheLayer = null }
  if (environmentalLayer) { map.removeLayer(environmentalLayer); environmentalLayer = null }
  if (heatRiskLayer) { map.removeLayer(heatRiskLayer); heatRiskLayer = null }
}

function normalizeLgaName(value) {
  return String(value || '')
    .toUpperCase()
    .replace(/\s*\([^)]*\)\s*/g, ' ')
    .replace(/\b(RURAL CITY|REGIONAL CITY|CITY|SHIRE|BOROUGH|MUNICIPALITY|COUNCIL)\b/g, ' ')
    .replace(/\b(RC|C|S|B)\b/g, ' ')
    .replace(/[^A-Z0-9]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function getFeatureLgaName(feature) {
  return (
    feature.properties.lga_name ||
    feature.properties.lga_name_2021 ||
    feature.properties.LGA_NAME ||
    ''
  )
}

async function loadCrimeHeatmapData(year = selectedCrimeYear.value) {
  const cacheKey = year || 'latest'
  if (crimeCache.has(cacheKey)) {
    return crimeCache.get(cacheKey)
  }

  const data = await getHeatmapCrime(year ? { year } : {})
  if (data.available_years?.length) {
    crimeYears.value = data.available_years
  } else if (data.year != null && !crimeYears.value.includes(data.year)) {
    crimeYears.value = [data.year, ...crimeYears.value].sort((a, b) => b - a)
  }
  if (data.year != null && selectedCrimeYear.value !== data.year && year == null) {
    selectedCrimeYear.value = data.year
  }

  crimeCache.set(data.year ?? cacheKey, data)
  if (cacheKey === 'latest' && data.year != null) {
    crimeCache.set(cacheKey, data)
  }
  return data
}

function renderCrimeOverlay(geojson, apiData) {
  const rateMap = Object.fromEntries(
    apiData.results.map(r => [normalizeLgaName(r.lga_name), r.adjusted_rate])
  )
  const formatRate = rate => (
    rate == null
      ? 'No data'
      : Number(rate).toLocaleString(undefined, { maximumFractionDigits: 2 })
  )

  choropletheLayer = L.geoJSON(geojson, {
    style(feature) {
      const key = normalizeLgaName(getFeatureLgaName(feature))
      const rate = rateMap[key]
      const fill =
        rate == null ? '#e0e0e0'
        : rate > 15000 ? '#d64545'
        : rate > 7000 ? '#f4923a'
        : rate > 3000 ? '#f7e07a'
        : rate > 1000  ? '#74c476'
        : '#1a7a4a'
      return { fillColor: fill, fillOpacity: 0.55, color: '#888', weight: 0.5 }
    },
    onEachFeature(feature, layer) {
      const key = normalizeLgaName(getFeatureLgaName(feature))
      const rate = rateMap[key]
      layer.bindTooltip(
        `<b>${getFeatureLgaName(feature)}</b><br>Rate: ${formatRate(rate)}`,
        { sticky: true }
      )
    },
  })
  choropletheLayer.addTo(map)
  choropletheLayer.bringToBack()
}

async function toggleOverlay(name) {
  if (!map || overlayLoading.value) return

  if (activeOverlay.value === name) {
    activeOverlay.value = null
    removeCurrentOverlay()
    return
  }

  overlayLoading.value = true
  removeCurrentOverlay()
  activeOverlay.value = name

  try {
    if (name === 'demand') {
      const [geojson, apiData] = await Promise.all([
        lgaGeoJson ? Promise.resolve(lgaGeoJson) : getHeatmapLgaBoundaries().then(d => { lgaGeoJson = d; return d }),
        getHeatmapDemand(),
      ])
      lgaGeoJson = geojson

      if (activeOverlay.value !== name) return

      const ratioMap = Object.fromEntries(
        apiData.results.map(r => [normalizeLgaName(r.lga_name), r.ratio])
      )
      const sorted = apiData.results
        .map(r => r.ratio)
        .filter(v => v != null)
        .sort((a, b) => a - b)
      const pct = p => sorted[Math.floor(p * sorted.length)] ?? 0
      const [p20, p40, p60, p80] = [0.2, 0.4, 0.6, 0.8].map(pct)

      choropletheLayer = L.geoJSON(geojson, {
        style(feature) {
          const key = normalizeLgaName(getFeatureLgaName(feature))
          const ratio = ratioMap[key]
          const fill =
            ratio == null ? '#cccccc'
            : ratio > p80 ? '#1a7a4a'
            : ratio > p60 ? '#74c476'
            : ratio > p40 ? '#f7e07a'
            : ratio > p20 ? '#f4923a'
            : '#d64545'
          return { fillColor: fill, fillOpacity: 0.55, color: '#888', weight: 0.5 }
        },
      })
      choropletheLayer.addTo(map)
      choropletheLayer.bringToBack()

    } else if (name === 'crime') {
      const [geojson, apiData] = await Promise.all([
        lgaGeoJson ? Promise.resolve(lgaGeoJson) : getHeatmapLgaBoundaries().then(d => { lgaGeoJson = d; return d }),
        loadCrimeHeatmapData(),
      ])
      lgaGeoJson = geojson

      if (activeOverlay.value !== name) return

      renderCrimeOverlay(geojson, apiData)

    } else if (name === 'heatrisk') {
      const apiData = heatRiskCache ?? (heatRiskCache = await getHeatmapHeatRisk())
      if (activeOverlay.value !== name) return

      const scores = apiData.results
        .map(r => r.risk_score)
        .filter(s => s != null)
        .sort((a, b) => a - b)
      const pct = p => scores[Math.floor(p * scores.length)] ?? 0
      const [p20, p40, p60, p80] = [0.2, 0.4, 0.6, 0.8].map(pct)

      const getHrColor = score => {
        if (score == null) return '#adb5bd'
        if (score > p80) return '#9d0208'
        if (score > p60) return '#f3722c'
        if (score > p40) return '#f9c74f'
        if (score > p20) return '#52b788'
        return '#1e7145'
      }

      const markers = apiData.results.map(r =>
        L.circleMarker([r.lat, r.lon], {
          pane: 'heatRiskPane',
          radius: 8,
          fillColor: getHrColor(r.risk_score),
          fillOpacity: 0.9,
          color: 'rgba(0,0,0,0.25)',
          weight: 1,
        }).bindTooltip(
          `Heat Risk: ${r.heat_risk}<br>Score: ${r.risk_score?.toFixed(3) ?? 'N/A'}`,
          { sticky: true }
        )
      )
      heatRiskLayer = L.layerGroup(markers).addTo(map)

    } else if (name === 'environmental') {
      const [geojson, apiData] = await Promise.all([
        lgaGeoJson ? Promise.resolve(lgaGeoJson) : getHeatmapLgaBoundaries().then(d => { lgaGeoJson = d; return d }),
        bushfireCache ? Promise.resolve(bushfireCache) : getHeatmapBushfire().then(d => { bushfireCache = d; return d }),
      ])
      lgaGeoJson = geojson

      if (activeOverlay.value !== name) return

      const countMap = Object.fromEntries(
        apiData.results.map(r => [normalizeLgaName(r.lga_name), r.bushfire_count])
      )
      const sorted = apiData.results.map(r => r.bushfire_count).sort((a, b) => a - b)
      const pct = p => sorted[Math.floor(p * sorted.length)] ?? 0
      const [p10, p25, p40, p55, p70, p85] = [0.10, 0.25, 0.40, 0.55, 0.70, 0.85].map(pct)

      choropletheLayer = L.geoJSON(geojson, {
        style(feature) {
          const key = normalizeLgaName(getFeatureLgaName(feature))
          const count = countMap[key]
          const fill =
            count == null ? '#e9ecef'
            : count > p85 ? '#9d0208'
            : count > p70 ? '#f94144'
            : count > p55 ? '#f3722c'
            : count > p40 ? '#f9c74f'
            : count > p25 ? '#a7c957'
            : count > p10 ? '#52b788'
            : '#1e7145'
          return { fillColor: fill, fillOpacity: 0.65, color: '#888', weight: 0.5 }
        },
        onEachFeature(feature, layer) {
          const key = normalizeLgaName(getFeatureLgaName(feature))
          const count = countMap[key]
          layer.bindTooltip(
            `<b>${getFeatureLgaName(feature)}</b><br>Bushfires: ${count ?? 'No data'}`,
            { sticky: true }
          )
        },
      })
      choropletheLayer.addTo(map)
      choropletheLayer.bringToBack()
    }
  } finally {
    overlayLoading.value = false
  }
}

onMounted(async () => {
  await nextTick()
  initMap()
  invalidateMapSize()
  await fetchMarkers()
})

watch(
  () => [props.searchQuery, props.searchType, props.selectedCareTypes, props.distance],
  async () => {
    await fetchMarkers()
  },
  { deep: true }
)

watch(
  () => [props.focusLat, props.focusLng],
  () => {
    if (map && hasFocusCoordinates()) {
      map.setView([props.focusLat, props.focusLng], 15)
    }
  }
)

watch(
  () => [props.userLat, props.userLng],
  () => {
    renderMarkers()
  }
)

watch(selectedCrimeYear, async (year, previousYear) => {
  if (
    activeOverlay.value !== 'crime' ||
    overlayLoading.value ||
    year == null ||
    year === previousYear
  ) {
    return
  }

  overlayLoading.value = true
  removeCurrentOverlay()

  try {
    const [geojson, apiData] = await Promise.all([
      lgaGeoJson ? Promise.resolve(lgaGeoJson) : fetch('/data/lga.geojson').then(r => r.json()),
      loadCrimeHeatmapData(year),
    ])
    lgaGeoJson = geojson

    if (activeOverlay.value === 'crime' && selectedCrimeYear.value === year) {
      renderCrimeOverlay(geojson, apiData)
    }
  } finally {
    overlayLoading.value = false
  }
})

watch(
  () => props.isActive,
  (isActive) => {
    if (isActive) {
      invalidateMapSize()
      renderMarkers()
    }
  }
)

onBeforeUnmount(() => {
  if (map) {
    removeCurrentOverlay()
    map.remove()
    map = null
  }
  markersLayer = null
  userMarker = null
})
</script>

<style scoped>
.map-section {
  width: 100%;
}

.map-wrapper {
  position: relative;
  width: 100%;
}

.map-no-results {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  padding: 12px 20px;
  font-size: 14px;
  color: #5e706a;
  font-weight: 500;
  white-space: nowrap;
  pointer-events: none;
}

.map-container {
  width: 100%;
  height: 430px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #ddd8cf;
  background: #f5f5f5;
}

.map-legends-container {
  position: absolute;
  left: 16px;
  bottom: 16px;
  z-index: 800;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}

.crime-year-control {
  position: absolute;
  top: 12px;
  left: 58px;
  z-index: 1100;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 9px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  box-shadow: 0 8px 22px rgba(31, 45, 42, 0.12);
}

.crime-year-label {
  font-size: 11px;
  font-weight: 700;
  color: #5e706a;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.crime-year-select {
  min-width: 78px;
  height: 28px;
  border: 1px solid #cfd8d4;
  border-radius: 5px;
  background: #fff;
  color: #253631;
  font: 600 12px var(--font-sans);
  cursor: pointer;
  pointer-events: auto;
}

.crime-year-select:disabled {
  color: #9aa8a4;
  cursor: not-allowed;
}

.map-legend {
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #ddd8cf;
  border-radius: 8px;
  padding: 10px 12px;
  box-shadow: 0 8px 22px rgba(31, 45, 42, 0.12);
  color: #253631;
  font-size: 12px;
  line-height: 1.35;
}

.legend-title {
  margin-bottom: 7px;
  font-weight: 700;
  color: #22332e;
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-title-spread {
  justify-content: space-between;
  gap: 16px;
}

.legend-info {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: 1px solid #cfd8d4;
  border-radius: 50%;
  color: #5e706a;
  background: #fff;
  font-size: 11px;
  font-weight: 700;
  line-height: 1;
  cursor: help;
  flex: 0 0 auto;
}

.legend-info-tooltip {
  position: absolute;
  left: calc(100% + 8px);
  top: 50%;
  width: max-content;
  max-width: 190px;
  padding: 6px 8px;
  border: 1px solid #ddd8cf;
  border-radius: 6px;
  background: rgba(37, 54, 49, 0.96);
  color: #fff;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.3;
  opacity: 0;
  pointer-events: none;
  transform: translateY(-50%) translateX(-2px);
  transition: opacity 0.15s, transform 0.15s;
  z-index: 2000;
}

.legend-info:hover .legend-info-tooltip,
.legend-info:focus .legend-info-tooltip {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

.legend-sub {
  margin-top: 6px;
  font-size: 10px;
  color: #77857f;
  font-style: italic;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 7px;
  white-space: nowrap;
}

.legend-item + .legend-item {
  margin-top: 5px;
}

.legend-dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px rgba(31, 45, 42, 0.16);
  flex: 0 0 auto;
}

.legend-likely {
  background: #4f7a62;
}

.legend-potential {
  background: #f5c518;
}

.legend-constrained {
  background: #d9822b;
}

.legend-highly-constrained {
  background: #d64545;
}

.legend-unavailable {
  background: #9e9e9e;
}

.legend-gradient-bar {
  width: 140px;
  height: 10px;
  border-radius: 4px;
  background: linear-gradient(to right, #fbbf24, #f97316, #dc2626, #7f1d1d);
  margin: 6px 0 4px;
}

.legend-gradient-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #5e706a;
}

.overlay-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  background: #fff;
  border: 1px solid #ddd8cf;
  border-radius: 10px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.overlay-bar-left {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
}

.overlay-hint {
  font-size: 12px;
  color: #9aa8a4;
  white-space: nowrap;
}

.overlay-label {
  font-size: 11px;
  font-weight: 700;
  color: #5e706a;
  margin-right: 4px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.overlay-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 5px;
  border: 1px solid #ddd8cf;
  background: transparent;
  color: #2D6A5F;
  cursor: pointer;
  transition: all 0.15s;
  font-family: var(--font-sans);
  white-space: nowrap;
}

.overlay-btn svg {
  flex: 0 0 auto;
}

.overlay-btn:disabled {
  color: #b0bab7;
  cursor: not-allowed;
  background: transparent;
}

.overlay-btn.active {
  background: #557067;
  color: white;
  border-color: #557067;
}

.overlay-btn:not(:disabled):not(.active):hover {
  background: #f0edea;
}

.map-state {
  height: 430px;
  border-radius: 14px;
  border: 1px solid #ddd8cf;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  color: #6b736f;
  font-size: 15px;
}

.error {
  color: #d64545;
}

@media (max-width: 640px) {
  .map-legends-container {
    left: 10px;
    bottom: 10px;
  }

  .overlay-bar {
    align-items: stretch;
    padding: 10px;
  }

  .overlay-bar-left {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    width: 100%;
  }

  .overlay-label {
    grid-column: 1 / -1;
    margin-right: 0;
    letter-spacing: 0;
  }

  .overlay-btn {
    justify-content: center;
    width: 100%;
    min-height: 36px;
    padding: 7px 8px;
  }

  .overlay-hint {
    display: none;
  }
}
</style>

<style>
.custom-marker-wrapper {
  background: transparent;
  border: none;
}

.custom-marker {
  width: 26px;
  height: 26px;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  position: relative;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
}

.custom-marker-inner {
  width: 10px;
  height: 10px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 6px;
  left: 6px;
}
</style>
