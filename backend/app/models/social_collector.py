from app.models.social_metric import SocialMetric
from datetime import date


def collect_social_metrics(db, client_id):
    metric = SocialMetric(
        client_id=client_id,
        date=date.today(),
        followers=12500,
        following=350,
        posts=210,
        likes=520,
        comments=45,
        shares=12,
        engagement_rate=4.2
    )

    db.add(metric)
    db.commit()