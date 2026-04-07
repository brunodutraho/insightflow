from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.services.subscription_service import (
    apply_coupon,
    subscribe_to_plan,
    cancel_subscription,
    get_active_subscription
)
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# PEGAR MINHA SUBSCRIPTION (POR TENANT)
@router.get("/me")
def get_my_subscription(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    sub = get_active_subscription(db, user.tenant_id)

    return {
        "has_subscription": bool(sub),
        "subscription": sub
    }


# UPGRADE / TROCA DE PLANO
@router.post("/subscribe")
def subscribe(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    plan_id = data.get("plan_id")

    if not plan_id:
        raise HTTPException(status_code=400, detail="plan_id is required")

    result = subscribe_to_plan(
        db=db,
        tenant_id=user.tenant_id,
        user_id=user.id,
        plan_id=plan_id
    )

    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "message": "Plan updated successfully",
        "subscription_id": str(result.id),
        "plan_id": str(result.plan_id)
    }


# APLICAR CUPOM
@router.post("/{subscription_id}/apply-coupon")
def apply_coupon_route(
    subscription_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sub = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.tenant_id == user.tenant_id
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    result = apply_coupon(db, subscription_id, data.get("code"))

    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# CANCELAR SUBSCRIPTION
@router.post("/cancel")
def cancel_my_subscription(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sub = get_active_subscription(db, user.tenant_id)

    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription")

    canceled = cancel_subscription(db, sub)

    return {
        "message": "Subscription canceled",
        "subscription_id": str(canceled.id)
    }

@router.post("/select-plan")
def select_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    subscription = subscribe_to_plan(
        db=db,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        plan_id=plan_id
    )

    return {
        "message": "Plano ativado",
        "plan_id": str(subscription.plan_id)
    }

@router.post("/upgrade")
def upgrade_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(404, "Plano não encontrado")

    subscription = subscribe_to_plan(
        db=db,
        tenant_id=user.tenant_id,
        user_id=user.id,
        plan_id=plan_id
    )

    return {
        "message": "Plano atualizado com sucesso",
        "plan": plan.name
    }