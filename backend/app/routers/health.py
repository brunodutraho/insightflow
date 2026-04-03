from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.models.client import Tenant
from app.auth.utils import hash_password

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "InsightFlow",
        "version": "1.0.0"
    }


class BootstrapAdminRequest(BaseModel):
    email: str
    password: str
    tenant_name: str = "InsightFlow Tenant"


@router.post("/bootstrap-admin")
def bootstrap_admin(
    data: BootstrapAdminRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.role == UserRole.admin_master).first()
    if existing:
        raise HTTPException(status_code=409, detail="Admin user already exists.")

    tenant = Tenant(name=data.tenant_name, owner_id=None)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    admin = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.admin_master,
        tenant_id=tenant.id,
        email_verified=True,
        status=UserStatus.active,
        terms_accepted=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    tenant.owner_id = admin.id
    db.commit()

    return {
        "message": "Admin bootstrap created",
        "admin_id": str(admin.id),
        "tenant_id": str(tenant.id)
    }