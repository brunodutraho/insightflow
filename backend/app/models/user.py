import enum
from sqlalchemy import Column, Integer, String, Enum
from app.database.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    gestor = "gestor"
    cliente = "cliente"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.cliente, nullable=False)