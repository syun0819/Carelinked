from fastapi import APIRouter, Depends, Request
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.heatmap import BushfireLgaResponse, CrimeStatsResponse, LgaStatsResponse
from app.services.heatmap_service import get_bushfire_heatmap, get_crime_heatmap, get_lga_supply_demand

router = APIRouter(prefix="/api/v1/heatmap", tags=["heatmap"])


@router.get("/demand", response_model=LgaStatsResponse)
@limiter.limit("30/minute")
@cache(expire=3600)
async def demand_heatmap(request: Request, db: AsyncSession = Depends(get_db)):
    results = await get_lga_supply_demand(db)
    return LgaStatsResponse(results=results)


@router.get("/bushfire", response_model=BushfireLgaResponse)
@limiter.limit("30/minute")
@cache(expire=3600)
async def bushfire_heatmap(request: Request, db: AsyncSession = Depends(get_db)):
    results = await get_bushfire_heatmap(db)
    return BushfireHeatResponse(results=results)


@router.get("/crime", response_model=CrimeStatsResponse)
@limiter.limit("30/minute")
@cache(expire=3600)
async def crime_heatmap(request: Request, db: AsyncSession = Depends(get_db)):
    results = await get_crime_heatmap(db)
    return CrimeStatsResponse(results=results)
