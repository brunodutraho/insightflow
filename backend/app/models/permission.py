import uuid
from sqlalchemy import Column, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


# TABELA ASSOCIATIVA (PRONTA PRA ESCALAR)
user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # PADRÃO GLOBAL (NUNCA MUDA)
    # users.create, users.read, billing.manage, ads.manage
    name = Column(String, unique=True, nullable=False, index=True)

    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship(
        "User",
        secondary=user_permissions,
        back_populates="permissions"
    )