from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.plan import Plan

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/")
def list_plans(db: Session = Depends(get_db)):
    plans = db.query(Plan).all()

    return [
        {
            "id": str(p.id),
            "name": p.name,
            "price": float(p.price),
        }
        for p in plans
    ]