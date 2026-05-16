from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.heatmap import BushfireLgaResponse, CrimeStatsResponse, HeatRiskResponse, LgaStatsResponse
from app.services.heatmap_service import get_bushfire_heatmap, get_crime_heatmap, get_facility_heat_risk, get_lga_boundaries_geojson, get_lga_supply_demand

router = APIRouter(prefix="/api/v1/heatmap", tags=["heatmap"])


@router.get("/lga-boundaries")
@limiter.limit("10/minute")
@cache(expire=86400)
async def lga_boundaries(request: Request, db: AsyncSession = Depends(get_db)):
    geojson = await get_lga_boundaries_geojson(db)
    return JSONResponse(content=geojson)


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
    return BushfireLgaResponse(results=results)


@router.get("/heat-risk", response_model=HeatRiskResponse)
@limiter.limit("30/minute")
@cache(expire=3600)
async def heat_risk(request: Request, db: AsyncSession = Depends(get_db)):
    results = await get_facility_heat_risk(db)
    return HeatRiskResponse(results=results)


@router.get("/crime", response_model=CrimeStatsResponse)
@limiter.limit("30/minute")
async def crime_heatmap(
    request: Request,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_crime_heatmap(db, year)
