from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    canceled_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    plan_id = Column(Integer, ForeignKey("plans.id"))

    is_active = Column(Boolean, default=True)

    # RELACIONAMENTOS
    user = relationship("User")
    plan = relationship("Plan", back_populates="subscriptions")