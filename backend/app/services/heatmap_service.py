import math
from typing import List

from sqlalchemy import select, func, cast, Numeric, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.heatmap import BushfireExtent, ResidentialCareDemandByLga
from app.schemas.heatmap import BushfireHeatPoint, LgaStatItem


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


async def get_bushfire_heatmap(db: AsyncSession) -> List[BushfireHeatPoint]:
    lat_num = cast(BushfireExtent.centroid_lat, Numeric(10, 4))
    lon_num = cast(BushfireExtent.centroid_lon, Numeric(10, 4))
    grid_lat = (func.round(lat_num / 0.5, 0) * 0.5).label("lat")
    grid_lon = (func.round(lon_num / 0.5, 0) * 0.5).label("lon")

    q = (
        select(grid_lat, grid_lon, func.sum(BushfireExtent.area_ha).label("total_ha"))
        .where(
            BushfireExtent.centroid_lat.isnot(None),
            BushfireExtent.centroid_lon.isnot(None),
        )
        .group_by(text("1"), text("2"))
    )
    rows = (await db.execute(q)).all()
    if not rows:
        return []

    max_log = math.log1p(max(row.total_ha or 0 for row in rows))
    if max_log == 0:
        max_log = 1
    return [
        BushfireHeatPoint(
            lat=float(row.lat),
            lon=float(row.lon),
            intensity=round(math.log1p(row.total_ha or 0) / max_log, 4),
        )
        for row in rows
    ]
