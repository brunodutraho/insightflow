# backend/app/models/plan.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)

    max_clients = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())

    subscriptions = relationship("Subscription", back_populates="plan")