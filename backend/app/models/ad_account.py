
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class AdAccount(Base):
    __tablename__ = "ad_accounts"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    platform = Column(String, nullable=False)  # meta, google, tiktok
    account_id = Column(String, nullable=False)
    access_token = Column(String, nullable=False)

    client = relationship("Client")