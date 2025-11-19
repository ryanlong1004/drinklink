from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = (
        "postgresql://drinklink:drinklink_dev_password@db:5432/drinklink"
    )

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Environment
    ENVIRONMENT: str = "development"

    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change-me-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
