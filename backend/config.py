from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/niche_watcher"
    
    # Email (Resend)
    resend_api_key: str
    sender_email: str = "noreply@niche-watcher.com"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Reddit
    reddit_client_id: str
    reddit_client_secret: str
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
