"""
Database connection configuration for the ValueInvestorsClub API.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Get DATABASE_URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/ideas"
)
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)


# Dependency for database session
def get_db():
    """
    Creates and yields a database session.
    Uses a context manager to ensure the session is closed after use.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()