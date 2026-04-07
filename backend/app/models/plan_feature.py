import uuid
from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class PlanFeature(Base):
    __tablename__ = "plan_features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"))
    feature_id = Column(UUID(as_uuid=True), ForeignKey("features.id"))

    enabled = Column(Boolean, default=True)

    plan = relationship("Plan", back_populates="plan_features")
    feature = relationship("Feature", back_populates="plan_features")