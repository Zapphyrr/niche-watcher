from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # Email Bot (Gmail SMTP)
    email_bot_address: str = "niche.watcher.bot@gmail.com"
    email_bot_password: str = "dev_bot_password"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"

    # Auth
    jwt_secret_key: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
