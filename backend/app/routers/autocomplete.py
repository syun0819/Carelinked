import re
from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.aged_care import AutoCompleteResponse
from app.services.autocomplete_service import get_autocomplete

def validate_search_query(q: str) -> str:
    if re.search(r"['\";\\<>]", q):
        raise HTTPException(status_code=400, detail="Search query contains invalid characters.")
    return q

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("/autocomplete", response_model=AutoCompleteResponse)
@limiter.limit("60/minute")
@cache(expire=60)
async def autocomplete(
    request: Request,
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    q = validate_search_query(q)
    if len(q.strip()) < 2:
        return AutoCompleteResponse()
    return await get_autocomplete(db, q.strip())
