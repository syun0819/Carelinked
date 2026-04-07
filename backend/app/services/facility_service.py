from typing import Optional, Tuple, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService


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
