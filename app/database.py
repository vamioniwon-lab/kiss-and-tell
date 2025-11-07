# app/database.py
import os
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def _force_psycopg_driver(dsn: str) -> str:
    """Force SQLAlchemy to use psycopg v3 driver."""
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")

    if dsn.startswith("postgres://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgres://"):]
    elif dsn.startswith("postgresql://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgresql://"):]
    elif dsn.startswith("postgresql+psycopg2://"):
        dsn = "postgresql+psycopg://" + dsn[len("postgresql+psycopg2://"):]

    return dsn


DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = _force_psycopg_driver(DATABASE_URL)

# Log: confirm driver
try:
    p = urlparse(DATABASE_URL)
    host_info = p.hostname or ""
    if p.port:
        host_info += f":{p.port}"
    print(f"[DB] Using => {p.scheme}://{host_info}{p.path}")
except Exception:
    pass

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ✅ THIS IS THE MISSING FUNCTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
