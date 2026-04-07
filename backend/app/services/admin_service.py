from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.client import Tenant
from app.models.subscription import Subscription


def get_admin_overview(db: Session):
    # =========================
    # USERS
    # =========================
    total_users = db.query(func.count(User.id)).scalar()

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    new_users = (
        db.query(func.count(User.id))
        .filter(User.created_at >= thirty_days_ago)
        .scalar()
    )

    # =========================
    # COMPANIES
    # =========================
    total_companies = db.query(func.count(Tenant.id)).scalar()

    # =========================
    # SUBSCRIPTIONS
    # =========================
    active_subs = (
        db.query(Subscription)
        .filter(Subscription.is_active == True)
        .all()
    )

    active_count = len(active_subs)

    # =========================
    # MRR (REAL)
    # =========================
    mrr = 0

    for sub in active_subs:
        if sub.plan_rel:
            price = sub.plan_rel.price if sub.plan_rel else 0

            if sub.discount_percent:
                price = price * (1 - sub.discount_percent / 100)

            if sub.discount_amount:
                price = max(0, price - sub.discount_amount)

            mrr += price

    # =========================
    # RESPONSE
    # =========================
    return {
        "users": {
            "total": total_users or 0,
            "new_last_30_days": new_users or 0,
        },
        "companies": {
            "total": total_companies or 0,
        },
        "revenue": {
            "active_subscriptions": active_count,
            "mrr": mrr,
        },
    }