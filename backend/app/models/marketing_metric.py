import uuid
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class MarketingMetric(Base):
    __tablename__ = "marketing_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    platform = Column(String, nullable=False)

    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Float, default=0)

    conversions = Column(Integer, default=0)

    date = Column(Date, nullable=False)

    # RELACIONAMENTO
    tenant = relationship("Tenant", back_populates="marketing_metrics")