from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.database.base import Base

class SocialMetric(Base):
    __tablename__ = "social_metrics"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    followers = Column(Integer, default=0)
    # AJUSTE: Mude para o nome que está no banco
    engagement_rate = Column(Float, default=0.0) 
    posts = Column(Integer, default=0)
    
    # OPCIONAL: Se quiser guardar o growth_rate no banco, adicione:
    growth_rate = Column(Float, default=0.0)

    date = Column(Date, nullable=False)
