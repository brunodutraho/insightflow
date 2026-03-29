from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User, UserRole
from app.auth.dependencies import get_current_user, require_roles
from .schemas import (
    TokenResponse,
    RegisterRequest,
    UserResponse,
    ClientUserCreate 
)
from .service import login_user, register_user, create_managed_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login_route(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Login padrão OAuth2. 
    O frontend deve enviar via form-data (username e password).
    """
    token = login_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    user = register_user(db, data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado"
        )

    token = login_user(db, data.email, data.password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/create-client-access", response_model=UserResponse)
def create_client_access(
    data: ClientUserCreate, 
    db: Session = Depends(get_db),
    current_manager: User = Depends(require_roles([UserRole.admin, UserRole.gestor]))
):
    """
    ROTA SÊNIOR: Permite que um Gestor crie um acesso para seu próprio Cliente.
    O sistema vincula automaticamente o manager_id e restringe a role para 'cliente'.
    """
    # 1. Validação de Segurança: O gestor só pode criar acesso para um cliente que ele possui
    from app.models.client import Client
    client = db.query(Client).filter(
        Client.id == data.client_id, 
        Client.owner_id == current_manager.id
    ).first()

    if not client and current_manager.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para gerenciar este cliente."
        )

    # 2. Criação do usuário vinculado
    new_user = create_managed_user(
        db=db,
        email=data.email,
        password=data.password,
        role=UserRole.cliente,
        manager_id=current_manager.id,
        client_id=data.client_id
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Erro ao criar usuário ou e-mail já existe"
        )

    return new_user
