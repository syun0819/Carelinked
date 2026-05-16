from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quality import StarRating


async def fetch_bulk(db: AsyncSession, facility_ids: List[str]) -> Dict[str, StarRating]:
    if not facility_ids:
        return {}
    try:
        result = await db.execute(
            select(StarRating).where(StarRating.service_id.in_(facility_ids))
        )
        return {str(row.service_id): row for row in result.scalars().all()}
    except Exception:
        return {}


async def fetch_one(db: AsyncSession, facility_id: str) -> Optional[StarRating]:
    try:
        result = await db.execute(
            select(StarRating).where(StarRating.service_id == facility_id).limit(1)
        )
        return result.scalar_one_or_none()
    except Exception:
        return None
