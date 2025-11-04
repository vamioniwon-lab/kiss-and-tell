from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SECRET_KEY: str = "dev"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./kissandtell.db"
    MEDIA_DIR: str = "media"
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
