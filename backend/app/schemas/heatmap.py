from typing import List, Optional

from pydantic import BaseModel, Field


class LgaStatItem(BaseModel):
    lga_name: str
    lga_code: str
    supply: int
    demand: int
    ratio: Optional[float]


class LgaStatsResponse(BaseModel):
    results: List[LgaStatItem]


class BushfireLgaItem(BaseModel):
    lga_name: str
    lga_code: str
    bushfire_count: int


class BushfireLgaResponse(BaseModel):
    results: List[BushfireLgaItem]


class CrimeStatItem(BaseModel):
    lga_name: str
    adjusted_rate: float


class CrimeStatsResponse(BaseModel):
    results: List[CrimeStatItem]
    year: Optional[int] = None
    available_years: List[int] = Field(default_factory=list)
