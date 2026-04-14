const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

async function request(path, params = {}) {
  const url = new URL(`${API_BASE_URL}${path}`)

  Object.entries(params).forEach(([key, value]) => {
<<<<<<< Updated upstream
    if (value === undefined || value === null || value === '') return
    if (Array.isArray(value)) {
      value.forEach(v => url.searchParams.append(key, v))
    } else {
      url.searchParams.append(key, value)
=======
    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(v => url.searchParams.append(key, v))
      } else {
        url.searchParams.append(key, value)
      }
>>>>>>> Stashed changes
    }
  })

  const res = await fetch(url)

  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`)
  }

  return res.json()
}

export function searchFacilities(params = {}) {
  return request('/api/v1/facilities/search', params)
}

export function getRecommendedFacilities() {
  return request('/api/v1/facilities/recommended')
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