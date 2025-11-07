from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Example:
# DATABASE_URL = "postgresql+psycopg://user:pass@host:port/db"

from os import getenv
DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
