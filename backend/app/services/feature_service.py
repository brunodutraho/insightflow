from sqlalchemy.orm import Session
from app.models.subscription import Subscription


def check_feature_access(user_id: int, db: Session, feature: str) -> bool:
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .first()
    )

    if not subscription or not subscription.is_active:
        return False

    plan = subscription.plan

    # 🔥 Regras simples (evolui depois)
    feature_rules = {
        "free": [],
        "pro": ["score"],
        "premium": ["score", "advanced_insights"]
    }

    allowed_features = feature_rules.get(plan, [])

    return feature in allowed_features