from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quality import StarRating
from app.repositories import quality_repository as quality_repo


async def get_quality_by_facility_id(
    db: AsyncSession,
    facility_id: str,
) -> Optional[StarRating]:
    return await quality_repo.fetch_one(db, facility_id)


async def get_quality_by_facility_ids(
    db: AsyncSession,
    facility_ids: List[str],
) -> List[StarRating]:
    mapping = await quality_repo.fetch_bulk(db, facility_ids)
    return list(mapping.values())
