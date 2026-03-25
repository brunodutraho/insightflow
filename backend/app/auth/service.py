from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from .utils import verify_password, create_access_token, hash_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        return None

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })

    return token

def register_user(db: Session, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None

    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.cliente
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
