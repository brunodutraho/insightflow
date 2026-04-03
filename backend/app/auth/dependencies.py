from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import uuid

from app.config.settings import settings
from app.database.database import get_db
from app.models.user import User, UserRole
from app.models.client import Tenant

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# GET CURRENT USER
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ROLE CHECK (rápido e simples)
def require_roles(allowed_roles: list[UserRole]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permissão insuficiente")
        return user

    return role_checker


# PERMISSION CHECK (ESCALÁVEL)
def require_permissions(required_permissions: list[str]):
    def permission_checker(user: User = Depends(get_current_user)):

        # ADMIN MASTER BYPASS
        if user.role == UserRole.admin_master:
            return user

        user_permissions = {perm.name for perm in user.permissions}

        for perm in required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=403,
                    detail=f"Permissão '{perm}' necessária"
                )

        return user

    return permission_checker


# HIERARQUIA MULTI-TENANT
def validate_hierarchy_access(client_id, user: User, db: Session):

    client = db.query(Tenant).filter(Tenant.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # ROOT
    if user.role == UserRole.admin_master:
        return client

    # GERENTE
    if user.role == UserRole.gerente:
        if client.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Cliente não pertence a você")
        return client

    # CLIENTES
    if user.role in UserRole.client_roles():
        if user.tenant_id != client_id:
            raise HTTPException(status_code=403, detail="Acesso restrito")
        return client

    raise HTTPException(status_code=403, detail="Acesso negado")