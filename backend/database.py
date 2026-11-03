import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.models import Base

if os.getenv("VERCEL"):
    DEFAULT_DB = "sqlite:////tmp/nexus_platform.db"
else:
    DEFAULT_DB = "sqlite:///./nexus_platform.db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

# For SQLite, check_same_thread=False allows async endpoints to access DB
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
