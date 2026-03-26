from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database.database import get_db
from app.models.ad_metric import AdMetric
from app.models.client import Client
from app.auth.dependencies import get_current_user
from app.services.score_service import calculate_score
from app.schemas.score_schema import PerformanceScoreResponse

router = APIRouter(prefix="/score", tags=["Performance Score"])


def validate_client_access(db: Session, client_id: int, user):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return client


@router.get("/", response_model=PerformanceScoreResponse)
def get_score(
    client_id: int = Query(...),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_client_access(db, client_id, current_user)

    query = db.query(
        func.sum(AdMetric.impressions).label("impressions"),
        func.sum(AdMetric.clicks).label("clicks"),
        func.sum(AdMetric.spend).label("spend"),
    ).filter(AdMetric.client_id == client_id)

    if start_date:
        query = query.filter(AdMetric.date >= start_date)

    if end_date:
        query = query.filter(AdMetric.date <= end_date)

    row = query.first()

    if not row:
        raise HTTPException(status_code=404, detail="No data found")

    impressions = row.impressions or 0
    clicks = row.clicks or 0
    spend = float(row.spend or 0)

    ctr = (clicks / impressions) if impressions > 0 else 0
    cpc = (spend / clicks) if clicks > 0 else 0
    cpm = (spend / impressions * 1000) if impressions > 0 else 0

    kpi = {
        "ctr": ctr,
        "cpc": cpc,
        "cpm": cpm
    }

    return calculate_score(kpi)