from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # Email (Resend)
    resend_api_key: str = "dev_key"
    sender_email: str = "noreply@niche-watcher.com"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Reddit
    reddit_client_id: str = "dev_reddit_id"
    reddit_client_secret: str = "dev_reddit_secret"
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
