from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.client import Client
from app.models.user_profile import UserProfile

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

    role_value = user.role.value if hasattr(user.role, "value") else user.role

    token = create_access_token({
        "sub": str(user.id),
        "role": role_value
    })

    return token


def register_user(db: Session, data):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        return None

    # USER (SEM NAME)
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.gestor
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # CLIENT
    client = Client(
        name=data.agency_name or "Minha Empresa",
        owner_id=new_user.id
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    # 🔗 VÍNCULO
    new_user.client_id = client.id
    db.commit()

    # PROFILE (AQUI VAI O NAME E RESTO)
    profile = UserProfile(
        user_id=new_user.id,
        name=data.name,
        phone=data.phone,
        country=data.country,
        state=data.state,
        agency_name=data.agency_name,
        company_size=data.company_size,
        source=data.source
    )

    db.add(profile)
    db.commit()

    return new_user

def create_managed_user(
    db: Session,
    email: str,
    password: str,
    role: UserRole,
    manager_id: int,
    client_id: int
):
    """
    🚀 Criação de usuário com vínculo hierárquico (Gestor → Cliente)
    """

    if db.query(User).filter(User.email == email).first():
        return None

    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        manager_id=manager_id,
        client_id=client_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

