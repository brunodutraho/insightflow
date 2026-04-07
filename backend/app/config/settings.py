from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # =========================
    # APP
    # =========================
    APP_NAME: str = "InsightFlow"
    ENV: Literal["development", "production", "staging"] = "development"
    DEBUG: bool = True

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL: str

    # =========================
    # SECURITY
    # =========================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # =========================
    # URLs
    # =========================
    FRONTEND_URL: str
    BACKEND_URL: str

    # =========================
    # GOOGLE OAUTH
    # =========================
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    # =========================
    # EMAIL
    # =========================
    EMAIL_FROM: str = "InsightFlow <onboarding@resend.dev>"
    EMAIL_PROVIDER: Literal["resend"] = "resend"
    RESEND_API_KEY: str

    # ========================
    # STRIPE
    # =========================
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # =========================
    # VALIDATIONS 
    # =========================
    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres")
        return v

    @field_validator("RESEND_API_KEY")
    def validate_resend_key(cls, v):
        if not v.startswith("re_"):
            raise ValueError("RESEND_API_KEY inválida")
        return v


settings = Settings()