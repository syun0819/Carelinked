import math
from typing import Optional, Tuple, List

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.availability import FacilityAvailabilityML
from app.models.quality import StarRating
from app.schemas.aged_care import FacilityCard, FacilityDetail, FacilityMapMarker
from app.services import location_service
from app.services.matching_service import calculate_match_score, get_match_category, is_matching_active

_DATA_SOURCE_BEDS = "Based on residential bed capacity data (aged_care_services)"
_DATA_SOURCE_ML = "Based on ML prediction model (aged_care_facility_availability)"

# Keep backward compat alias
_DATA_SOURCE = _DATA_SOURCE_BEDS


def calculate_availability(residential_places: Optional[int]) -> str:
    if residential_places is None:
        return "Possibly Available"
    if residential_places >= 100:
        return "Likely Available"
    if residential_places >= 30:
        return "Possibly Available"
    return "Likely Unavailable"


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_ml_availability_group(
    ml_record: Optional[FacilityAvailabilityML],
    care_type: Optional[str] = None,  # noqa: ARG001
) -> Optional[str]:
    if ml_record is None:
        return None
    label = ml_record.residential_label_name
    return label if label else None


def resolve_availability(ml_map: dict, row) -> tuple:
    ml_label = get_ml_availability_group(ml_map.get(row.id), row.care_type)
    availability_group = ml_label or calculate_availability(row.residential_places)
    data_source = _DATA_SOURCE_ML if ml_label else _DATA_SOURCE_BEDS
    return availability_group, data_source


async def _fetch_ml_record(db: AsyncSession, facility_id: str) -> Optional[FacilityAvailabilityML]:
    try:
        result = await db.execute(
            select(FacilityAvailabilityML)
            .where(FacilityAvailabilityML.facility_id == facility_id)
            .limit(1)
        )
        return result.scalar_one_or_none()
    except Exception:
        return None


async def _fetch_ml_records_bulk(db: AsyncSession, facility_ids: List[str]) -> dict:
    """Returns {facility_id: FacilityAvailabilityML}."""
    if not facility_ids:
        return {}
    try:
        result = await db.execute(
            select(FacilityAvailabilityML)
            .where(FacilityAvailabilityML.facility_id.in_(facility_ids))
        )
        return {row.facility_id: row for row in result.scalars().all()}
    except Exception:
        return {}


async def _fetch_star_rating_records_bulk(db: AsyncSession, facility_ids: List[str]) -> dict:
    """Returns {service_id: StarRating}."""
    if not facility_ids:
        return {}
    try:
        result = await db.execute(
            select(StarRating)
            .where(StarRating.service_id.in_(facility_ids))
        )
        return {str(row.service_id): row for row in result.scalars().all()}
    except Exception:
        return {}


def _apply_match_scores(rows: list, star_map: dict, match_weights: Optional[dict]) -> list:
    if not is_matching_active(match_weights):
        return rows

    for row in rows:
        score = calculate_match_score(star_map.get(str(row.id)), match_weights)
        row.match_score = score
        row.match_category = get_match_category(score)

    rows.sort(
        key=lambda row: (
            getattr(row, "match_score", None) is None,
            -(getattr(row, "match_score", None) or 0),
            row.service_name or "",
        )
    )
    return rows


def _sort_rows(rows: list, sort_by: Optional[str], user_lat: Optional[float], user_lng: Optional[float]) -> list:
    """Sort a list of AgedCareService rows. Rows without coords go last for distance sort."""
    if sort_by == "beds_desc":
        rows.sort(key=lambda r: r.residential_places or 0, reverse=True)
    elif sort_by == "beds_asc":
        rows.sort(key=lambda r: r.residential_places or 0)
    elif sort_by == "distance" and user_lat is not None and user_lng is not None:
        def dist_key(r):
            if r.latitude is None or r.longitude is None:
                return float("inf")
            return haversine_distance(user_lat, user_lng, r.latitude, r.longitude)
        rows.sort(key=dist_key)
    else:
        rows.sort(key=lambda r: r.service_name or "")
    return rows


async def search_facilities(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
    region: Optional[str],
    keyword: Optional[str],
    care_type: Optional[List[str]],
    abs_remoteness: Optional[str],
    min_beds: Optional[int],
    max_beds: Optional[int],
    sort_by: Optional[str],
    limit: int,
    offset: int,
    max_distance_km: Optional[float] = None,
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
    match_weights: Optional[dict] = None,
) -> Tuple[List[AgedCareService], int]:
    query = select(AgedCareService)

    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))
    if keyword:
        query = query.where(AgedCareService.service_name.ilike(f"%{keyword}%"))

    if care_type:
        query = query.where(AgedCareService.care_type.in_(care_type))
    if abs_remoteness:
        query = query.where(AgedCareService.abs_remoteness.ilike(f"%{abs_remoteness}%"))
    if min_beds is not None and min_beds > 0:
        query = query.where(AgedCareService.residential_places >= min_beds)
    if max_beds is not None and max_beds > 0:
        query = query.where(AgedCareService.residential_places <= max_beds)

    # Resolve center coords from postcode or suburb when distance filtering is requested
    center_lat, center_lng = None, None
    if max_distance_km is not None and (postcode or suburb):
        center_lat, center_lng = await location_service.get_location_center(
            db=db, suburb=suburb, postcode=postcode
        )

    apply_distance_filter = center_lat is not None and center_lng is not None and max_distance_km is not None
    apply_distance_sort = sort_by == "distance" and user_lat is not None and user_lng is not None
    apply_match_sort = is_matching_active(match_weights)

    if apply_distance_filter or apply_distance_sort or apply_match_sort:
        result = await db.execute(query)
        all_rows = list(result.scalars().all())

        if apply_distance_filter:
            all_rows = [
                r for r in all_rows
                if r.latitude is not None
                and r.longitude is not None
                and haversine_distance(center_lat, center_lng, r.latitude, r.longitude) <= max_distance_km
            ]

        if apply_match_sort:
            star_map = await _fetch_star_rating_records_bulk(db, [r.id for r in all_rows])
            all_rows = _apply_match_scores(all_rows, star_map, match_weights)
        else:
            all_rows = _sort_rows(all_rows, sort_by, user_lat, user_lng)

        total = len(all_rows)
        rows = all_rows[offset: offset + limit]
    else:
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        if sort_by == "beds_desc":
            query = query.order_by(AgedCareService.residential_places.desc())
        elif sort_by == "beds_asc":
            query = query.order_by(AgedCareService.residential_places.asc())
        else:
            query = query.order_by(AgedCareService.service_name.asc())

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        rows = list(result.scalars().all())

    ml_map = await _fetch_ml_records_bulk(db, [r.id for r in rows])
    for row in rows:
        row._availability_group, row._data_source = resolve_availability(ml_map, row)
        if not hasattr(row, "match_score"):
            row.match_score = None
        if not hasattr(row, "match_category"):
            row.match_category = None

    return rows, total


async def get_facilities_for_map(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
    region: Optional[str],
    keyword: Optional[str],
    care_type: Optional[List[str]],
    max_distance_km: Optional[float],
    center_lat: Optional[float],
    center_lng: Optional[float],
) -> Tuple[List[FacilityMapMarker], int]:
    query = select(AgedCareService)

    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))
    if care_type:
        query = query.where(AgedCareService.care_type.in_(care_type))
    if keyword:
        query = query.where(
            or_(
                AgedCareService.service_name.ilike(f"%{keyword}%"),
                AgedCareService.physical_suburb.ilike(f"%{keyword}%"),
            )
        )

    result = await db.execute(query)
    rows = result.scalars().all()

    ml_map = await _fetch_ml_records_bulk(db, [r.id for r in rows])

    apply_distance = (
        max_distance_km is not None
        and center_lat is not None
        and center_lng is not None
    )

    markers: List[FacilityMapMarker] = []
    for row in rows:
        if apply_distance:
            if row.latitude is None or row.longitude is None:
                continue
            dist = haversine_distance(center_lat, center_lng, row.latitude, row.longitude)
            if dist > max_distance_km:
                continue

        availability_group, data_source = resolve_availability(ml_map, row)

        markers.append(
            FacilityMapMarker(
                id=row.id,
                service_name=row.service_name,
                latitude=row.latitude,
                longitude=row.longitude,
                care_type=row.care_type,
                residential_places=row.residential_places,
                availability_group=availability_group,
                data_source=data_source,
                provider_name=row.provider_name,
                physical_suburb=row.physical_suburb,
                physical_post_code=row.physical_post_code,
            )
        )

    return markers, len(markers)


async def get_facility_by_id(
    db: AsyncSession,
    facility_id: str,
) -> Optional[FacilityDetail]:
    query = (
        select(AgedCareService)
        .where(AgedCareService.id == facility_id)
    )
    result = await db.execute(query)
    row = result.scalar_one_or_none()
    if row is None:
        return None

    ml_map = await _fetch_ml_records_bulk(db, [facility_id])
    detail = FacilityDetail.model_validate(row)
    detail.availability_group, detail.data_source = resolve_availability(ml_map, row)

    try:
        quality_result = await db.execute(
            select(StarRating)
            .where(StarRating.service_id == facility_id)
            .limit(1)
        )
        quality_row = quality_result.scalar_one_or_none()
        if quality_row:
            detail.overall_star_rating = quality_row.overall_star_rating
            detail.residents_experience_rating = quality_row.residents_experience_rating
            detail.compliance_rating = quality_row.compliance_rating
            detail.staffing_rating = quality_row.staffing_rating
            detail.quality_measures_rating = quality_row.quality_measures_rating
            detail.re_food_score = float(quality_row.re_food_score) if quality_row.re_food_score else None
            detail.re_safety_score = float(quality_row.re_safety_score) if quality_row.re_safety_score else None
            detail.re_respect_score = float(quality_row.re_respect_score) if quality_row.re_respect_score else None
            detail.re_caring_score = float(quality_row.re_caring_score) if quality_row.re_caring_score else None
            detail.re_home_score = float(quality_row.re_home_score) if quality_row.re_home_score else None
            detail.re_voice_score = float(quality_row.re_voice_score) if quality_row.re_voice_score else None
            detail.re_explain_score = float(quality_row.re_explain_score) if quality_row.re_explain_score else None
            detail.re_follow_up_score = float(quality_row.re_follow_up_score) if quality_row.re_follow_up_score else None
            detail.re_independent_score = float(quality_row.re_independent_score) if quality_row.re_independent_score else None
            detail.re_competent_score = float(quality_row.re_competent_score) if quality_row.re_competent_score else None
            detail.re_care_need_score = float(quality_row.re_care_need_score) if quality_row.re_care_need_score else None
            detail.re_operation_score = float(quality_row.re_operation_score) if quality_row.re_operation_score else None
            detail.s_rn_care_minutes_target = float(quality_row.s_rn_care_minutes_target) if quality_row.s_rn_care_minutes_target else None
            detail.s_rn_care_minutes_actual = float(quality_row.s_rn_care_minutes_actual) if quality_row.s_rn_care_minutes_actual else None
            detail.s_total_care_minutes_target = float(quality_row.s_total_care_minutes_target) if quality_row.s_total_care_minutes_target else None
            detail.s_total_care_minutes_actual = float(quality_row.s_total_care_minutes_actual) if quality_row.s_total_care_minutes_actual else None
            if quality_row.s_rn_care_minutes_actual is not None and quality_row.s_rn_care_minutes_target is not None:
                detail.rn_minutes_met = float(quality_row.s_rn_care_minutes_actual) >= float(quality_row.s_rn_care_minutes_target)
            if quality_row.s_total_care_minutes_actual is not None and quality_row.s_total_care_minutes_target is not None:
                detail.total_minutes_met = float(quality_row.s_total_care_minutes_actual) >= float(quality_row.s_total_care_minutes_target)
    except Exception:
        pass

    return detail


_CARE_TYPE_SORT_FIELD = {
    "Residential": AgedCareService.residential_places,
    "Short-Term Restorative Care (STRC)": AgedCareService.restorative_care_places,
    "Transition Care": AgedCareService.restorative_care_places,
    "Multi-Purpose Service": AgedCareService.residential_places,
    "National Aboriginal and Torres Strait Islander Aged Care Program": AgedCareService.home_care_places,
}


async def get_recommended_facilities(
    db: AsyncSession,
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None,
) -> List[FacilityCard]:
    if user_lat is not None and user_lng is not None:
        return await get_nearest_facilities(db, user_lat, user_lng, limit=6)

    results: List[FacilityCard] = []
    for care_type, sort_field in _CARE_TYPE_SORT_FIELD.items():
        query = (
            select(AgedCareService)
            .where(AgedCareService.care_type == care_type)
            .order_by(sort_field.desc().nulls_last())
            .limit(1)
        )
        row = (await db.execute(query)).scalar_one_or_none()
        if row:
            ml_map = await _fetch_ml_records_bulk(db, [row.id])
            card = FacilityCard.model_validate(row)
            card.availability_group, card.data_source = resolve_availability(ml_map, row)
            results.append(card)
    return results


async def get_similar_facilities(
    db: AsyncSession,
    facility_id: str,
    limit: int = 4,
) -> List[FacilityCard]:
    target = await get_facility_by_id(db, facility_id)
    if target is None:
        return []

    query = (
        select(AgedCareService)
        .where(AgedCareService.care_type == target.care_type)
        .where(AgedCareService.id != target.id)
    )
    result = await db.execute(query)
    candidates = result.scalars().all()

    if target.latitude is None or target.longitude is None:
        nearest = list(candidates[:limit])
    else:
        with_distance = [
            (haversine_distance(target.latitude, target.longitude, r.latitude, r.longitude), r)
            for r in candidates
            if r.latitude is not None and r.longitude is not None
        ]
        with_distance.sort(key=lambda x: x[0])
        nearest = [r for _, r in with_distance[:limit]]

    ml_map = await _fetch_ml_records_bulk(db, [r.id for r in nearest])
    cards: List[FacilityCard] = []
    for r in nearest:
        card = FacilityCard.model_validate(r)
        card.availability_group, card.data_source = resolve_availability(ml_map, r)
        card.distance_km = round(
            haversine_distance(target.latitude, target.longitude, r.latitude, r.longitude), 2
        ) if target.latitude and target.longitude and r.latitude and r.longitude else None
        cards.append(card)
    return cards


async def get_nearest_facilities(
    db: AsyncSession,
    user_lat: float,
    user_lng: float,
    limit: int = 6,
) -> List[FacilityCard]:
    query = (
        select(AgedCareService)
        .where(AgedCareService.latitude.isnot(None))
        .where(AgedCareService.longitude.isnot(None))
    )
    result = await db.execute(query)
    rows = result.scalars().all()

    with_distance = [
        (haversine_distance(user_lat, user_lng, r.latitude, r.longitude), r)
        for r in rows
    ]
    with_distance.sort(key=lambda x: x[0])
    nearest = [(dist, r) for dist, r in with_distance[:limit]]

    ml_map = await _fetch_ml_records_bulk(db, [r.id for _, r in nearest])
    cards: List[FacilityCard] = []
    for dist, r in nearest:
        card = FacilityCard.model_validate(r)
        card.availability_group, card.data_source = resolve_availability(ml_map, r)
        card.distance_km = round(dist, 2)
        cards.append(card)
    return cards
