from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, nullable=False)

    discount_percent = Column(Float, nullable=True)
    discount_amount = Column(Float, nullable=True)

    max_uses = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())