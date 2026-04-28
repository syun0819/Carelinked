import facilityExampleImage from '../assets/facility_example.jpg'

const DEFAULT_IMAGE = facilityExampleImage

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
    distance: item.distance_km ?? null,

    image: DEFAULT_IMAGE,
  }
}

export function mapFacilityDetail(item) {
  return {
    id: item.id,
    name: item.service_name || '',
    address: item.physical_address || '',
    suburb: item.physical_suburb || '',
    state: item.physical_state || '',
    postcode: item.physical_post_code || '',
    careType: item.care_type || '',
    provider: item.provider_name || '',
    acpr: item.aged_care_planning_region || '',
    remoteness: item.abs_remoteness || '',
    totalBeds: item.residential_places ?? 0,
    restorativeCarePlaces: item.restorative_care_places ?? 0,
    bedAvailability: item.availability_group || 'Unknown',
    latitude: item.latitude ?? null,
    longitude: item.longitude ?? null,
    organisationType: item.organisation_type || '',
    governmentFunding: item.australian_government_funding ?? null,

    // Star ratings (1–5 integers)
    overallStarRating: item.overall_star_rating ?? null,
    residentsExperienceRating: item.residents_experience_rating ?? null,
    complianceRating: item.compliance_rating ?? null,
    staffingRating: item.staffing_rating ?? null,
    qualityMeasuresRating: item.quality_measures_rating ?? null,

    // Resident experience sub-scores (0–1 floats)
    reFoodScore: item.re_food_score ?? null,
    reSafetyScore: item.re_safety_score ?? null,
    reRespectScore: item.re_respect_score ?? null,
    reCaringScore: item.re_caring_score ?? null,
    reHomeScore: item.re_home_score ?? null,
    reVoiceScore: item.re_voice_score ?? null,
    reExplainScore: item.re_explain_score ?? null,
    reFollowUpScore: item.re_follow_up_score ?? null,
    reIndependentScore: item.re_independent_score ?? null,
    reCompetentScore: item.re_competent_score ?? null,
    reCareNeedScore: item.re_care_need_score ?? null,
    reOperationScore: item.re_operation_score ?? null,

    // Staffing minutes
    sRnCareMinutesTarget: item.s_rn_care_minutes_target ?? null,
    sRnCareMinutesActual: item.s_rn_care_minutes_actual ?? null,
    sTotalCareMinutesTarget: item.s_total_care_minutes_target ?? null,
    sTotalCareMinutesActual: item.s_total_care_minutes_actual ?? null,
    rnMinutesMet: item.rn_minutes_met ?? null,
    totalMinutesMet: item.total_minutes_met ?? null,

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
