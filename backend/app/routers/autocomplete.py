from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.aged_care import AutoCompleteResponse
from app.services.autocomplete_service import get_autocomplete

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("/autocomplete", response_model=AutoCompleteResponse)
@limiter.limit("60/minute")
@cache(expire=60)
async def autocomplete(
    request: Request,
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    if len(q.strip()) < 2:
        return AutoCompleteResponse()
    return await get_autocomplete(db, q.strip())
