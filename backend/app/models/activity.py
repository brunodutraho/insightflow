from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base
from datetime import datetime

class ActivityItem(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String) # 'assinatura', 'cadastro', 'cancelamento', 'configuracao'
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)