import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, Boolean, ForeignKey, DateTime, Enum, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class SubscriptionStatus(str, enum.Enum):
    trialing = "trialing"
    active = "active"
    past_due = "past_due"
    canceled = "canceled"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 📅 datas principais
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🔄 status
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.trialing)
    is_active = Column(Boolean, default=True)

    # ⏳ ciclo
    trial_ends_at = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)

    # ❌ cancelamento
    canceled_at = Column(DateTime, nullable=True)

    # 💰 desconto (ESSENCIAL pro seu apply_coupon funcionar direito)
    discount_percent = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)

    # 💳 integração futura com Stripe
    stripe_subscription_id = Column(String, nullable=True)

    # 🔗 relacionamentos
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"))

    user = relationship("User", back_populates="subscriptions")
    tenant = relationship("Tenant", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")