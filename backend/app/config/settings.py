from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "InsightFlow"
    ENV: str = "development"

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/insightflow"

    class Config:
        env_file = ".env"


settings = Settings()