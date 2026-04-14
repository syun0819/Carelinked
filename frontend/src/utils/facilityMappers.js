const DEFAULT_IMAGE =
  'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1200&q=80'

export function mapFacilityCard(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    address: item.physical_address || '',
    suburb: item.physical_suburb || '',
    postcode: item.physical_post_code || '',
    careType: item.care_type || '',
    provider: item.provider_name || '',
    acpr: item.aged_care_planning_region || '',
    remoteness: item.abs_remoteness || '',
    totalBeds: item.residential_places ?? 0,
    bedAvailability: item.availability_group || 'Unknown',
    
    image: DEFAULT_IMAGE,
  }
}

export function mapFacilityDetail(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    address: item.physical_address || '',
    suburb: item.physical_suburb || '',
    postcode: item.physical_post_code || '',
    careType: item.care_type || '',
    provider: item.provider_name || '',
    acpr: item.aged_care_planning_region || '',
    remoteness: item.abs_remoteness || '',
    totalBeds: item.residential_places ?? 0,
    homeCarePlaces: item.home_care_places ?? 0,
    restorativeCarePlaces: item.restorative_care_places ?? 0,
    bedAvailability: item.availability_group || 'Unknown',
    latitude: item.latitude ?? null,
    longitude: item.longitude ?? null,
    organisationType: item.organisation_type || '',
    governmentFunding: item.australian_government_funding ?? null,

    image: DEFAULT_IMAGE,
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