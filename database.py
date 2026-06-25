# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Get the absolute path to the directory containing database.py (backend/)
BASE_DIR = Path(__file__).resolve().parent

# 2. Point explicitly to the .env file inside that folder
dotenv_path = BASE_DIR / ".env"

# 3. Load it up securely
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(f"DATABASE_URL environment variable is not set! Checked path: {dotenv_path}")

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