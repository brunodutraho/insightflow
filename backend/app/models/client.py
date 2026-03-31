from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Dono da empresa (Gestor)
    owner = relationship(
        "User",
        foreign_keys=[owner_id]
    )

    # Usuários vinculados (multi-tenant real)
    users = relationship(
        "User",
        back_populates="company",
        foreign_keys="User.client_id",
        cascade="all, delete-orphan"
    )

    # RELACIONAMENTO CORRETO COM AD ACCOUNTS
    ad_accounts = relationship(
        "AdAccount",
        back_populates="client",
        cascade="all, delete-orphan"
    )

    # Dados de marketing (mantido consistente)
    ad_metrics = relationship(
        "AdMetric",
        back_populates="client",
        cascade="all, delete-orphan"
    )

    social_metrics = relationship(
        "SocialMetric",
        back_populates="client",
        cascade="all, delete-orphan"
    )

    # Insights ligados ao cliente
    insights = relationship(
        "Insight",
        back_populates="client",
        cascade="all, delete-orphan"
    )