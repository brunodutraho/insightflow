from pydantic import BaseModel
from datetime import date


class SocialMetricResponse(BaseModel):
    date: date
    followers: int
    engagement: float
    posts: int

    class Config:
        from_attributes = True


class SocialSummary(BaseModel):
    total_followers: int
    avg_engagement: float
    total_posts: int
    growth_rate: float


class SocialResponse(BaseModel):
    summary: SocialSummary
    data: list[SocialMetricResponse]