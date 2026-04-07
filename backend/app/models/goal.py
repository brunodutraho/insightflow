from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.base import Base

class GoalHistory(Base):
    __tablename__ = "goal_history"
    
    id = Column(Integer, primary_key=True, index=True)
    target_value = Column(Float, nullable=False)
    # Referência do mês (ex: 2024-03-01) para sabermos a qual mês esta meta pertence
    month_reference = Column(DateTime, nullable=False, index=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String) # Email do admin que realizou a alteração

    def __repr__(self):
        return f"<GoalHistory {self.month_reference}: {self.target_value}>"
