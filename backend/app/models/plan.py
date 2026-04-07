import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # dados básicos
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    price = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String, default="BRL")

    # LIMITES (HARD SAAS)
    max_users = Column(Integer, default=1)
    max_requests_per_month = Column(Integer, default=1000)
    max_clients = Column(Integer, default=1)

    # multi-tenant (caso queira planos customizados por empresa)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)

    # controle
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    is_active = Column(Boolean, default=True, nullable=False)

    # relações
    tenant = relationship("Tenant", back_populates="plans")

    subscriptions = relationship(
        "Subscription",
        back_populates="plan",
        cascade="all, delete-orphan"
    )

    plan_features = relationship(
        "PlanFeature",
        back_populates="plan",
        cascade="all, delete-orphan"
    )