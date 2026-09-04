from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pak_legal"
    REDIS_URL: str = "redis://localhost:6379/0"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    AI_API_URL: str = "https://llm2.jugaar.ai/v1"
    AI_API_KEY: str = ""
    AI_MODEL: str = "xiaomimimo/mimo-v2.5"

    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "pak-legal-documents"
    R2_PUBLIC_URL: str = ""

    APP_ENV: str = "development"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:5180",
        "https://kanun.8.jugaar.ai",
    ]

    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
