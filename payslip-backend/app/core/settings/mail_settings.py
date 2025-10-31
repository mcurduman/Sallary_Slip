
from pydantic_settings import BaseSettings
from pydantic import EmailStr, SecretStr
class MailSettings(BaseSettings):
    SERVER: str
    PORT: int
    USERNAME: str
    PASSWORD: SecretStr
    DEFAULT_SENDER: EmailStr
    USE_TLS: bool = True
    USE_SSL: bool = False
    TEMPLATE_UUID: str