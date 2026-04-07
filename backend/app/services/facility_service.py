import math
from typing import Optional, Tuple, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.schemas.aged_care import FacilityMapMarker

_DATA_SOURCE = "Based on residential bed capacity data (aged_care_services)"


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


async def search_facilities(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
    region: Optional[str],
    care_type: Optional[str],
    abs_remoteness: Optional[str],
    min_beds: Optional[int],
    max_beds: Optional[int],
    sort_by: Optional[str],
    limit: int,
    offset: int,
) -> Tuple[List[AgedCareService], int]:
    query = select(AgedCareService).where(AgedCareService.physical_state == "VIC")

    # Search conditions
    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))

    # Filter conditions
    if care_type:
        query = query.where(AgedCareService.care_type == care_type)
    if abs_remoteness:
        query = query.where(AgedCareService.abs_remoteness.ilike(f"%{abs_remoteness}%"))
    if min_beds is not None:
        query = query.where(AgedCareService.residential_places >= min_beds)
    if max_beds is not None:
        query = query.where(AgedCareService.residential_places <= max_beds)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Sorting
    if sort_by == "beds_desc":
        query = query.order_by(AgedCareService.residential_places.desc())
    elif sort_by == "beds_asc":
        query = query.order_by(AgedCareService.residential_places.asc())
    else:
        query = query.order_by(AgedCareService.service_name.asc())

    # Pagination
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    rows = list(result.scalars().all())

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

        markers.append(
            FacilityMapMarker(
                id=row.id,
                service_name=row.service_name,
                latitude=row.latitude,
                longitude=row.longitude,
                care_type=row.care_type,
                residential_places=row.residential_places,
                availability_group=calculate_availability(row.residential_places),
                data_source=_DATA_SOURCE,
                provider_name=row.provider_name,
                physical_suburb=row.physical_suburb,
                physical_post_code=row.physical_post_code,
            )
        )

    return markers, len(markers)


async def get_facility_by_id(
    db: AsyncSession,
    facility_id: str,
) -> Optional[AgedCareService]:
    query = (
        select(AgedCareService)
        .where(AgedCareService.id == facility_id)
        .where(AgedCareService.physical_state == "VIC")
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()
