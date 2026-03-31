from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/reauth")
def reauthenticate(data: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    password = data.get("password")

    if not password:
        raise HTTPException(status_code=400, detail="Password required")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"success": True}