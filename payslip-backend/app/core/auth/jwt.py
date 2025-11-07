from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.utils.errors.CredentialsException import CredentialsException
from app.core.config import get_settings

from app.core.logging import get_logger
logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().jwt.SECRET_KEY.get_secret_value(), algorithm=get_settings().jwt.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, get_settings().jwt.SECRET_KEY.get_secret_value(), algorithms=[get_settings().jwt.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
        return username
    except jwt.JWTError:
        raise CredentialsException()