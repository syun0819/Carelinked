from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import LocationGeo


async def fetch_center_by_suburb_or_postcode(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
):
    if postcode:
        query = (
            select(LocationGeo)
            .where(LocationGeo.postcode == postcode.strip())
            .limit(1)
        )
    elif suburb:
        query = (
            select(LocationGeo)
            .where(LocationGeo.suburb.ilike(f"%{suburb.strip()}%"))
            .limit(1)
        )
    else:
        return None

    result = await db.execute(query)
    return result.scalar_one_or_none()
