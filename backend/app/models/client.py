import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)

    # FK para owner (O usuário que manda no tenant)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Alterado para True para evitar erro circular no primeiro registro

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # --- RELAÇÕES ---

    # 1. O dono do Tenant
    owner = relationship(
        "User",
        foreign_keys=[owner_id],
        post_update=True  
    )

    # 2. Todos os usuários ligados a este Tenant
    users = relationship(
        "User",
        back_populates="tenant",
        foreign_keys="User.tenant_id", # Importante: manter o padrão do modelo User
        cascade="all, delete-orphan"
    )

    # 3. Assinaturas vinculadas ao Tenant (Empresa)
    subscriptions = relationship(
        "Subscription", 
        back_populates="tenant", 
        cascade="all, delete-orphan"
    )

    # 4. Planos
    plans = relationship(
        "Plan",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    # 5. Métricas e Business
    ad_accounts = relationship("AdAccount", back_populates="tenant", cascade="all, delete-orphan")
    ad_metrics = relationship("AdMetric", back_populates="tenant", cascade="all, delete-orphan")
    social_metrics = relationship("SocialMetric", back_populates="tenant", cascade="all, delete-orphan")
    communication_metrics = relationship("CommunicationMetric", back_populates="tenant", cascade="all, delete-orphan")
    marketing_metrics = relationship("MarketingMetric", back_populates="tenant", cascade="all, delete-orphan")

    insights = relationship(
        "Insight",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )
