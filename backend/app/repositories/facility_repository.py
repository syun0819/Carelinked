from typing import List, Optional, Tuple

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService


def _build_filter_query(
    suburb: Optional[str] = None,
    postcode: Optional[str] = None,
    region: Optional[str] = None,
    keyword: Optional[str] = None,
    care_type: Optional[List[str]] = None,
    abs_remoteness: Optional[str] = None,
    min_beds: Optional[int] = None,
    max_beds: Optional[int] = None,
    keyword_match_suburb: bool = False,
):
    query = select(AgedCareService)
    if suburb:
        query = query.where(AgedCareService.physical_suburb.ilike(f"%{suburb}%"))
    if postcode:
        query = query.where(AgedCareService.physical_post_code == postcode)
    if region:
        query = query.where(AgedCareService.aged_care_planning_region.ilike(f"%{region}%"))
    if keyword:
        if keyword_match_suburb:
            query = query.where(
                or_(
                    AgedCareService.service_name.ilike(f"%{keyword}%"),
                    AgedCareService.physical_suburb.ilike(f"%{keyword}%"),
                )
            )
        else:
            query = query.where(AgedCareService.service_name.ilike(f"%{keyword}%"))
    if care_type:
        query = query.where(AgedCareService.care_type.in_(care_type))
    if abs_remoteness:
        query = query.where(AgedCareService.abs_remoteness.ilike(f"%{abs_remoteness}%"))
    if min_beds is not None and min_beds > 0:
        query = query.where(AgedCareService.residential_places >= min_beds)
    if max_beds is not None and max_beds > 0:
        query = query.where(AgedCareService.residential_places <= max_beds)
    return query


async def fetch_by_id(db: AsyncSession, facility_id: str) -> Optional[AgedCareService]:
    result = await db.execute(
        select(AgedCareService).where(AgedCareService.id == facility_id)
    )
    return result.scalar_one_or_none()


async def fetch_all_matching(
    db: AsyncSession,
    suburb: Optional[str] = None,
    postcode: Optional[str] = None,
    region: Optional[str] = None,
    keyword: Optional[str] = None,
    care_type: Optional[List[str]] = None,
    abs_remoteness: Optional[str] = None,
    min_beds: Optional[int] = None,
    max_beds: Optional[int] = None,
    keyword_match_suburb: bool = False,
) -> List[AgedCareService]:
    query = _build_filter_query(
        suburb, postcode, region, keyword, care_type,
        abs_remoteness, min_beds, max_beds, keyword_match_suburb,
    )
    result = await db.execute(query)
    return list(result.scalars().all())


async def fetch_page(
    db: AsyncSession,
    sort_by: Optional[str],
    limit: int,
    offset: int,
    suburb: Optional[str] = None,
    postcode: Optional[str] = None,
    region: Optional[str] = None,
    keyword: Optional[str] = None,
    care_type: Optional[List[str]] = None,
    abs_remoteness: Optional[str] = None,
    min_beds: Optional[int] = None,
    max_beds: Optional[int] = None,
) -> Tuple[List[AgedCareService], int]:
    query = _build_filter_query(suburb, postcode, region, keyword, care_type, abs_remoteness, min_beds, max_beds)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    if sort_by == "beds_desc":
        query = query.order_by(AgedCareService.residential_places.desc())
    elif sort_by == "beds_asc":
        query = query.order_by(AgedCareService.residential_places.asc())
    else:
        query = query.order_by(AgedCareService.service_name.asc())

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def fetch_all_with_coords(db: AsyncSession) -> List[AgedCareService]:
    result = await db.execute(
        select(AgedCareService)
        .where(AgedCareService.latitude.isnot(None))
        .where(AgedCareService.longitude.isnot(None))
    )
    return list(result.scalars().all())


async def fetch_by_care_type_top(
    db: AsyncSession,
    care_type: str,
    sort_field,
) -> Optional[AgedCareService]:
    result = await db.execute(
        select(AgedCareService)
        .where(AgedCareService.care_type == care_type)
        .order_by(sort_field.desc().nulls_last())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def fetch_similar_candidates(
    db: AsyncSession,
    care_type: str,
    exclude_id: str,
) -> List[AgedCareService]:
    result = await db.execute(
        select(AgedCareService)
        .where(AgedCareService.care_type == care_type)
        .where(AgedCareService.id != exclude_id)
    )
    return list(result.scalars().all())
