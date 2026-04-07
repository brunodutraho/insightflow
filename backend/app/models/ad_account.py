import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class AdAccount(Base):
    __tablename__ = "ad_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    platform = Column(String, nullable=False)  # meta, google, tiktok
    account_id = Column(String, nullable=False)
    access_token = Column(String, nullable=False)

    # RELACIONAMENTO CORRIGIDO (SEM WARNING)
    tenant = relationship(
        "Tenant",
        back_populates="ad_accounts",
        overlaps="ad_accounts"
    )