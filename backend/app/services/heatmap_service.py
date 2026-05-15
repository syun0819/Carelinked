from typing import Any, Dict, List, Optional

from shapely import wkt as shapely_wkt
from shapely.geometry import mapping
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.heatmap import BushfireLgaSummary, CrimeRateLga, FacilityHeatRisk, LgaBoundary, ResidentialCareDemandByLga
from app.schemas.heatmap import BushfireLgaItem, CrimeStatItem, CrimeStatsResponse, HeatRiskItem, LgaStatItem


async def get_lga_boundaries_geojson(db: AsyncSession) -> Dict[str, Any]:
    q = select(
        LgaBoundary.lga_code,
        LgaBoundary.lga_name,
        LgaBoundary.state_name,
        LgaBoundary.geom_wkt,
    ).where(LgaBoundary.geom_wkt.isnot(None))
    rows = (await db.execute(q)).all()

    features = []
    for row in rows:
        try:
            geom = shapely_wkt.loads(row.geom_wkt)
            features.append({
                "type": "Feature",
                "properties": {
                    "lga_code": row.lga_code,
                    "lga_name": row.lga_name,
                    "state_name": row.state_name,
                },
                "geometry": mapping(geom),
            })
        except Exception:
            continue

    return {"type": "FeatureCollection", "features": features}


async def get_lga_supply_demand(db: AsyncSession) -> List[LgaStatItem]:
    demand_q = (
        select(
            ResidentialCareDemandByLga.lga_name,
            ResidentialCareDemandByLga.lga_code,
            func.sum(ResidentialCareDemandByLga.people_count).label("demand"),
        )
        .where(ResidentialCareDemandByLga.admission_type == "Permanent")
        .group_by(ResidentialCareDemandByLga.lga_name, ResidentialCareDemandByLga.lga_code)
    )
    demand_rows = (await db.execute(demand_q)).all()

    supply_q = (
        select(
            AgedCareService.lga_name,
            func.sum(AgedCareService.residential_places).label("supply"),
        )
        .where(AgedCareService.lga_name.isnot(None))
        .group_by(AgedCareService.lga_name)
    )
    supply_rows = (await db.execute(supply_q)).all()

    supply_map: dict[str, int] = {
        row.lga_name.upper(): (row.supply or 0) for row in supply_rows
    }

    results: List[LgaStatItem] = []
    for row in demand_rows:
        supply = supply_map.get(row.lga_name.upper(), 0)
        demand = row.demand or 0
        ratio = round(supply / demand, 4) if demand > 0 else None
        results.append(
            LgaStatItem(
                lga_name=row.lga_name,
                lga_code=row.lga_code,
                supply=supply,
                demand=demand,
                ratio=ratio,
            )
        )

    return results


async def get_crime_heatmap(db: AsyncSession, year: Optional[int] = None) -> CrimeStatsResponse:
    base_filters = (
        CrimeRateLga.measure == "OFFENCE_RATE_POOLED_NORMALISED",
        CrimeRateLga.frequency == "ANNUAL",
        CrimeRateLga.adjusted_rate.isnot(None),
    )
    years_q = (
        select(CrimeRateLga.year)
        .where(*base_filters)
        .group_by(CrimeRateLga.year)
        .order_by(desc(CrimeRateLga.year))
    )
    available_years = [row.year for row in (await db.execute(years_q)).all()]
    selected_year = year if year is not None else (available_years[0] if available_years else None)

    if selected_year is None:
        return CrimeStatsResponse(results=[], year=None, available_years=available_years)

    q = (
        select(
            CrimeRateLga.lga_name,
            func.sum(CrimeRateLga.adjusted_rate).label("adjusted_rate"),
        )
        .where(
            CrimeRateLga.year == selected_year,
            *base_filters,
        )
        .group_by(CrimeRateLga.lga_name)
    )
    rows = (await db.execute(q)).all()
    return CrimeStatsResponse(
        results=[
            CrimeStatItem(lga_name=row.lga_name, adjusted_rate=float(row.adjusted_rate))
            for row in rows
        ],
        year=selected_year,
        available_years=available_years,
    )


async def get_bushfire_heatmap(db: AsyncSession) -> List[BushfireLgaItem]:
    q = select(
        BushfireLgaSummary.lga_name,
        BushfireLgaSummary.lga_code,
        BushfireLgaSummary.bushfire_count,
    ).order_by(BushfireLgaSummary.bushfire_count.desc())
    rows = (await db.execute(q)).all()
    return [
        BushfireLgaItem(
            lga_name=row.lga_name,
            lga_code=row.lga_code,
            bushfire_count=row.bushfire_count,
        )
        for row in rows
    ]


async def get_facility_heat_risk(db: AsyncSession) -> List[HeatRiskItem]:
    q = select(
        FacilityHeatRisk.latitude,
        FacilityHeatRisk.longitude,
        FacilityHeatRisk.heat_risk,
        FacilityHeatRisk.risk_score,
    ).where(
        FacilityHeatRisk.latitude.isnot(None),
        FacilityHeatRisk.longitude.isnot(None),
        FacilityHeatRisk.heat_risk.in_(["low", "medium", "high"]),
    )
    rows = (await db.execute(q)).all()
    return [
        HeatRiskItem(
            lat=row.latitude,
            lon=row.longitude,
            heat_risk=row.heat_risk,
            risk_score=float(row.risk_score) if row.risk_score is not None else None,
        )
        for row in rows
    ]
