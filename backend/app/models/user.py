import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class UserRole(str, enum.Enum):
    admin_master = "admin_master"
    gerente = "gerente"
    administrativo = "administrativo"
    suporte = "suporte"
    marketing = "marketing"
    gestor_interno = "gestor_interno"
    gestor_assinante = "gestor_assinante"
    cliente_final = "cliente_final"

    @classmethod
    def admin_roles(cls):
        return [cls.admin_master, cls.gerente]

    @classmethod
    def staff_roles(cls):
        return [cls.suporte, cls.marketing, cls.gestor_interno]

    @classmethod
    def client_roles(cls):
        return [cls.gestor_assinante, cls.cliente_final]


class UserStatus(str, enum.Enum):
    active = "active"
    pending_invite = "pending_invite"
    blocked = "blocked"
    inactive = "inactive"


class AuthProvider(str, enum.Enum):
    local = "local"
    google = "google"
    microsoft = "microsoft"
    apple = "apple"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=True)

    provider = Column(Enum(AuthProvider), default=AuthProvider.local, nullable=False)
    provider_id = Column(String, nullable=True, index=True)

    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    email_verified = Column(Boolean, default=False)

    status = Column(Enum(UserStatus), default=UserStatus.pending_invite, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.cliente_final, nullable=False)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # --- RELATIONS ---
    
    tenant = relationship(
        "Tenant", 
        back_populates="users", 
        foreign_keys=[tenant_id]
    )

    managed_users = relationship(
        "User",
        backref=backref("manager", remote_side=[id]),
        foreign_keys=[manager_id]
    )

    subscriptions = relationship("Subscription", back_populates="user")

    permissions = relationship(
        "Permission",
        secondary="user_permissions",
        back_populates="users"
    )

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    insights = relationship("Insight", back_populates="user")