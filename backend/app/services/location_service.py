from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import LocationGeo


async def get_location_center(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
) -> Tuple[Optional[float], Optional[float]]:
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
        return (None, None)

    result = await db.execute(query)
    row = result.scalar_one_or_none()

    if row is None:
        return (None, None)

    return (float(row.latitude), float(row.longitude))
