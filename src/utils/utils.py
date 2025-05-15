from datetime import datetime, timedelta, UTC
import uuid
from passlib.context import CryptContext
from jose import jwt

from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifying password using bcrypt"""
    return pwd_context.verify(plain_password, hashed_password)

def create_token(id: int, login: str, username: str, expires_delta: timedelta):
    encode = {'sub': login, 'id': id, 'username': username}
    jti = str(uuid.uuid4())
    encode.update({'jti': jti})
    expires = datetime.now(UTC) + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
