from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database.database import get_db
from app.models.insight import Insight
from app.auth.dependencies import require_roles
from app.schemas.analytics_schema import (
    InsightCategoryMetric,
    InsightTimeMetric,
    InsightUserMetric
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# 📊 Insights por categoria (com filtro de período)
@router.get("/insights-by-category", response_model=list[InsightCategoryMetric])
def get_insights_metrics(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin", "gestor"]))
):
    query = db.query(
        Insight.category,
        func.count(Insight.id).label("total")
    )

    if start_date:
        query = query.filter(Insight.created_at >= start_date)

    if end_date:
        query = query.filter(Insight.created_at <= end_date)

    stats = (
        query
        .group_by(Insight.category)
        .order_by(func.count(Insight.id).desc())
        .all()
    )

    return [
        {
            "category": s.category,
            "total": s.total
        }
        for s in stats
    ]


# 📈 Insights ao longo do tempo
@router.get("/insights-over-time", response_model=list[InsightTimeMetric])
def insights_over_time(
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin", "gestor"]))
):
    date_field = func.date(Insight.created_at)

    stats = (
        db.query(
            date_field.label("date"),
            func.count(Insight.id).label("total")
        )
        .group_by(date_field)
        .order_by(date_field)
        .all()
    )

    return [
        {
            "date": s.date,
            "total": s.total
        }
        for s in stats
    ]


# 🧑‍💼 Insights por usuário (ranking)
@router.get("/insights-by-user", response_model=list[InsightUserMetric])
def insights_by_user(
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin"]))
):
    stats = (
        db.query(
            Insight.user_id,
            func.count(Insight.id).label("total")
        )
        .group_by(Insight.user_id)
        .order_by(func.count(Insight.id).desc())
        .all()
    )

    return [
        {
            "user_id": s.user_id,
            "total": s.total
        }
        for s in stats
    ]