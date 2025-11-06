from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://kiss_and_tell_db_user:qzuhGUE1flC6ok37YR1zmjyQALdR86EQ@dpg-d455o81r0fns73dhoma0-a/kiss_and_tell_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    from .models import Base
    Base.metadata.create_all(bind=engine)
