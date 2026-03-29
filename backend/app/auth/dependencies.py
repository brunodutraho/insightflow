from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.database import get_db
from app.models.user import User, UserRole
from app.models.client import Client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 🔐 PEGA USUÁRIO REAL DO BANCO
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# 🔐 CONTROLE DE ROLES
def require_roles(allowed_roles: list[str]):
    def role_checker(user: User = Depends(get_current_user)):

        user_role = user.role.value if hasattr(user.role, "value") else user.role

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Permissão insuficiente"
            )

        return user

    return role_checker


# 🔐 CONTROLE DE HIERARQUIA (MULTI-TENANT)
def validate_hierarchy_access(client_id: int, user: User, db: Session):
    """
    Regras:
    - Admin: acesso total
    - Gestor: apenas clientes que ele é owner
    - Cliente: apenas seu próprio client_id
    """

    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    user_role = user.role.value if hasattr(user.role, "value") else user.role

    # ADMIN
    if user_role == UserRole.admin or user_role == "admin":
        return client

    # GESTOR
    if user_role == UserRole.gestor or user_role == "gestor":
        if client.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Cliente não pertence a você")
        return client

    # CLIENTE
    if user_role == UserRole.cliente or user_role == "cliente":
        if user.client_id != client_id:
            raise HTTPException(status_code=403, detail="Acesso restrito")
        return client

    raise HTTPException(status_code=403, detail="Acesso negado")