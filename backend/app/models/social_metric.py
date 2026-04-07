import uuid
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class SocialMetric(Base):
    __tablename__ = "social_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    posts = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)

    date = Column(Date, nullable=False)

    # RELACIONAMENTO
    tenant = relationship("Tenant", back_populates="social_metrics")