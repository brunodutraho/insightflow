from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.database import get_db
from app.models.user import User
from app.models.client import Client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user 

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_roles(allowed_roles: list[str]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return user
    return role_checker


# Global Customer Validation
def validate_client_access(
    client_id: int,
    user: User,
    db: Session
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if user.role == "admin":
        return client

    if user.role == "manager" and client.owner_id == user.id:
        return client

    if user.role == "client" and client.id == user.id:
        return client

    raise HTTPException(status_code=403, detail="Access denied")