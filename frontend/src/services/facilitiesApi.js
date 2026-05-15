
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

async function request(path, params = {}, options = {}) {
  const url = new URL(`${API_BASE_URL}${path}`)
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return
    if (Array.isArray(value)) {
      value.forEach(v => url.searchParams.append(key, v))
    } else {
      url.searchParams.append(key, value)
    }
  })
  const res = await fetch(url, {
    signal: options.signal,
    method: options.method || 'GET',
    headers: options.body ? { 'Content-Type': 'application/json' } : undefined,
    body: options.body ? JSON.stringify(options.body) : undefined
  })
  if (!res.ok) {
    let detail = ''
    try {
      const errorBody = await res.json()
      detail = errorBody.detail ? `: ${JSON.stringify(errorBody.detail)}` : ''
    } catch {
      detail = ''
    }
    throw new Error(`API request failed: ${res.status}${detail}`)
  }
  return res.json()
}

export function searchFacilities(params = {}) {
  return request('/api/v1/facilities/search', params)
}

export function getSearchAutocomplete(q, options = {}) {
  return request('/api/v1/search/autocomplete', { q }, options)
}

export function getAutocomplete(q) {
  return request('/api/v1/search/autocomplete', { q })
}

export async function getRecommendedFacilities(params = {}) {
  return request('/api/v1/facilities/recommended', params)
}

export function getMapFacilities(params = {}) {
  return request('/api/v1/facilities/map', params)
}

export function getFacilityDetail(facilityId) {
  return request(`/api/v1/facilities/${facilityId}`)
}

export function getSimilarFacilities(facilityId, limit = 4) {
  return request(`/api/v1/facilities/${facilityId}/similar`, { limit })
}

export function estimateWaitTime(body) {
  return request('/api/v1/waittime/estimate', {}, {
    method: 'POST',
    body
  })
}

export function getHeatmapDemand() {
  return request('/api/v1/heatmap/demand')
}

export function getHeatmapBushfire() {
  return request('/api/v1/heatmap/bushfire')
}

export function getHeatmapCrime(params = {}) {
  return request('/api/v1/heatmap/crime', params)
}
