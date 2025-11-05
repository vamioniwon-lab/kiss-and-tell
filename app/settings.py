from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Use env var if provided; falls back to local sqlite file
    DATABASE_URL: str = "sqlite:///./app.db"

    SECRET_KEY: str = "change-me-now-very-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
