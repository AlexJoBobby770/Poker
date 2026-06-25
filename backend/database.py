# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load variables from backend/.env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# The engine handles the active network connection pool to PostgreSQL
engine = create_engine(DATABASE_URL)

# Every database operations runs inside an isolated, atomic Session transaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database model classes will inherit from
Base = declarative_base()

def get_db():
    """FastAPI Dependency to safely yield a database session per API request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()