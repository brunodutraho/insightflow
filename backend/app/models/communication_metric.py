from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class CommunicationMetric(Base):
    __tablename__ = "communication_metrics"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    channel = Column(String)  # email, whatsapp

    sent = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)

    date = Column(Date)

    # RELACIONAMENTO SÊNIOR
    client = relationship("Client")