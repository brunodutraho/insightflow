import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    gestor = "gestor"
    cliente = "cliente"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(UserRole, name="user_role"), default=UserRole.cliente, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    insights = relationship("Insight", back_populates="user")