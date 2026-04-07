import uuid
from datetime import datetime, timedelta, timezone
from typing import Type, Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import random

from app.config.settings import settings
from app.models.user import User, UserRole, UserStatus
from app.models.email_verification_token import EmailVerificationToken
from app.models.password_reset_token import PasswordResetToken
from app.auth.utils import hash_password
import secrets

# --- CONFIGURAÇÕES DE TOKEN ---

def generate_unique_token() -> str:
    return str(uuid.uuid4())

# CRIA ACCESS TOKEN (JWT para Login)
def create_access_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "role": user.role.value, # Pega a string do Enum
        "tenant_id": str(user.tenant_id),
        "email": user.email,
        "exp": now + timedelta(hours=24),
        "iat": now,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

# DECODE E VERIFICAÇÃO DE JWT
def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Validate required fields
        if not payload.get("sub"):
            return None

        return payload
    except JWTError:
        return None
    except Exception:
        return None

def verify_token(token: str) -> dict:
    payload = decode_token(token)
    if payload is None:
        raise ValueError("Token inválido ou expirado")

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    email = payload.get("email")
    role = payload.get("role")

    if not user_id or not email:
        raise ValueError("Payload do token inválido - campos obrigatórios ausentes")

    # Validate UUID format
    try:
        user_uuid = uuid.UUID(user_id)
        tenant_uuid = uuid.UUID(tenant_id) if tenant_id else None
    except ValueError:
        raise ValueError("IDs no token têm formato inválido")

    return {
        "user_id": user_uuid,
        "role": role,
        "tenant_id": tenant_uuid,
        "email": email,
    }

# --- TOKENS DE BANCO DE DADOS (E-mail e Senha) ---


def create_password_reset_token(db: Session, user: User) -> str:
    token = generate_unique_token()
    db_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30)
    )
    db.add(db_token)
    db.commit()
    return token

def verify_and_get_token(db: Session, token_str: str, model_class: Type) -> Optional[object]:
    now = datetime.now(timezone.utc) 
    return db.query(model_class).filter(
        model_class.token == token_str,
        model_class.used_at.is_(None),
        model_class.expires_at > now
    ).first()

def mark_token_as_used(db: Session, token_record: object):
    token_record.used_at = datetime.now(timezone.utc)
    db.commit()

# --- FLUXOS DE NEGÓCIO ---

# =========================
# CREATE TOKEN + CODE
# =========================
def create_email_verification_token(db: Session, user):
    # INVALIDA TOKENS ANTIGOS
    db.query(EmailVerificationToken).filter(
        EmailVerificationToken.user_id == user.id,
        EmailVerificationToken.used_at.is_(None)  # ✅ CORRETO
    ).update({"used_at": datetime.utcnow()})

    token = secrets.token_urlsafe(32)
    code = str(secrets.randbelow(1000000)).zfill(6)

    expires_at = datetime.utcnow() + timedelta(minutes=15)

    verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        code=code,
        expires_at=expires_at,
        used_at=None
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return {
        "token": token,
        "code": code
    }

# =========================
# VERIFY TOKEN OU CODE
# =========================
def verify_email_token(
    db: Session,
    token: str = None,
    code: str = None
):
    now = datetime.now(timezone.utc)

    print("DEBUG TOKEN:", repr(token))
    print("DEBUG CODE:", repr(code))

    # Clean the code if provided
    if code:
        code = code.strip()
        print("DEBUG CODE after strip:", repr(code))

    query = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.used_at.is_(None),
        EmailVerificationToken.expires_at > now
    )

    # Priorizamos a busca pelo código de 6 dígitos (CODE)
    if code:
        query = query.filter(EmailVerificationToken.code == code)
        print(f"DEBUG: Searching by code: {repr(code)}")

        # Log extra para debug caso não encontre
        all_codes = db.query(EmailVerificationToken).filter(
            EmailVerificationToken.used_at.is_(None),
            EmailVerificationToken.expires_at > now
        ).all()
        print(f"DEBUG: All unused codes currently in DB: {[c.code for c in all_codes]}")

    # Se não houver code, tentamos pelo TOKEN (o link longo)
    elif token:
        query = query.filter(EmailVerificationToken.token == token)
        print(f"DEBUG: Searching by token: {repr(token)}")

    else:
        print("DEBUG: No token or code provided")
        return None


    token_record = query.first()

    print("DEBUG FOUND:", token_record)
    if token_record:
        print(f"DEBUG: Found token for user {token_record.user_id}, code: {repr(token_record.code)}, expires: {token_record.expires_at}")

    if not token_record:
        print("DEBUG: No valid token found")
        return None

    user = db.query(User).filter(User.id == token_record.user_id).first()

    if not user:
        print("DEBUG: User not found")
        return None

    print(f"DEBUG: Verifying email for user {user.email}")

    user.email_verified = True
    user.status = UserStatus.active

    token_record.used_at = now

    db.commit()

    print("DEBUG: Email verified successfully")

    return user

def reset_password_with_token(db: Session, token_str: str, new_password: str) -> bool:
    token_record = verify_and_get_token(db, token_str, PasswordResetToken)
    if not token_record:
        return False

    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        return False

    user.hashed_password = hash_password(new_password)
    mark_token_as_used(db, token_record)
    return True

def delete_expired_tokens(db: Session, model_class: Type) -> int:
    now = datetime.now(timezone.utc)
    deleted = db.query(model_class).filter(model_class.expires_at < now).delete()
    db.commit()
    return deleted
