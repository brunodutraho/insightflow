from sqlalchemy import Column, String, Date, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.base import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    user_id = Column(UUID(as_uuid=True), nullable=True)

    source = Column(String)
    type = Column(String)
    value = Column(Numeric)

    extra_data = Column(JSON)
    reference_date = Column(Date)