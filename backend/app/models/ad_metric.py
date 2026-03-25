from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.database.base import Base


class AdMetric(Base):
    __tablename__ = "ad_metrics"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Float, default=0.0)

    date = Column(Date)