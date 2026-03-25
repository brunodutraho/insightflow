from pydantic import BaseModel
from datetime import date


class InsightCategoryMetric(BaseModel):
    category: str
    total: int


class InsightTimeMetric(BaseModel):
    date: date
    total: int


class InsightUserMetric(BaseModel):
    user_id: int
    total: int