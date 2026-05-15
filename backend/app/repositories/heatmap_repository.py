from typing import List

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.heatmap import BushfireLgaSummary, CrimeRateLga, FacilityHeatRisk, LgaBoundary, ResidentialCareDemandByLga

_CRIME_BASE_FILTERS = (
    CrimeRateLga.measure == "OFFENCE_RATE_POOLED_NORMALISED",
    CrimeRateLga.frequency == "ANNUAL",
    CrimeRateLga.adjusted_rate.isnot(None),
)


async def fetch_lga_boundaries(db: AsyncSession):
    q = select(
        LgaBoundary.lga_code,
        LgaBoundary.lga_name,
        LgaBoundary.state_name,
        LgaBoundary.geom_wkt,
    ).where(LgaBoundary.geom_wkt.isnot(None))
    return (await db.execute(q)).all()


async def fetch_demand_by_lga(db: AsyncSession):
    q = (
        select(
            ResidentialCareDemandByLga.lga_name,
            ResidentialCareDemandByLga.lga_code,
            func.sum(ResidentialCareDemandByLga.people_count).label("demand"),
        )
        .where(ResidentialCareDemandByLga.admission_type == "Permanent")
        .group_by(ResidentialCareDemandByLga.lga_name, ResidentialCareDemandByLga.lga_code)
    )
    return (await db.execute(q)).all()


async def fetch_supply_by_lga(db: AsyncSession):
    q = (
        select(
            AgedCareService.lga_name,
            func.sum(AgedCareService.residential_places).label("supply"),
        )
        .where(AgedCareService.lga_name.isnot(None))
        .group_by(AgedCareService.lga_name)
    )
    return (await db.execute(q)).all()


async def fetch_bushfire_by_lga(db: AsyncSession):
    q = select(
        BushfireLgaSummary.lga_name,
        BushfireLgaSummary.lga_code,
        BushfireLgaSummary.bushfire_count,
    ).order_by(BushfireLgaSummary.bushfire_count.desc())
    return (await db.execute(q)).all()


async def fetch_crime_years(db: AsyncSession) -> List[int]:
    q = (
        select(CrimeRateLga.year)
        .where(*_CRIME_BASE_FILTERS)
        .group_by(CrimeRateLga.year)
        .order_by(desc(CrimeRateLga.year))
    )
    return [row.year for row in (await db.execute(q)).all()]


async def fetch_crime_rates(db: AsyncSession, year: int):
    q = (
        select(
            CrimeRateLga.lga_name,
            func.sum(CrimeRateLga.adjusted_rate).label("adjusted_rate"),
        )
        .where(CrimeRateLga.year == year, *_CRIME_BASE_FILTERS)
        .group_by(CrimeRateLga.lga_name)
    )
    return (await db.execute(q)).all()


async def fetch_facility_heat_risk(db: AsyncSession):
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
    return (await db.execute(q)).all()
