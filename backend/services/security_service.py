from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()
MAX_BCRYPT_PASSWORD_BYTES = 72


def _validate_password_length(password: str) -> None:
    # bcrypt has a hard 72-byte input limit. We validate early to avoid runtime 500 errors.
    password_bytes_len = len(password.encode("utf-8"))
    if password_bytes_len > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError("Password too long: bcrypt supports up to 72 UTF-8 bytes.")


def hash_password(password: str) -> str:
    _validate_password_length(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        _validate_password_length(plain_password)
    except ValueError:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire_delta = expires_minutes or settings.jwt_access_token_expire_minutes
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload = {
        "sub": subject,
        "exp": expire_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
