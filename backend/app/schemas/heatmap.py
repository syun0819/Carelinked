from typing import List, Optional

from pydantic import BaseModel


class LgaStatItem(BaseModel):
    lga_name: str
    lga_code: str
    supply: int
    demand: int
    ratio: Optional[float]


class LgaStatsResponse(BaseModel):
    results: List[LgaStatItem]


class BushfireHeatPoint(BaseModel):
    lat: float
    lon: float
    intensity: float  # 0–1, normalized


class BushfireHeatResponse(BaseModel):
    results: List[BushfireHeatPoint]


class CrimeStatItem(BaseModel):
    lga_name: str
    adjusted_rate: float


class CrimeStatsResponse(BaseModel):
    results: List[CrimeStatItem]
