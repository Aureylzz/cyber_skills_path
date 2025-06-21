from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Cybersecurity Assessment Platform"
    version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
