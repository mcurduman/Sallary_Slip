
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
    TEMPLATE_UUID_SINGLE: str
    COMPANY_NAME: str
    COMPANY_ADDRESS: str
    COMPANY_CITY: str
    COMPANY_COUNTRY: str
    COMPANY_ZIP_CODE: str