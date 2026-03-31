from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.subscription import Subscription
from app.services.subscription_service import apply_coupon
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# 🔍 pegar minha subscription
@router.get("/me")
def get_my_subscription(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sub = db.query(Subscription).filter(
        Subscription.user_id == user.id
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return sub


# 💸 aplicar cupom
@router.post("/{subscription_id}/apply-coupon")
def apply_coupon_route(
    subscription_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sub = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user.id
    ).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    result = apply_coupon(db, subscription_id, data.get("code"))

    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return result