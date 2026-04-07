from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database.database import get_db
from app.models.social_metric import SocialMetric
from app.models.client import Tenant
from app.schemas.social_schema import SocialResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/social", tags=["Social Media"])


def validate_client_access(db, client_id, user):
    client = db.query(Tenant).filter(Tenant.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")


@router.get("/", response_model=SocialResponse)
def get_social_metrics(
    client_id: str = Query(...),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_client_access(db, client_id, current_user)

    query = db.query(SocialMetric).filter(
        SocialMetric.tenant_id == client_id
    )

    if start_date:
        query = query.filter(SocialMetric.date >= start_date)

    if end_date:
        query = query.filter(SocialMetric.date <= end_date)

    stats = query.order_by(SocialMetric.date).all()

    if not stats:
        return {
            "summary": {
                "total_followers": 0,
                "avg_engagement": 0,
                "total_posts": 0,
                "growth_rate": 0
            },
            "data": []
        }

    data = []
    total_engagement = 0
    total_posts = 0

    first_followers = stats[0].followers
    last_followers = stats[-1].followers

    for s in stats:
        total_engagement += s.engagement
        total_posts += s.posts

        data.append({
            "date": s.date,
            "followers": s.followers,
            "engagement": s.engagement,
            "posts": s.posts
        })

    avg_engagement = total_engagement / len(stats)

    growth_rate = 0
    if first_followers > 0:
        growth_rate = ((last_followers - first_followers) / first_followers) * 100

    summary = {
        "total_followers": last_followers,
        "avg_engagement": round(avg_engagement, 2),
        "total_posts": total_posts,
        "growth_rate": round(growth_rate, 2)
    }

    return {
        "summary": summary,
        "data": data
    }