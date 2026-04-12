import math
from typing import Optional, Tuple, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.availability import FacilityAvailabilityML
from app.schemas.aged_care import FacilityCard, FacilityDetail, FacilityMapMarker

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
    care_type: Optional[str],
) -> Optional[str]:
    if ml_record is None:
        return None
    if care_type == "Home Care":
        label = ml_record.home_care_label_name
    elif care_type in ("Short-Term Restorative Care (STRC)", "Transition Care"):
        label = ml_record.restorative_care_label_name
    else:
        label = ml_record.residential_label_name
    return label if label else None


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


async def search_facilities(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
    region: Optional[str],
    keyword: Optional[str],
    care_type: Optional[str],
    abs_remoteness: Optional[str],
    min_beds: Optional[int],
    max_beds: Optional[int],
    sort_by: Optional[str],
    limit: int,
    offset: int,
) -> Tuple[List[AgedCareService], int]:
    query = select(AgedCareService).where(AgedCareService.physical_state == "VIC")

    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))
    if keyword:
        query = query.where(AgedCareService.service_name.ilike(f"%{keyword}%"))

    if care_type:
        query = query.where(AgedCareService.care_type == care_type)
    if abs_remoteness:
        query = query.where(AgedCareService.abs_remoteness.ilike(f"%{abs_remoteness}%"))
    if min_beds is not None:
        query = query.where(AgedCareService.residential_places >= min_beds)
    if max_beds is not None:
        query = query.where(AgedCareService.residential_places <= max_beds)

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
        ml_label = get_ml_availability_group(ml_map.get(row.id), row.care_type)
        row._availability_group = ml_label or calculate_availability(row.residential_places)
        row._data_source = _DATA_SOURCE_ML if ml_label else _DATA_SOURCE_BEDS

    return rows, total


async def get_facilities_for_map(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
    region: Optional[str],
    care_type: Optional[str],
    max_distance_km: Optional[float],
    center_lat: Optional[float],
    center_lng: Optional[float],
) -> Tuple[List[FacilityMapMarker], int]:
    query = select(AgedCareService).where(AgedCareService.physical_state == "VIC")

    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))
    if care_type:
        query = query.where(AgedCareService.care_type == care_type)

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

        ml_label = get_ml_availability_group(ml_map.get(row.id), row.care_type)
        availability_group = ml_label or calculate_availability(row.residential_places)
        data_source = _DATA_SOURCE_ML if ml_label else _DATA_SOURCE_BEDS

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
        .where(AgedCareService.physical_state == "VIC")
    )
    result = await db.execute(query)
    row = result.scalar_one_or_none()
    if row is None:
        return None

    ml_record = await _fetch_ml_record(db, facility_id)
    ml_label = get_ml_availability_group(ml_record, row.care_type)

    detail = FacilityDetail.model_validate(row)
    if ml_label:
        detail.availability_group = ml_label
        detail.data_source = _DATA_SOURCE_ML
    else:
        detail.availability_group = calculate_availability(row.residential_places)
        detail.data_source = _DATA_SOURCE_BEDS
    return detail


_CARE_TYPE_SORT_FIELD = {
    "Residential": AgedCareService.residential_places,
    "Home Care": AgedCareService.home_care_places,
    "Short-Term Restorative Care (STRC)": AgedCareService.restorative_care_places,
    "Transition Care": AgedCareService.restorative_care_places,
    "Multi-Purpose Service": AgedCareService.residential_places,
    "National Aboriginal and Torres Strait Islander Aged Care Program": AgedCareService.home_care_places,
}


async def get_recommended_facilities(db: AsyncSession) -> List[FacilityCard]:
    results: List[FacilityCard] = []
    for care_type, sort_field in _CARE_TYPE_SORT_FIELD.items():
        query = (
            select(AgedCareService)
            .where(AgedCareService.physical_state == "VIC")
            .where(AgedCareService.care_type == care_type)
            .order_by(sort_field.desc().nulls_last())
            .limit(1)
        )
        row = (await db.execute(query)).scalar_one_or_none()
        if row:
            results.append(FacilityCard.model_validate(row))
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
        .where(AgedCareService.physical_state == "VIC")
        .where(AgedCareService.care_type == target.care_type)
        .where(AgedCareService.id != target.id)
    )
    result = await db.execute(query)
    candidates = result.scalars().all()

    if target.latitude is None or target.longitude is None:
        return [FacilityCard.model_validate(r) for r in candidates[:limit]]

    with_distance = [
        (haversine_distance(target.latitude, target.longitude, r.latitude, r.longitude), r)
        for r in candidates
        if r.latitude is not None and r.longitude is not None
    ]
    with_distance.sort(key=lambda x: x[0])

    return [FacilityCard.model_validate(r) for _, r in with_distance[:limit]]
