from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.coupon import Coupon
from app.models.subscription import SubscriptionStatus


# CRIAR / TROCAR PLANO (CORE DO SAAS)
def subscribe_to_plan(db, tenant_id, user_id, plan_id):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        return {"error": "Plan not found"}

    # desativa atual
    db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.is_active == True
    ).update({
        "is_active": False,
        "status": SubscriptionStatus.canceled,
        "canceled_at": datetime.utcnow()
    })

    # cria nova
    new_subscription = Subscription(
        tenant_id=tenant_id,
        user_id=user_id,
        plan_id=plan.id,
        status=SubscriptionStatus.active,
        is_active=True,
        started_at=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30),
        discount_percent=0,
        discount_amount=0
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


# APLICAR CUPOM
def apply_coupon(db: Session, subscription_id: int, code: str):
    sub = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not sub:
        return {"error": "Subscription not found"}

    coupon = db.query(Coupon).filter(
        Coupon.code == code
    ).first()

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


# CANCELAR SUBSCRIPTION
def cancel_subscription(db: Session, subscription: Subscription):
    subscription.is_active = False
    subscription.canceled_at = datetime.utcnow()

    db.commit()
    db.refresh(subscription)

    return subscription


# PEGAR SUBSCRIPTION ATIVA DO TENANT
def get_active_subscription(db: Session, tenant_id):
    return db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.is_active == True
    ).first()