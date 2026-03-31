from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.models.coupon import Coupon
from datetime import datetime


def apply_coupon(db: Session, subscription_id: int, code: str):
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()

    if not sub:
        return {"error": "Subscription not found"}

    coupon = db.query(Coupon).filter(Coupon.code == code).first()

    if not coupon or not coupon.is_active:
        return {"error": "Invalid coupon"}

    if coupon.max_uses and coupon.used_count >= coupon.max_uses:
        return {"error": "Coupon expired"}

    # aplicar desconto
    sub.discount_percent = coupon.discount_percent
    sub.discount_amount = coupon.discount_amount

    coupon.used_count += 1

    db.commit()
    db.refresh(sub)

    return sub


def cancel_subscription(db: Session, subscription: Subscription):
    subscription.is_active = False
    subscription.canceled_at = datetime.utcnow()

    db.commit()
    db.refresh(subscription)

    return subscription