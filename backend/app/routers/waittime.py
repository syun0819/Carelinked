from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.waittime import WaitTimeEstimateRequest, WaitTimeEstimateResponse
from app.services.waittime_service import estimate_wait_time

router = APIRouter(prefix="/api/v1/waittime", tags=["waittime"])


@router.post("/estimate", response_model=WaitTimeEstimateResponse)
@limiter.limit("30/minute")
async def estimate(
    request: Request,
    body: WaitTimeEstimateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await estimate_wait_time(db, body)
