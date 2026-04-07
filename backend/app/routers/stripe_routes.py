from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.services.stripe_service import create_checkout_session

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/checkout")
def create_checkout(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = create_checkout_session(
        db,
        user,
        plan_id=data.get("plan_id"),
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel"
    )

    return result