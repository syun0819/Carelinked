const DEFAULT_IMAGE =
  'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1200&q=80'

export function mapFacilityCard(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    image: DEFAULT_IMAGE,
    address: item.physical_address || '',
    suburb: item.physical_suburb || '',
    postcode: item.physical_post_code || '',
    careType: item.care_type || '',
    provider: item.provider_name || '',
    acpr: item.aged_care_planning_region || '',
    remoteness: item.abs_remoteness || '',
    totalBeds: item.residential_places ?? 0,

    state: '',
    organisationType: '',
    funding: '',
    providerType: '',
    bedAvailability: 'Unknown',
    estimatedWaitTime: '',
    waitWeeks: null,
    distance: null
  }
}

export function mapFacilityDetail(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    image: DEFAULT_IMAGE,
    address: item.physical_address || '',
    suburb: item.physical_suburb || '',
    postcode: item.physical_post_code || '',
    careType: item.care_type || '',
    provider: item.provider_name || '',
    acpr: item.aged_care_planning_region || '',
    remoteness: item.abs_remoteness || '',
    totalBeds: item.residential_places ?? 0,

    state: item.state || '',
    organisationType: item.organisation_type || '',
    funding: item.funding || '',
    providerType: item.provider_type || '',
    bedAvailability: item.availability_group || item.bed_availability || 'Unknown',
    estimatedWaitTime: item.estimated_wait_time || '',
    waitWeeks: item.wait_weeks ?? null,
    distance: item.distance ?? null,

    latitude: item.latitude ?? null,
    longitude: item.longitude ?? null
  }
}

export function mapFacilityMarker(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    latitude: item.latitude ?? null,
    longitude: item.longitude ?? null,
    careType: item.care_type || '',
    totalBeds: item.residential_places ?? 0,
    provider: item.provider_name || '',
    suburb: item.physical_suburb || '',
    postcode: item.physical_post_code || '',
    availability: item.availability_group || '',
    dataSource: item.data_source || ''
  }
}