# app/database.py
import os
from urllib.parse import urlparse, urlunparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def _force_psycopg_driver(dsn: str) -> str:
    """
    Ensure DSN uses SQLAlchemy's psycopg (v3) driver.
    Normalizes:
      - postgres://...                 -> postgresql+psycopg://...
      - postgresql://...               -> postgresql+psycopg://...
      - postgresql+psycopg2://...      -> postgresql+psycopg://...
    """
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")

    # If URL has no explicit driver, or wrong driver, normalize it
    if dsn.startswith("postgres://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgres://"):]
    elif dsn.startswith("postgresql://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgresql://"):]
    elif dsn.startswith("postgresql+psycopg2://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgresql+psycopg2://"):]

    return dsn

DATABASE_URL = os.getenv("DATABASE_URL")  # from Render
DATABASE_URL = _force_psycopg_driver(DATABASE_URL)

# (Optional) mask password in a startup log so you can verify the driver in Render logs
try:
    parsed = urlparse(DATABASE_URL)
    safe_netloc = parsed.hostname or ""
    if parsed.port:
        safe_netloc += f":{parsed.port}"
    print(f"[DB] Using dialect=postgresql driver=psycopg -> {parsed.scheme}://{safe_netloc}{parsed.path}")
except Exception:
    pass

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
