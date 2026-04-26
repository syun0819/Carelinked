from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.quality import StarRating


async def get_quality_by_facility_id(
    db: AsyncSession,
    facility_id: str,
) -> Optional[StarRating]:
    result = await db.execute(
        select(StarRating)
        .where(StarRating.service_id == facility_id)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_quality_by_facility_ids(
    db: AsyncSession,
    facility_ids: List[str],
) -> List[StarRating]:
    result = await db.execute(
        select(StarRating)
        .where(StarRating.service_id.in_(facility_ids))
    )
    return list(result.scalars().all())
