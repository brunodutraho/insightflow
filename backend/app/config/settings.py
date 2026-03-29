# backend/app/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "InsightFlow"
    ENV: str = "development"

    # 🚀 ADICIONE VALORES PADRÃO AQUI (Evita o congelamento se o .env falhar)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/insightflow"
    SECRET_KEY: str = "super_secret_dev_key"
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas para facilitar o dev

settings = Settings()
