import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=True)

    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    agency_name = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    source = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")