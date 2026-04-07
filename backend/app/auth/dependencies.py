from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import uuid

from app.config.settings import settings
from app.database.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.models.client import Tenant
from fastapi import Depends, HTTPException
from app.services.plan_service import has_feature
from app.services.limit_service import check_user_limit
from app.services.subscription_service import get_active_subscription
from app.models.subscription import SubscriptionStatus
from datetime import datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# GET CURRENT USER
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if not user_id:
            raise credentials_exception

        user_uuid = uuid.UUID(user_id)

    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_uuid).first()

    if not user.email_verified:
        raise HTTPException(403, "Email não verificado.")

    if user.status == UserStatus.blocked:
        raise HTTPException(403, "Conta bloqueada.")

    if user.status != UserStatus.active:
        raise HTTPException(403, "Conta inativa.")

    return user

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

def require_feature(feature_code: str):
    def dependency(
        db: Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
        allowed = has_feature(db, user.tenant_id, feature_code)

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail=f"Seu plano não permite acesso a: {feature_code}"
            )

        return True

    return dependency

def require_user_limit(current_count: int):
    def dependency(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
    ):
        allowed = check_user_limit(db, user.tenant_id, current_count)

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="User limit reached. Upgrade your plan."
            )

    return dependency

# =============================
# SUBSCRIPTION CHECK (SAAS CORE)
# =============================

def require_active_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # BYPASS PARA STAFF INTERNO
    if user.role in [
        UserRole.admin_master,
        UserRole.gerente,
        UserRole.administrativo,
        UserRole.suporte,
        UserRole.marketing,
        UserRole.gestor_interno,
    ]:
        return None

    subscription = get_active_subscription(db, user.tenant_id)

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Nenhum plano ativo. Escolha um plano."
        )

    now = datetime.now(timezone.utc)

    # status cancelado
    if subscription.status == SubscriptionStatus.canceled:
        raise HTTPException(
            status_code=403,
            detail="Sua assinatura foi cancelada."
        )

    # expirado
    if (
        subscription.current_period_end and
        subscription.current_period_end < now
    ):
        raise HTTPException(
            status_code=403,
            detail="Sua assinatura expirou."
        )

    return subscription


# =============================
# ACCESS COMBINADO (ROLE + PLAN)
# =============================

def require_access(roles: list[UserRole]):
    def dependency(
        user: User = Depends(require_roles(roles)),
        subscription = Depends(require_active_subscription)
    ):
        return user
    return dependency