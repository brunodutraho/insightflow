from pydantic import BaseModel
from datetime import date


class KPIDataPoint(BaseModel):
    date: date
    impressions: int
    clicks: int
    spend: float
    ctr: float
    cpc: float
    cpm: float


class KPISummary(BaseModel):
    impressions: int
    clicks: int
    spend: float
    ctr: float
    cpc: float
    cpm: float


class KPIResponse(BaseModel):
    summary: KPISummary
    data: list[KPIDataPoint]


class KPIComparison(BaseModel):
    current: KPISummary
    previous: KPISummary
    change: dict

class KPIInsightResponse(BaseModel):
    current: KPISummary
    previous: KPISummary
    change: dict
    insights: list[str]