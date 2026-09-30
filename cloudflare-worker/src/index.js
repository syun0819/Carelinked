import { facilities } from './facilities.js'

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
}

const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {
    ...CORS_HEADERS,
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'public, max-age=300'
  }
})

const error = (detail, status = 404) => json({ detail }, status)

function getAllParams(url, key) {
  const repeated = url.searchParams.getAll(key)
  return repeated.flatMap(value => String(value).split(',')).map(v => v.trim()).filter(Boolean)
}

function includesText(value, query) {
  return String(value || '').toLowerCase().includes(String(query || '').toLowerCase())
}

function toNumber(value, fallback = null) {
  if (value == null || value === '') return fallback
  const number = Number(value)
  return Number.isFinite(number) ? number : fallback
}

function haversineDistance(lat1, lon1, lat2, lon2) {
  const toRad = degrees => degrees * Math.PI / 180
  const earthKm = 6371
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  return earthKm * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

function withDistance(items, lat, lng) {
  if (lat == null || lng == null) return items
  return items.map(item => ({
    ...item,
    distance_km: item.latitude != null && item.longitude != null
      ? Math.round(haversineDistance(lat, lng, item.latitude, item.longitude) * 10) / 10
      : null
  }))
}

function searchFacilities(url) {
  const keyword = url.searchParams.get('keyword')
  const suburb = url.searchParams.get('suburb')
  const postcode = url.searchParams.get('postcode')
  const region = url.searchParams.get('region')
  const careTypes = getAllParams(url, 'care_type')
  const remoteness = url.searchParams.get('abs_remoteness')
  const minBeds = toNumber(url.searchParams.get('min_beds'))
  const maxBeds = toNumber(url.searchParams.get('max_beds'))
  const userLat = toNumber(url.searchParams.get('user_lat'))
  const userLng = toNumber(url.searchParams.get('user_lng'))
  const sortBy = url.searchParams.get('sort_by') || 'name'
  const limit = Math.min(toNumber(url.searchParams.get('limit'), 20), 100)
  const offset = toNumber(url.searchParams.get('offset'), 0)

  let results = [...facilities]

  if (keyword) {
    results = results.filter(item =>
      includesText(item.service_name, keyword) ||
      includesText(item.provider_name, keyword) ||
      includesText(item.physical_suburb, keyword) ||
      includesText(item.aged_care_planning_region, keyword)
    )
  }
  if (suburb) results = results.filter(item => includesText(item.physical_suburb, suburb))
  if (postcode) results = results.filter(item => item.physical_post_code === postcode)
  if (region) results = results.filter(item => includesText(item.aged_care_planning_region, region))
  if (careTypes.length) results = results.filter(item => careTypes.includes(item.care_type))
  if (remoteness) results = results.filter(item => item.abs_remoteness === remoteness)
  if (minBeds != null) results = results.filter(item => (item.residential_places || 0) >= minBeds)
  if (maxBeds != null) results = results.filter(item => (item.residential_places || 0) <= maxBeds)

  results = withDistance(results, userLat, userLng)

  if (sortBy === 'beds_desc') {
    results.sort((a, b) => (b.residential_places || 0) - (a.residential_places || 0))
  } else if (sortBy === 'beds_asc') {
    results.sort((a, b) => (a.residential_places || 0) - (b.residential_places || 0))
  } else if (sortBy === 'distance') {
    results.sort((a, b) => (a.distance_km ?? Number.MAX_SAFE_INTEGER) - (b.distance_km ?? Number.MAX_SAFE_INTEGER))
  } else {
    results.sort((a, b) => a.service_name.localeCompare(b.service_name))
  }

  const total = results.length
  const page = results.slice(offset, offset + limit)
  return {
    total,
    results: page,
    message: total === 0 ? 'No facilities found. Try adjusting your search criteria.' : null
  }
}

function mapFacilities(url) {
  const response = searchFacilities(new URL(url))
  return {
    total: response.total,
    results: response.results.map(item => ({
      id: item.id,
      service_name: item.service_name,
      latitude: item.latitude,
      longitude: item.longitude,
      care_type: item.care_type,
      residential_places: item.residential_places,
      availability_group: item.availability_group,
      data_source: item.data_source,
      provider_name: item.provider_name,
      physical_suburb: item.physical_suburb,
      physical_post_code: item.physical_post_code
    })),
    message: response.message
  }
}

function recommendedFacilities(url) {
  const limit = Math.min(toNumber(url.searchParams.get('limit'), 6), 20)
  const userLat = toNumber(url.searchParams.get('user_lat'))
  const userLng = toNumber(url.searchParams.get('user_lng'))
  const results = withDistance([...facilities], userLat, userLng)
    .sort((a, b) => {
      if (userLat != null && userLng != null) {
        return (a.distance_km ?? Number.MAX_SAFE_INTEGER) - (b.distance_km ?? Number.MAX_SAFE_INTEGER)
      }
      return (b.residential_places || 0) - (a.residential_places || 0)
    })
    .slice(0, limit)
  return { total: results.length, results }
}

function getSimilar(id, url) {
  const limit = Math.min(toNumber(url.searchParams.get('limit'), 4), 20)
  const target = facilities.find(item => item.id === id)
  if (!target) return null
  const results = facilities
    .filter(item => item.id !== id)
    .map(item => ({
      ...item,
      distance_km: target.latitude && target.longitude && item.latitude && item.longitude
        ? Math.round(haversineDistance(target.latitude, target.longitude, item.latitude, item.longitude) * 10) / 10
        : null
    }))
    .sort((a, b) => {
      if (a.care_type === target.care_type && b.care_type !== target.care_type) return -1
      if (a.care_type !== target.care_type && b.care_type === target.care_type) return 1
      return (a.distance_km ?? Number.MAX_SAFE_INTEGER) - (b.distance_km ?? Number.MAX_SAFE_INTEGER)
    })
    .slice(0, limit)
  return { total: results.length, results }
}

function autocomplete(url) {
  const q = String(url.searchParams.get('q') || '').trim()
  if (q.length < 2) return { facilities: [], suburbs: [], postcodes: [] }
  const matches = facilities.filter(item =>
    includesText(item.service_name, q) ||
    includesText(item.physical_suburb, q) ||
    includesText(item.physical_post_code, q)
  )
  const suburbs = new Map()
  const postcodes = new Map()
  for (const item of matches) {
    suburbs.set(`${item.physical_suburb}-${item.physical_post_code}`, {
      name: item.physical_suburb,
      postcode: item.physical_post_code,
      type: 'suburb'
    })
    postcodes.set(item.physical_post_code, {
      postcode: item.physical_post_code,
      suburb: item.physical_suburb,
      type: 'postcode'
    })
  }
  return {
    facilities: matches.slice(0, 8).map(item => ({
      id: item.id,
      name: item.service_name,
      type: 'facility',
      suburb: item.physical_suburb,
      state: item.physical_state,
      postcode: item.physical_post_code
    })),
    suburbs: [...suburbs.values()].slice(0, 6),
    postcodes: [...postcodes.values()].slice(0, 6)
  }
}

async function estimateWaitTime(request) {
  const body = await request.json().catch(() => ({}))
  const urgency = String(body.urgency || body.priority || '').toLowerCase()
  const hasHighNeed = Object.values(body).some(value => String(value).toLowerCase().includes('high'))
  let days = 41
  if (urgency.includes('urgent') || hasHighNeed) days = 24
  if (String(body.location || '').toLowerCase().includes('regional')) days += 14
  const outcome = days <= 30 ? 'less_than_median' : days <= 60 ? 'around_median' : 'more_than_median'
  const category = days <= 30 ? 'Shorter than average' : days <= 60 ? 'Around average' : 'Longer than average'
  return {
    outcome,
    estimated_days: days,
    estimate_days: days,
    wait_days: days,
    category,
    outcome_label: category,
    message: `Estimated wait time: ${days} days`,
    explanation: 'Demo estimate based on AIHW median wait-time context and portfolio-site inputs.'
  }
}

function heatmapDemand() {
  return json({
    results: [
      { lga_name: 'Melbourne', supply: 420, demand: 510, ratio: 0.82 },
      { lga_name: 'Sydney', supply: 500, demand: 650, ratio: 0.77 },
      { lga_name: 'Adelaide', supply: 260, demand: 300, ratio: 0.87 },
      { lga_name: 'Perth', supply: 340, demand: 360, ratio: 0.94 }
    ]
  })
}

function heatmapBushfire() {
  return json({
    results: [
      { lga_name: 'Melbourne', bushfire_count: 4 },
      { lga_name: 'Sydney', bushfire_count: 8 },
      { lga_name: 'Adelaide', bushfire_count: 6 },
      { lga_name: 'Parkes', bushfire_count: 18 }
    ]
  })
}

function heatmapCrime(url) {
  const year = toNumber(url.searchParams.get('year'), 2024)
  return json({
    year,
    available_years: [2024, 2023, 2022],
    results: [
      { lga_name: 'Melbourne', adjusted_rate: 7200 },
      { lga_name: 'Sydney', adjusted_rate: 6900 },
      { lga_name: 'Adelaide', adjusted_rate: 4100 },
      { lga_name: 'Perth', adjusted_rate: 3900 }
    ]
  })
}

function heatmapHeatRisk() {
  return json({
    results: facilities.map(item => ({
      id: item.id,
      lat: item.latitude,
      lon: item.longitude,
      risk_score: Math.min(1, Math.max(0.1, (item.residential_places || 50) / 160)),
      heat_risk: (item.residential_places || 0) > 100 ? 'High' : 'Moderate'
    }))
  })
}

function lgaBoundaries() {
  const boxes = [
    ['Melbourne', [144.86, -37.88, 145.05, -37.74]],
    ['Sydney', [151.12, -33.93, 151.29, -33.78]],
    ['Adelaide', [138.50, -35.02, 138.69, -34.84]],
    ['Perth', [115.75, -32.03, 115.96, -31.87]],
    ['Parkes', [148.10, -33.20, 148.25, -33.08]]
  ]
  return json({
    type: 'FeatureCollection',
    features: boxes.map(([name, [west, south, east, north]]) => ({
      type: 'Feature',
      properties: {
        lga_name: name,
        lga_name_2021: name,
        LGA_NAME: name
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [west, south],
          [east, south],
          [east, north],
          [west, north],
          [west, south]
        ]]
      }
    }))
  })
}

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS_HEADERS })

    const url = new URL(request.url)
    const path = url.pathname.replace(/\/$/, '')

    if (path === '/health') return json({ ok: true, service: 'carelinked-worker' })
    if (path === '/api/v1/facilities/recommended') return json(recommendedFacilities(url))
    if (path === '/api/v1/facilities/search') return json(searchFacilities(url))
    if (path === '/api/v1/facilities/map') return json(mapFacilities(url))
    if (path === '/api/v1/search/autocomplete') return json(autocomplete(url))
    if (path === '/api/v1/waittime/estimate' && request.method === 'POST') return json(await estimateWaitTime(request))
    if (path === '/api/v1/heatmap/demand') return heatmapDemand()
    if (path === '/api/v1/heatmap/bushfire') return heatmapBushfire()
    if (path === '/api/v1/heatmap/crime') return heatmapCrime(url)
    if (path === '/api/v1/heatmap/heat-risk') return heatmapHeatRisk()
    if (path === '/api/v1/heatmap/lga-boundaries') return lgaBoundaries()

    const similarMatch = path.match(/^\/api\/v1\/facilities\/([^/]+)\/similar$/)
    if (similarMatch) {
      const response = getSimilar(similarMatch[1], url)
      return response ? json(response) : error('Facility not found.', 404)
    }

    const detailMatch = path.match(/^\/api\/v1\/facilities\/([^/]+)$/)
    if (detailMatch) {
      const facility = facilities.find(item => item.id === detailMatch[1])
      return facility ? json(facility) : error('Facility not found.', 404)
    }

    return error('Not found.', 404)
  }
}
