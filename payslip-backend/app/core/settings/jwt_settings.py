from pydantic_settings import BaseSettings
from pydantic import SecretStr

class JWTSettings(BaseSettings):
    SECRET_KEY: SecretStr
    TOKEN_LOCATION: list[str] = ["headers"]
    COOKIE_CSRF_PROTECT: bool = False
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "Lax"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30