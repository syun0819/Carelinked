from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.heatmap import BushfireLgaSummary, CrimeRateLga, ResidentialCareDemandByLga
from app.schemas.heatmap import BushfireLgaItem, CrimeStatItem, LgaStatItem


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


async def get_crime_heatmap(db: AsyncSession) -> List[CrimeStatItem]:
    latest_year_q = select(func.max(CrimeRateLga.year)).where(
        CrimeRateLga.offence == "dwelling",
        CrimeRateLga.measure == "OFFENCE_RATE_POOLED_NORMALISED",
        CrimeRateLga.frequency == "ANNUAL",
        CrimeRateLga.adjusted_rate.isnot(None),
    )
    latest_year = (await db.execute(latest_year_q)).scalar()
    if latest_year is None:
        return []

    q = (
        select(
            CrimeRateLga.lga_name,
            func.avg(CrimeRateLga.adjusted_rate).label("adjusted_rate"),
        )
        .where(
            CrimeRateLga.year == latest_year,
            CrimeRateLga.offence == "dwelling",
            CrimeRateLga.measure == "OFFENCE_RATE_POOLED_NORMALISED",
            CrimeRateLga.frequency == "ANNUAL",
            CrimeRateLga.adjusted_rate.isnot(None),
        )
        .group_by(CrimeRateLga.lga_name)
    )
    rows = (await db.execute(q)).all()
    return [
        CrimeStatItem(lga_name=row.lga_name, adjusted_rate=float(row.adjusted_rate))
        for row in rows
    ]


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
