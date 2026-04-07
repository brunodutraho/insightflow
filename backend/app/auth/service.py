from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import uuid
from typing import Optional
from fastapi import HTTPException, status

from app.models.user import User, UserRole, UserStatus, AuthProvider
from app.models.client import Tenant
from app.models.audit_log import AuditLog
from app.models.subscription import Subscription, SubscriptionStatus
from app.services.email_service import send_verification_email_safe
from app.auth.token_service import create_access_token, create_email_verification_token
from app.auth.utils import verify_password, hash_password
from app.config.settings import settings

# --- AUTHENTICATION ---


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    # BLOQUEIA LOGIN SOCIAL
    if user.provider != AuthProvider.local:
        raise HTTPException(
            status_code=400,
            detail="Este usuário utiliza login social (Google)."
        )

    # GARANTE QUE EXISTE SENHA
    if not user.hashed_password:
        return None

    # VERIFICA HASH
    if not verify_password(password, user.hashed_password):
        return None
    print("LOGIN DEBUG:", email, password)
    print("HASH:", user.hashed_password)
    print("VERIFY:", verify_password(password, user.hashed_password))

    return user


def login_user(db: Session, email: str, password: str) -> str:
    # =========================
    # 1. AUTENTICAÇÃO
    # =========================
    user = authenticate_user(db, email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # =========================
    # 2. EMAIL NÃO VERIFICADO
    # =========================
    if not user.email_verified:
        try:
            # Gera novo token/código
            verification = create_email_verification_token(db, user)

            # Link de verificação
            verify_link = f"{settings.FRONTEND_URL}/verify-email?token={verification['token']}"

            # Envia email
            success = send_verification_email_safe(
                to_email=user.email,
                code=verification["code"],
                verify_link=verify_link
            )

            if not success:
                print("⚠️ Falha ao enviar email de verificação")

        except Exception as e:
            print("❌ ERRO AO GERAR/ENVIAR VERIFICAÇÃO:", str(e))

        # 🚫 Bloqueia login até verificar
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "EMAIL_NOT_VERIFIED",
                "email": user.email
            }
        )

    # 3. STATUS DA CONTA
    if user.status == UserStatus.blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta bloqueada."
        )

    if user.status == UserStatus.inactive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta inativa."
        )

    if user.status != UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Conta inválida: {user.status.value}"
        )

    # 4. LOGIN SUCESSO
    try:
        user.last_login = datetime.now(timezone.utc)

        audit = AuditLog(
            user_id=user.id,
            action="user_login",
            details=f"Login realizado: {user.email}"
        )
        db.add(audit)

        token = create_access_token(user)

        db.commit()

        return token

    except Exception as e:
        db.rollback()
        print(f"💥 LOGIN ERROR: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar login."
        )



# --- REGISTRATION (Auto-cadastro / Assinante) ---

def register_user(db: Session, data) -> Optional[User]:
    existing_user = db.query(User).filter(User.email == data.email).first()

    # USUÁRIO JÁ EXISTE
    if existing_user:
        # Se ainda NÃO verificou email → permitir fluxo continuar
        if not existing_user.email_verified:
            return existing_user

        # Já verificado → bloquear
        return None

    # =========================
    # NOVO USUÁRIO
    # =========================

    # 1. Tenant
    tenant = Tenant(
        name=data.company_name or f"Empresa de {data.full_name}",
        owner_id=None
    )
    db.add(tenant)
    db.flush()

    # 2. Usuário
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.gestor_assinante,
        tenant_id=tenant.id,
        full_name=data.full_name,
        phone=data.phone,
        email_verified=False,
        status=UserStatus.pending_invite
    )

    db.add(new_user)
    db.flush()

    tenant.owner_id = new_user.id

    # 3. TRIAL AUTOMÁTICO
    subscription = Subscription(
        user_id=new_user.id,
        tenant_id=tenant.id,
        status=SubscriptionStatus.trialing,
        trial_ends_at=datetime.now(timezone.utc) + timedelta(days=7),
        is_active=True
    )

    db.add(subscription)

    db.commit()
    db.refresh(new_user)

    return new_user




def create_managed_user(
    db: Session,
    email: str,
    password: str,
    role: UserRole,
    manager_id: uuid.UUID,
    client_id: uuid.UUID
) -> Optional[User]:
    
    # Verifica duplicidade
    if db.query(User).filter(User.email == email).first():
        return None

    # Cria usuário vinculado a um tenant existente
    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        manager_id=manager_id,
        tenant_id=client_id,
        status=UserStatus.pending_invite,
        email_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
