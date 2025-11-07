import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")  # set on Render dashboard

# pg8000 is the driver used by SQLAlchemy automatically for postgresql+pg8000
# If your URL starts with postgresql:// it still works with pg8000 installed.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()
