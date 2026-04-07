from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.subscription import Subscription
from app.models.user import User
from app.services.subscription_service import get_active_subscription

def get_current_plan(db, tenant_id):
    sub = db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.is_active == True
    ).first()

    if not sub:
        return None

    return sub.plan


def check_client_limit(db: Session, tenant_id):
    subscription = get_active_subscription(db, tenant_id)

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Nenhum plano ativo"
        )

    plan = subscription.plan

    # conta apenas subusuários (clientes criados)
    total_clients = db.query(User).filter(
        User.tenant_id == tenant_id,
        User.parent_id != None
    ).count()

    if total_clients >= plan.max_clients:
        raise HTTPException(
            status_code=403,
            detail="Limite de clientes atingido para o seu plano"
        )

    return True