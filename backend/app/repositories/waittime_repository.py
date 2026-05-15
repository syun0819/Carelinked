from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.waittime import WaitTimeRatio


async def fetch_all_ratios(db: AsyncSession) -> List[WaitTimeRatio]:
    result = await db.execute(select(WaitTimeRatio))
    return list(result.scalars().all())
