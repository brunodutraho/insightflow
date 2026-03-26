from sqlalchemy.orm import Session
from app.models.social_metric import SocialMetric


def get_latest_social_metrics(db: Session, client_id: int):
    social = (
        db.query(SocialMetric)
        .filter(SocialMetric.client_id == client_id)
        .order_by(SocialMetric.date.desc())
        .first()
    )

    if not social:
        return None

    return {
        "followers": social.followers,
        "engagement": social.engagement,
        "posts": social.posts,
        "growth_rate": social.growth_rate
    }