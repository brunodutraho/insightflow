from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.models.plan import Plan
from app.services.stripe_service import create_checkout_session

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/checkout-session")
def checkout_session(
    plan_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(404, "Plano não encontrado")

    session = create_checkout_session(user, plan)

    return {
        "checkout_url": session.url
    }