import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database.database import get_db
from app.models.user import User, UserRole
from app.auth.dependencies import require_feature
from app.services.user_service import count_users
from app.services.limit_service import check_user_limit
from app.auth.dependencies import require_access

router = APIRouter(prefix="/users", tags=["Users"])

# 🔐 USER LOGADO (ME)
@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "role": user.role,
        "full_name": user.full_name,
        "tenant_id": str(user.tenant_id)
    }

# 🔐 ROTA DE TESTE ADMIN (Apenas Master e Gerente)
@router.get("/admin-check")
def admin_check_route(user: User = Depends(require_roles([UserRole.admin_master, UserRole.gerente]))):
    return {
        "message": "Acesso administrativo confirmado",
        "admin_id": str(user.id)
    }

# 🔐 DASHBOARD (Acesso para equipe interna e gestores assinantes)
@router.get("/dashboard-access")
def dashboard_check(
    user: User = Depends(require_access([
        UserRole.admin_master, 
        UserRole.gerente, 
        UserRole.gestor_interno, 
        UserRole.gestor_assinante
    ]))
):
    return {
        "message": "Acesso ao dashboard concedido",
        "role": user.role
    }

# 🔍 LISTAR USUÁRIOS (Com filtro de risco)
@router.get("/")
def list_users(
    filter_type: Optional[str] = Query(None, alias="filter"),
    db: Session = Depends(get_db),
    # Apenas quem gere a plataforma vê essa lista global
    admin: User = Depends(require_roles([UserRole.admin_master, UserRole.gerente]))
):
    query = db.query(User)

    if filter_type == "at_risk":
        # Uso de timezone.utc para evitar avisos do Python 3.12
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query = query.filter(
            User.last_login != None,
            User.last_login < seven_days_ago
        )

    users = query.all()

    return [
        {
            "id": str(u.id),
            "email": u.email,
            "role": u.role,
            "status": u.status,
            "created_at": u.created_at,
            "last_login": u.last_login
        }
        for u in users
    ]

# 🛠 ALTERAR ROLE (Cuidado: Agora espera um membro do Enum UserRole)
@router.patch("/{user_id}/role")
def update_user_role(
    user_id: str, # UUID recebido como string
    new_role: UserRole = Body(..., embed=True), # O FastAPI valida se a string enviada existe no Enum
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles([UserRole.admin_master]))
):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    target_user.role = new_role
    db.commit()

    return {"message": f"Cargo atualizado para {new_role}"}

# 🗑 DELETAR USUÁRIO
@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles([UserRole.admin_master]))
):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Evita que o admin se delete por acidente
    if target_user.id == admin.id:
        raise HTTPException(status_code=400, detail="Você não pode deletar sua própria conta")

    db.delete(target_user)
    db.commit()

    return {"message": "Usuário removido com sucesso"}

@router.post("/invite")
def invite_user(
    _ = Depends(require_feature("multi_users")),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return {"message": "Convite enviado"}

@router.post("/")
def create_user(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # conta usuários do tenant
    current_users = count_users(db, current_user.tenant_id)

    # valida limite do plano
    allowed = check_user_limit(
        db,
        current_user.tenant_id,
        current_users
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="User limit reached. Upgrade your plan."
        )

    # cria usuário
    new_user = User(
        email=data.get("email"),
        full_name=data.get("full_name"),
        role=UserRole.gestor_assinante,
        tenant_id=current_user.tenant_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": str(new_user.id)
    }