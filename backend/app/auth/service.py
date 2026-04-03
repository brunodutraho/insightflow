from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid
from typing import Optional

from app.models.user import User, UserRole, UserStatus
from app.models.client import Tenant
from app.models.audit_log import AuditLog

# Importamos as funções do seu token_service atualizado
from app.auth.token_service import create_access_token
from app.auth.utils import verify_password, hash_password


# --- AUTHENTICATION ---

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    # Busca o usuário por email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    # Verifica a senha (hash)
    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str) -> Optional[str]:
    user = authenticate_user(db, email, password)

    if not user:
        return None

    # Validações de Status e Verificação
    if not user.email_verified:
        raise Exception("Email não verificado. Verifique sua caixa de entrada.")

    if user.status not in [UserStatus.active, UserStatus.pending_invite]:
        raise Exception("Esta conta está bloqueada ou inativa.")

    # Atualiza último login
    user.last_login = datetime.now(timezone.utc)
    
    # Gera o token usando a função atualizada que recebe o objeto User
    token = create_access_token(user)

    # Registro de Auditoria
    audit = AuditLog(
        user_id=user.id,
        action="user_login",
        details=f"Login realizado com sucesso: {user.email}"
    )
    db.add(audit)
    db.commit()

    return token


# --- REGISTRATION (Auto-cadastro / Assinante) ---

def register_user(db: Session, data):
    # Verifica se já existe
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        return None

    # 1. Cria o Tenant (Empresa) primeiro
    tenant = Tenant(
        name=data.company_name or f"Empresa de {data.full_name}",
        owner_id=None 
    )
    db.add(tenant)
    db.flush()  

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

    # 3. Vincula o Usuário como dono oficial do Tenant
    tenant.owner_id = new_user.id

    db.commit()
    db.refresh(new_user)
    db.refresh(tenant)

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
        email_verified=False,
        status=UserStatus.pending_invite
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
