from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import location_repository as location_repo


async def get_location_center(
    db: AsyncSession,
    suburb: Optional[str],
    postcode: Optional[str],
) -> Tuple[Optional[float], Optional[float]]:
    row = await location_repo.fetch_center_by_suburb_or_postcode(db, suburb, postcode)
    if row is None:
        return (None, None)
    return (float(row.latitude), float(row.longitude))
