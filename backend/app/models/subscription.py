from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    plan = Column(String, default="free")
    max_clients = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)