from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.database.database import get_db
from app.models.ad_metric import AdMetric
from app.models.client import Tenant
from app.schemas.kpi_schema import KPIResponse, KPIInsightResponse
from app.auth.dependencies import get_current_user
from app.services.insight_service import generate_insights

router = APIRouter(prefix="/kpis", tags=["KPIs"])


# ==============================
# 🔐 MULTI-TENANT SECURITY
# ==============================
def validate_client_access(db: Session, client_id: int, user):
    client = db.query(Tenant).filter(Tenant.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return client


# ==============================
# 📊 SUMMARY CALCULATION
# ==============================
def calculate_summary(row):
    if not row:
        return {
            "impressions": 0,
            "clicks": 0,
            "spend": 0,
            "ctr": 0,
            "cpc": 0,
            "cpm": 0,
        }

    impressions = row.impressions or 0
    clicks = row.clicks or 0
    spend = float(row.spend or 0)

    ctr = (clicks / impressions) if impressions > 0 else 0
    cpc = (spend / clicks) if clicks > 0 else 0
    cpm = (spend / impressions * 1000) if impressions > 0 else 0

    return {
        "impressions": impressions,
        "clicks": clicks,
        "spend": round(spend, 2),
        "ctr": round(ctr, 4),
        "cpc": round(cpc, 2),
        "cpm": round(cpm, 2),
    }


# ==============================
# 🧠 INSIGHTS ENGINE
# ==============================
def generate_insights(change: dict) -> list[str]:
    insights = []

    # CTR
    if change["ctr"] > 5:
        insights.append("CTR increased significantly → campaigns are more efficient")
    elif change["ctr"] < -5:
        insights.append("CTR decreased → ads may be less engaging")

    # CPC
    if change["cpc"] > 5:
        insights.append("CPC increased → you are paying more per click")
    elif change["cpc"] < -5:
        insights.append("CPC decreased → cost efficiency improved")

    # Spend
    if change["spend"] > 10:
        insights.append("Spend increased significantly → monitor ROI")
    elif change["spend"] < -10:
        insights.append("Spend decreased → campaigns may be scaling down")

    # Clicks
    if change["clicks"] > 10:
        insights.append("Clicks increased → traffic is growing")
    elif change["clicks"] < -10:
        insights.append("Clicks dropped → possible performance issue")

    # fallback
    if not insights:
        insights.append("No significant changes detected")

    return insights


# ==============================
# 📊 KPIs COM FILTRO
# ==============================
@router.get("/", response_model=KPIResponse)
def get_kpis(
    client_id: str = Query(...),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_client_access(db, client_id, current_user)

    query = db.query(AdMetric).filter(
        AdMetric.tenant_id == client_id
    )

    if start_date:
        query = query.filter(AdMetric.date >= start_date)

    if end_date:
        query = query.filter(AdMetric.date <= end_date)

    stats = (
        query.with_entities(
            AdMetric.date,
            func.sum(AdMetric.impressions).label("impressions"),
            func.sum(AdMetric.clicks).label("clicks"),
            func.sum(AdMetric.spend).label("spend"),
        )
        .group_by(AdMetric.date)
        .order_by(AdMetric.date)
        .all()
    )

    data = []

    total_impressions = 0
    total_clicks = 0
    total_spend = 0.0

    for s in stats:
        impressions = s.impressions or 0
        clicks = s.clicks or 0
        spend = float(s.spend or 0)

        total_impressions += impressions
        total_clicks += clicks
        total_spend += spend

        ctr = (clicks / impressions) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0
        cpm = (spend / impressions * 1000) if impressions > 0 else 0

        data.append({
            "date": s.date,
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "ctr": round(ctr, 4),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
        })

    summary = calculate_summary(type("Row", (), {
        "impressions": total_impressions,
        "clicks": total_clicks,
        "spend": total_spend
    })())

    return {
        "summary": summary,
        "data": data
    }


# ==============================
# 🔥 COMPARAÇÃO + INSIGHTS
# ==============================
@router.get("/compare", response_model=KPIInsightResponse)
def compare_kpis(
    client_id: str = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_client_access(db, client_id, current_user)

    delta = end_date - start_date

    prev_start = start_date - delta - timedelta(days=1)
    prev_end = start_date - timedelta(days=1)

    def get_stats(start, end):
        return (
            db.query(
                func.sum(AdMetric.impressions).label("impressions"),
                func.sum(AdMetric.clicks).label("clicks"),
                func.sum(AdMetric.spend).label("spend"),
            )
            .filter(
                AdMetric.tenant_id == client_id,
                AdMetric.date >= start,
                AdMetric.date <= end
            )
            .first()
        )

    current_row = get_stats(start_date, end_date)
    previous_row = get_stats(prev_start, prev_end)

    current = calculate_summary(current_row)
    previous = calculate_summary(previous_row)

    def calc_change(curr, prev):
        result = {}

        for key in curr.keys():
            prev_value = prev[key]
            curr_value = curr[key]

            if prev_value == 0:
                result[key] = 0
            else:
                result[key] = round(((curr_value - prev_value) / prev_value) * 100, 2)

        return result

    change = calc_change(current, previous)

    insights = generate_insights(change)
    insights = generate_insights(current, previous)

    return {
        "current": current,
        "previous": previous,
        "change": change,
        "insights": insights
    }