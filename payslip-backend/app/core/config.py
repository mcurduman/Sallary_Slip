from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum
from app.core.settings.database_settings import DatabaseSettings
from app.core.settings.mail_settings import MailSettings
from app.core.settings.jwt_settings import JWTSettings

class Env(str, Enum):
    development = "development"
    production = "production"
class Settings(BaseSettings):
    ENV: Env = Env.development
    APP_NAME: str = "payslip"
    JOB_INTERVAL_MINUTES: int = 1
    LOG_LEVEL: str = "DEBUG"

    database: DatabaseSettings
    mail: MailSettings
    jwt: JWTSettings

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


@lru_cache
def get_settings() -> Settings:
    return Settings()
