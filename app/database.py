from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ✅ Load database URL from Render environment
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create DB engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Import models & create tables
def init_models():
    from app import models
    Base.metadata.create_all(bind=engine)

# ✅ Run DB init at module load
init_models()
