from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment (Railway/Supabase will provide this)
# For Supabase, format: postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback for local development
    _default_pg = "postgresql://username:password@localhost:5432/reddit_sentiment_db"
    DATABASE_URL = os.getenv("DATABASE_URL", _default_pg)
    if "username:password" in DATABASE_URL or not DATABASE_URL.strip():
        DATABASE_URL = "sqlite:///./reddit_sentiment.db"

# Supabase uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

