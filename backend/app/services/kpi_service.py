from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ad_metric import AdMetric


def get_kpis_data(db: Session, client_id, start_date=None, end_date=None):
    query = db.query(AdMetric).filter(AdMetric.client_id == client_id)

    if start_date:
        query = query.filter(AdMetric.date >= start_date)

    if end_date:
        query = query.filter(AdMetric.date <= end_date)

    stats = query.all()

    impressions = sum(s.impressions or 0 for s in stats)
    clicks = sum(s.clicks or 0 for s in stats)
    spend = sum(float(s.spend or 0) for s in stats)

    ctr = (clicks / impressions) if impressions else 0
    cpc = (spend / clicks) if clicks else 0
    cpm = (spend / impressions * 1000) if impressions else 0

    return {
        "summary": {
            "impressions": impressions,
            "clicks": clicks,
            "spend": round(spend, 2),
            "ctr": round(ctr, 4),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
        }
    }