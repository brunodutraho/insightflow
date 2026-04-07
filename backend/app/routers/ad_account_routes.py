from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.ad_account import AdAccount
from app.models.client import Tenant
from app.schemas.ad_account import AdAccountCreate, AdAccountResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/ad-accounts", tags=["Ad Accounts"])


@router.post("/", response_model=AdAccountResponse)
def create_ad_account(
    data: AdAccountCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # AJUSTE: Mudamos current_user.id para int(current_user["user_id"])
    user_id = int(current_user["user_id"])

    client = (
        db.query(Tenant)
        .filter(
            Tenant.id == data.client_id,
            Tenant.owner_id == user_id
        )
        .first()
    )

    if not client:
        raise HTTPException(status_code=403, detail="Invalid client or no permission")

    # Criamos o objeto passando os campos do schema
    account = AdAccount(**data.dict())

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.get("/", response_model=list[AdAccountResponse])
def list_ad_accounts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Aqui já estava quase certo, garantimos o uso do dicionário
    user_id = int(current_user["user_id"])
    
    return (
        db.query(AdAccount)
        .join(Tenant)
        .filter(Tenant.owner_id == user_id)
        .all()
    )
