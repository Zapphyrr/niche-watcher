from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
import logging

from config import get_settings
from database import get_db
from models import User, UserCredential
from services import create_access_token, decode_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])
security_scheme = HTTPBearer()
settings = get_settings()
logger = logging.getLogger("niche_watcher.auth")


def _set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.environment == "production",
        max_age=settings.jwt_access_token_expire_minutes * 60,
    )


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: EmailStr


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)):
    logger.info("signup requested email=%s", payload.email)

    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        logger.info("signup creating new user email=%s", payload.email)
        user = User(email=payload.email, subscribed=True)
        db.add(user)
        db.flush()
    else:
        logger.info("signup found existing user id=%s email=%s", user.id, user.email)

    existing_credentials = db.query(UserCredential).filter(UserCredential.user_id == user.id).first()
    if existing_credentials:
        logger.warning("signup rejected because credentials already exist user_id=%s email=%s", user.id, user.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered. Use login.",
        )

    try:
        # Clean password: remove all invisible chars, non-breaking spaces, control chars
        password_cleaned = ''.join(c for c in payload.password if c.isprintable() and not c.isspace() or c == ' ').strip()
        password_cleaned = ' '.join(password_cleaned.split())  # Normalize spaces
        password_bytes = len(password_cleaned.encode('utf-8'))
        
        logger.info("signup hashing password email=%s password_bytes=%s original_bytes=%s", 
                    payload.email, password_bytes, len(payload.password.encode('utf-8')))
        print("password_cleaned:", password_cleaned)
        hashed_password = hash_password(password_cleaned)
    except ValueError as exc:
        logger.warning("signup password rejected email=%s error=%s", payload.email, exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    credentials = UserCredential(
        user_id=user.id,
        hashed_password=hashed_password,
    )
    db.add(credentials)
    db.commit()
    logger.info("signup committed user_id=%s email=%s", user.id, user.email)

    access_token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, access_token)
    logger.info("signup auth cookie set user_id=%s email=%s", user.id, user.email)
    return AuthResponse(
        access_token=access_token,
        user_id=user.id,
        email=user.email,
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    logger.info("login requested email=%s", payload.email)

    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        logger.warning("login failed user not found email=%s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    credentials = db.query(UserCredential).filter(UserCredential.user_id == user.id).first()

    try:
        # Clean password: remove all invisible chars, control chars
        password_cleaned = ''.join(c for c in payload.password if c.isprintable() and not c.isspace() or c == ' ').strip()
        password_cleaned = ' '.join(password_cleaned.split())  # Normalize spaces
        is_valid = credentials is not None and verify_password(password_cleaned, credentials.hashed_password)
    except ValueError:
        is_valid = False

    logger.info(
        "login password check email=%s user_id=%s has_credentials=%s valid=%s",
        payload.email,
        user.id,
        credentials is not None,
        is_valid,
    )

    if not is_valid:
        logger.warning("login failed invalid credentials email=%s user_id=%s", payload.email, user.id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, access_token)
    logger.info("login success user_id=%s email=%s auth cookie set", user.id, user.email)
    return AuthResponse(
        access_token=access_token,
        user_id=user.id,
        email=user.email,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    logger.info("logout requested")
    response.delete_cookie("access_token")


@router.get("/me")
def me(
    auth: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(auth.credentials)
        user_id = int(payload.get("sub", "0"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "subscribed": user.subscribed,
        "created_at": user.created_at,
    }
