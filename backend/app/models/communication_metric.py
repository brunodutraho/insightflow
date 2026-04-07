import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class CommunicationMetric(Base):
    __tablename__ = "communication_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    channel = Column(String)  # email, whatsapp

    sent = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)

    date = Column(Date)

    # RELACIONAMENTO SÊNIOR
    tenant = relationship("Tenant", back_populates="communication_metrics")