from __future__ import annotations
from enum import Enum
from functools import lru_cache
from typing import Literal, Any, Optional
from pydantic import AnyUrl, PostgresDsn, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Env(str, Enum):
    development = "development"
    production = "production"

LogLevel = Literal["CRITICAL","ERROR","WARNING","INFO","DEBUG","NOTSET"]

class Settings(BaseSettings):
    ENV: Env = Env.development
    APP_NAME: str = "car-insurance"
    JOB_INTERVAL_MINUTES: int = 1
    LOG_LEVEL: Optional[LogLevel] = None
    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    LOG_FILE_PATH: str = "logs/app.log"
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",              
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def set_and_validate_db(cls, v: Optional[str], info: Any) -> str:
        if v:
            try:
                PostgresDsn(v)
            except ValidationError as e:
                raise ValueError(f"Invalid Postgres DSN for production: {e}") from e
            return v

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def default_log_level(cls, v, info):
        if v: return v
        return "DEBUG" if info.data.get("ENV", Env.development) is Env.development else "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()