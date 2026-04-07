from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import RedirectResponse
from app.auth.oauth import oauth
from app.config.settings import settings
from app.models.client import Tenant
from app.auth.token_service import create_access_token
import uuid
from app.database.database import get_db
from app.models.user import User, UserRole, AuthProvider, UserStatus
from app.auth.dependencies import require_roles, get_current_user
from pydantic import BaseModel
from app.services.email_service import send_verification_email_safe
from datetime import datetime, timedelta, timezone
from app.models.subscription import Subscription, SubscriptionStatus

from .schemas import (
    TokenResponse,
    RegisterRequest,
    UserResponse,
    ClientUserCreate,
    RegisterResponse
)

from .service import (
    login_user,
    register_user,
    create_managed_user
)

from app.auth.token_service import (
    create_email_verification_token,
    verify_email_token,
    create_password_reset_token,
    reset_password_with_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])


class VerifyEmailRequest(BaseModel):
    token: str | None = None
    code: str | None = None


# =========================
# GOOGLE LOGIN
# =========================
@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = f"{settings.BACKEND_URL}/auth/callback/google"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback/google")
async def google_callback(request: Request, db: Session = Depends(get_db)):

    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    if not user_info:
        try:
            user_info = await oauth.google.parse_id_token(request, token)
        except Exception:
            raise HTTPException(status_code=400, detail="Erro ao obter dados do Google")

    if not user_info:
        raise HTTPException(status_code=400, detail="Erro ao autenticar com Google")

    google_id = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Email não retornado pelo Google")

    user = db.query(User).filter(User.email == email).first()

    if user:
        if not user.provider_id:
            user.provider = AuthProvider.google
            user.provider_id = google_id
            user.email_verified = True
            db.commit()
            db.refresh(user)

    else:
        tenant = Tenant(
            id=uuid.uuid4(),
            name=f"{name}'s Workspace"
        )
        db.add(tenant)
        db.flush()

        user = User(
            email=email,
            full_name=name,
            provider=AuthProvider.google,
            provider_id=google_id,
            email_verified=True,
            status=UserStatus.active,
            tenant_id=tenant.id
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(user)

    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/oauth-success?token={access_token}"
    )


# =========================
# LOGIN
# =========================
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=TokenResponse)
async def login_route(
    request: Request,
    db: Session = Depends(get_db),
):
    email = None
    password = None

    content_type = request.headers.get("content-type", "")

    # 📌 Caso 1: JSON (axios padrão)
    if "application/json" in content_type:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")

    # 📌 Caso 2: Form (OAuth2 padrão)
    elif "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

    # ❌ Erro se não vier nada
    if not email or not password:
        raise HTTPException(
            status_code=422,
            detail="Credenciais obrigatórias: email e password"
        )

    token = login_user(db, email, password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# =========================
# VERIFY TOKEN
# =========================
@router.get("/verify-token")
def verify_token_endpoint(
    current_user: User = Depends(get_current_user)
):
    """Endpoint to verify if token is valid and return user info"""
    return {
        "valid": True,
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role.value,
            "status": current_user.status.value,
            "email_verified": current_user.email_verified,
            "tenant_id": str(current_user.tenant_id) if current_user.tenant_id else None
        }
    }


# =========================
# LOGOUT (client-side token removal)
# =========================
@router.post("/logout")
def logout():
    """Client-side logout - just return success"""
    return {"message": "Logout realizado com sucesso"}


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado e já verificado."
        )

    user.provider = AuthProvider.local
    user.status = UserStatus.pending_invite
    user.email_verified = False

    db.commit()
    db.refresh(user)

    verification = create_email_verification_token(db, user)

    verify_link = f"{settings.FRONTEND_URL}/verify?token={verification['token']}"

    send_verification_email_safe(
        to_email=user.email,
        code=verification["code"],
        verify_link=verify_link
    )

    return {
        "message": "Verifique seu email para ativar sua conta"
    }

# =========================
# VERIFY EMAIL
# =========================
@router.post("/verify-email")
def verify_email(data: VerifyEmailRequest, db: Session = Depends(get_db)):

    print(f"DEBUG verify_email: received data.token={repr(data.token)}, data.code={repr(data.code)}")

    user = verify_email_token(
        db,
        token=data.token,
        code=data.code
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Código ou token inválido"
        )

    # ATIVA USUÁRIO
    user.status = UserStatus.active
    user.email_verified = True

    db.commit()

    return {"message": "Email verificado com sucesso"}


# =========================
# RESEND EMAIL
# =========================
class ResendVerificationRequest(BaseModel):
    email: str

class ResendVerificationRequest(BaseModel):
    email: str

@router.post("/resend-verification")
def resend_verification(
    data: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    # Anti enumeration
    if not user:
        return {"message": "Se existir, será enviado"}

    verification = create_email_verification_token(db, user)

    verify_link = f"{settings.FRONTEND_URL}/verify?token={verification['token']}"

    success = send_verification_email_safe(
        to_email=user.email,
        code=verification["code"],
        verify_link=verify_link
    )

    if not success:
        raise HTTPException(500, "Erro ao enviar email")

    return {"message": "Código reenviado"}


# =========================
# FORGOT PASSWORD
# =========================
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if user:
        token = create_password_reset_token(db, user)
        reset_link = f"http://localhost:3000/reset?token={token}"

        print(f"RESET LINK: {reset_link}")

    return {"message": "Se o email existir, você receberá instruções"}


# =========================
# RESET PASSWORD
# =========================
@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):

    success = reset_password_with_token(db, token, new_password)

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Token inválido ou expirado"
        )

    return {"message": "Senha atualizada com sucesso"}


# =========================
# CREATE CLIENT ACCESS
# =========================
@router.post("/create-client-access", response_model=UserResponse)
def create_client_access(
    data: ClientUserCreate,
    db: Session = Depends(get_db),
    current_manager: User = Depends(require_roles([
        UserRole.admin_master,
        UserRole.gerente,
        UserRole.gestor_interno,
        UserRole.gestor_assinante
    ]))
):
    from app.models.client import Tenant

    client = db.query(Tenant).filter(
        Tenant.id == data.client_id
    ).first()

    is_staff = current_manager.role in [
        UserRole.admin_master,
        UserRole.gerente
    ]

    if not is_staff and (not client or client.owner_id != current_manager.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para gerenciar este cliente."
        )

    new_user = create_managed_user(
        db=db,
        email=data.email,
        password=data.password,
        role=UserRole.cliente_final,
        manager_id=current_manager.id,
        client_id=data.client_id
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar usuário ou e-mail já existe"
        )

    return new_user