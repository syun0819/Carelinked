from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.availability import FacilityAvailabilityML


async def fetch_bulk(db: AsyncSession, facility_ids: List[str]) -> Dict[str, FacilityAvailabilityML]:
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


async def fetch_one(db: AsyncSession, facility_id: str) -> Optional[FacilityAvailabilityML]:
    try:
        result = await db.execute(
            select(FacilityAvailabilityML)
            .where(FacilityAvailabilityML.facility_id == facility_id)
            .limit(1)
        )
        return result.scalar_one_or_none()
    except Exception:
        return None
