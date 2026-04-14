<template>
  <div class="map-section">
    <div v-if="loading" class="map-state">Loading map...</div>
    <div v-else-if="error" class="map-state error">{{ error }}</div>
    <div v-show="!loading && !error" ref="mapEl" class="map-container"></div>
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
  isActive: {
    type: Boolean,
    default: true
  }
})

const mapEl = ref(null)
const loading = ref(false)
const error = ref('')
const markers = ref([])

let map = null
let markersLayer = null
let userMarker = null

const defaultCenter = [-37.8136, 144.9631]
const defaultZoom = 10
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
  } else {
    params.region = 'Melbourne'
    params.max_distance_km = props.distance ?? 10
  }

  if (props.selectedCareTypes.length > 0) {
    const mappedType = careTypeMap[props.selectedCareTypes[0]]
    if (mappedType) {
      params.care_type = mappedType
    }
  }

  if (props.distance != null) {
    params.max_distance_km = props.distance
  }

  return params
}

function getMarkerColor(availability) {
  if (availability === 'High') return '#4f7a62'
  if (availability === 'Medium') return '#d9822b'
  if (availability === 'Low') return '#d64545'
  return '#7a6fd6'
}

function createCustomIcon(color) {
  return L.divIcon({
    className: 'custom-marker-wrapper',
    html: `
      <div class="custom-marker" style="background:${color}">
        <div class="custom-marker-inner"></div>
      </div>
    `,
    iconSize: [26, 38],
    iconAnchor: [13, 38],
    popupAnchor: [0, -34]
  })
}

function initMap() {
  if (map || !mapEl.value) return

  let center = defaultCenter
  let zoom = defaultZoom

  if (props.userLat != null && props.userLng != null) {
    center = [props.userLat, props.userLng]
    zoom = 11
  }

  map = L.map(mapEl.value, {
    zoomControl: true
  }).setView(center, zoom)

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

function renderMarkers() {
  if (!map || !markersLayer) return

  markersLayer.clearLayers()
  renderUserMarker()

  const validMarkers = markers.value.filter(
    (item) => item.latitude != null && item.longitude != null
  )

  if (validMarkers.length === 0) {
    if (props.userLat != null && props.userLng != null) {
      map.setView([props.userLat, props.userLng], 11)
    } else {
      map.setView(defaultCenter, defaultZoom)
    }
    invalidateMapSize()
    return
  }

  validMarkers.forEach((item) => {
    const icon = createCustomIcon(getMarkerColor(item.availability))

    const marker = L.marker([item.latitude, item.longitude], { icon })

    marker.bindPopup(`
      <div class="facility-popup">
        <div class="popup-title">${item.name || 'Unnamed facility'}</div>
        <div class="popup-line">${(item.suburb || '')} ${(item.postcode || '')}</div>
        <div class="popup-line">${item.careType || ''}</div>
        <div class="popup-line">Beds: ${item.totalBeds ?? 'N/A'}</div>
        <div class="popup-line">
          ${item.availability ? `Availability: ${item.availability}` : 'Availability: Unknown'}
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

  const boundsPoints = validMarkers.map((item) => [item.latitude, item.longitude])

  if (props.userLat != null && props.userLng != null) {
    boundsPoints.push([props.userLat, props.userLng])
  }

  if (boundsPoints.length === 1) {
    map.setView(boundsPoints[0], 12)
  } else {
    const bounds = L.latLngBounds(boundsPoints)
    map.fitBounds(bounds, { padding: [30, 30] })
  }

  invalidateMapSize()
}

async function fetchMarkers() {
  loading.value = true
  error.value = ''

  try {
    const params = buildParams()

    console.log('map params:', params)

    let rawResults = []

    if (params.suburb || params.postcode || params.care_type) {
      const data = await getMapFacilities(params)
      console.log('map response:', data)
      rawResults = data.results || []
    }

    markers.value = rawResults.map(mapFacilityMarker)

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
  () => [props.searchQuery, props.selectedCareTypes, props.distance],
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

.map-container {
  width: 100%;
  height: 430px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #ddd8cf;
  background: #f5f5f5;
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