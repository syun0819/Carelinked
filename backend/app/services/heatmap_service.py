from typing import Any, Dict, List, Optional

from shapely import wkt as shapely_wkt
from shapely.geometry import mapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import heatmap_repository as heatmap_repo
from app.schemas.heatmap import BushfireLgaItem, CrimeStatItem, CrimeStatsResponse, HeatRiskItem, LgaStatItem


async def get_lga_boundaries_geojson(db: AsyncSession) -> Dict[str, Any]:
    rows = await heatmap_repo.fetch_lga_boundaries(db)

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
    demand_rows = await heatmap_repo.fetch_demand_by_lga(db)
    supply_rows = await heatmap_repo.fetch_supply_by_lga(db)

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
    available_years = await heatmap_repo.fetch_crime_years(db)
    selected_year = year if year is not None else (available_years[0] if available_years else None)

    if selected_year is None:
        return CrimeStatsResponse(results=[], year=None, available_years=available_years)

    rows = await heatmap_repo.fetch_crime_rates(db, selected_year)
    return CrimeStatsResponse(
        results=[
            CrimeStatItem(lga_name=row.lga_name, adjusted_rate=float(row.adjusted_rate))
            for row in rows
        ],
        year=selected_year,
        available_years=available_years,
    )


async def get_bushfire_heatmap(db: AsyncSession) -> List[BushfireLgaItem]:
    rows = await heatmap_repo.fetch_bushfire_by_lga(db)
    return [
        BushfireLgaItem(
            lga_name=row.lga_name,
            lga_code=row.lga_code,
            bushfire_count=row.bushfire_count,
        )
        for row in rows
    ]


async def get_facility_heat_risk(db: AsyncSession) -> List[HeatRiskItem]:
    rows = await heatmap_repo.fetch_facility_heat_risk(db)
    return [
        HeatRiskItem(
            lat=row.latitude,
            lon=row.longitude,
            heat_risk=row.heat_risk,
            risk_score=float(row.risk_score) if row.risk_score is not None else None,
        )
        for row in rows
    ]
