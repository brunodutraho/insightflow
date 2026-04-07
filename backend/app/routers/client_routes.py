from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database.database import get_db
from app.auth.dependencies import get_current_user, require_roles, require_access
from app.models.user import User, UserRole
from app.models.client import Tenant
from app.services.limit_service import check_client_limit

router = APIRouter(prefix="/clients", tags=["Clients"])

# --- LISTAGEM DE CLIENTES (TENANTS) ---
@router.get("/")
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role in [UserRole.admin_master, UserRole.gerente]:
        return db.query(Tenant).all()
    
    if current_user.role in [UserRole.suporte, UserRole.marketing]:
        return db.query(Tenant).all()

    
    if current_user.role in [UserRole.gestor_assinante, UserRole.gestor_interno]:
        return db.query(Tenant).filter(Tenant.owner_id == current_user.id).all()
    
    if current_user.role == UserRole.cliente_final:
        return db.query(Tenant).filter(Tenant.id == current_user.tenant_id).all()

    return []

# --- CRIAÇÃO DE NOVO CLIENTE (TENANT) ---
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_client(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_access([
        UserRole.admin_master, 
        UserRole.gerente, 
        UserRole.gestor_assinante,
        UserRole.gestor_interno
    ]))
):
    # BLOQUEIO DO PLANO (MONETIZAÇÃO)
    check_client_limit(db, current_user.tenant_id)

    new_client = Tenant(
        name=name, 
        owner_id=current_user.id
    )

    try:
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )

# --- DETALHES DE UM CLIENTE ESPECÍFICO ---
@router.get("/{client_id}")
def get_client_detail(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Tenant).filter(Tenant.id == client_id).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # VALIDAÇÃO DE SEGURANÇA: O usuário tem permissão para ver ESSE cliente?
    is_staff = current_user.role in [UserRole.admin_master, UserRole.gerente, UserRole.suporte]
    is_owner = client.owner_id == current_user.id
    is_member = client.id == current_user.tenant_id

    if not (is_staff or is_owner or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar os dados deste cliente."
        )

    return client
