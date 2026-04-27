<template>
  <div class="map-section">
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
      <div class="map-legend" aria-label="Availability legend">
        <div class="legend-title">Availability</div>
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
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import L from 'leaflet'
import { getMapFacilities } from '../services/facilitiesApi'
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
  }
})

const mapEl = ref(null)
const loading = ref(false)
const error = ref('')
const hasSearched = ref(false)
const markers = ref([])

let map = null
let markersLayer = null
let userMarker = null

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
    if (/^\d+$/.test(q)) {
      params.postcode = q
    } else {
      params.suburb = q
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
  console.log('offset result:', result.length, result.map(f => `${f.latitude},${f.longitude}`))
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

    const params = buildParams()
    if (hasFocusCoordinates()) {
      focusMapOnSelectedFacility()
    } else if (params.postcode || params.suburb) {
      // 保持当前地图位置不变，不重置到 Melbourne
    } else {
      map.setView([-37.8136, 144.9631], 12)
    }

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

  const leafletMarkers = validMarkers.map((item) =>
    L.marker([item.latitude, item.longitude])
  )
  const group = L.featureGroup(leafletMarkers)
  map.fitBounds(group.getBounds().pad(0.2))
  focusMapOnSelectedFacility()

  invalidateMapSize()
}

async function fetchMarkers() {
  loading.value = true
  error.value = ''

  try {
    const params = buildParams()

    console.log('map params:', params)

    let rawResults = []

    if (params.suburb || params.postcode || params.region) {
      const data = await getMapFacilities(params)
      console.log('map response:', data)
      rawResults = data.results || []
    }

    markers.value = rawResults.map(mapFacilityMarker)
    hasSearched.value = params.suburb || params.postcode || params.region ? true : false

    emit('update:count', markers.value.length)

    await nextTick()
    renderMarkers()
  } catch (err) {
    console.error('Failed to load map facilities:', err)
    error.value = 'Failed to load map facilities.'
    markers.value = []
    emit('update:count', 0)
    clearMarkers()
  } finally {
    loading.value = false
    invalidateMapSize()
  }
}

onMounted(async () => {
  await nextTick()
  initMap()
  invalidateMapSize()
  await fetchMarkers()
})

watch(
  () => [props.searchQuery, props.selectedCareTypes, props.distance, props.focusLat, props.focusLng],
  async () => {
    await fetchMarkers()
  },
  { deep: true }
)

watch(
  () => [props.userLat, props.userLng],
  () => {
    renderMarkers()
  }
)

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

.map-legend {
  position: absolute;
  left: 16px;
  bottom: 16px;
  z-index: 800;
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
  .map-legend {
    left: 10px;
    right: 10px;
    bottom: 10px;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 5px 10px;
  }

  .legend-title {
    grid-column: 1 / -1;
    margin-bottom: 2px;
  }

  .legend-item + .legend-item {
    margin-top: 0;
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
