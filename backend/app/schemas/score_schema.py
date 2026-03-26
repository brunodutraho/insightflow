from pydantic import BaseModel


class PerformanceScoreResponse(BaseModel):
    score: int
    level: str
    details: dict
    insights: list[str]