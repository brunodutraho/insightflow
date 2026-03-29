from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.client import Client

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista os clientes conforme a permissão:
    - Admin: Todos os clientes da plataforma.
    - Gestor: Apenas os clientes que ele criou (owner_id).
    - Cliente: Retorna apenas a si mesmo (ou lista vazia).
    """
    user_role = current_user.role.value if hasattr(current_user.role, "value") else current_user.role

    if user_role == "admin":
        return db.query(Client).all()
    
    if user_role == "gestor":
        return db.query(Client).filter(Client.owner_id == current_user.id).all()
    
    if user_role == "cliente":
        return db.query(Client).filter(Client.id == current_user.client_id).all()

    return []

@router.post("/")
def create_client(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "gestor"]))
):
    new_client = Client(name=name, owner_id=current_user.id)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
