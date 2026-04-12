<template>
  <div class="map-section">
    <div v-if="loading" class="map-state">Loading map...</div>
    <div v-else-if="error" class="map-state error">{{ error }}</div>
    <div v-else-if="markers.length === 0" class="map-state">
      No facilities found for this area.
    </div>
    <div v-show="markers.length > 0" ref="mapEl" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
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
  }
})

const mapEl = ref(null)
const loading = ref(false)
const error = ref('')
const markers = ref([])

let map = null
let markersLayer = null

const careTypeMap = {
  'Residential Aged Care': 'Residential',
  'Residential Care': 'Residential',
  'Home Care Package (HCP)': 'Home Care',
  'CHSP - Community Support': 'CHSP',
  'Respite (Short Stay)': 'Respite Care',
  'Respite Care': 'Respite Care',
  'Dementia / Memory Care': 'Memory Care',
  'Memory Care': 'Memory Care'
}

function buildParams() {
  const params = {}
  const q = props.searchQuery.trim()

  if (!q) {
    params.suburb = 'WALLINGTON'
  } else if (/^\d+$/.test(q)) {
    params.postcode = q
  } else {
    params.suburb = q
  }

  const careTypeMap = {
    'Residential Aged Care': 'Residential',
    'Residential Care': 'Residential',
    'Home Care Package (HCP)': 'Home Care',
    'CHSP - Community Support': '',
    'Respite (Short Stay)': '',
    'Respite Care': '',
    'Dementia / Memory Care': '',
    'Memory Care': ''
  }

  if (props.selectedCareTypes.length > 0) {
    const mapped = careTypeMap[props.selectedCareTypes[0]]
    if (mapped) {
      params.care_type = mapped
    }
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

  map = L.map(mapEl.value, {
    zoomControl: true
  }).setView([-37.8136, 144.9631], 8)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
}

function renderMarkers() {
  if (!map || !markersLayer) return

  markersLayer.clearLayers()

  const validMarkers = markers.value.filter(
    item => item.latitude !== null && item.longitude !== null
  )

  if (validMarkers.length === 0) return

  validMarkers.forEach(item => {
    const icon = createCustomIcon(getMarkerColor(item.availability))

    const marker = L.marker([item.latitude, item.longitude], { icon })

    marker.bindPopup(`
      <div style="min-width: 180px;">
        <strong>${item.name}</strong><br />
        ${item.suburb} ${item.postcode}<br />
        ${item.careType}<br />
        Beds: ${item.totalBeds}<br />
        ${item.availability ? `Availability: ${item.availability}` : ''}
      </div>
    `)

    marker.addTo(markersLayer)
  })

  const bounds = L.latLngBounds(
    validMarkers.map(item => [item.latitude, item.longitude])
  )

  map.fitBounds(bounds, { padding: [30, 30] })
}

async function fetchMarkers() {
  loading.value = true
  error.value = ''

  try {
    const params = buildParams()

    if (!params) {
      markers.value = []
      error.value = 'Enter a suburb or postcode to view facilities on the map.'
      if (markersLayer) markersLayer.clearLayers()
      return
    }

    console.log('map params:', params)

    const data = await getMapFacilities(params)
    console.log('map response:', data)

    markers.value = (data.results || []).map(mapFacilityMarker)

    if (markers.value.length === 0) {
      error.value = 'No facilities found for this area.'
      if (markersLayer) markersLayer.clearLayers()
      return
    }

    renderMarkers()
  } catch (err) {
    console.error('Failed to load map facilities:', err)
    error.value = 'Failed to load map facilities.'
    markers.value = []
    if (markersLayer) markersLayer.clearLayers()
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initMap()
  fetchMarkers()
})

watch(
  () => [props.searchQuery, props.selectedCareTypes, props.distance],
  () => {
    fetchMarkers()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
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