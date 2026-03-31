from sqlalchemy import Column, Integer, Float, String
from app.database.base import Base

class AppConfig(Base):
    __tablename__ = "app_config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Float, nullable=False)