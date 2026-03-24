from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "InsightFlow"
    ENV: str = "development"
    
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/insightflow"
    
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
