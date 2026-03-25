from pydantic import BaseModel
from datetime import datetime


class InsightCreate(BaseModel):
    content: str
    category: str | None = "general"


class InsightResponse(BaseModel):
    id: int
    content: str
    category: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True