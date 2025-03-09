"""
Fixtures for API integration tests.
"""
import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import models and app
from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from api.main import app, get_db

# Use in-memory SQLite for tests
@pytest.fixture(scope="session")
def engine():
    """Create engine for in-memory SQLite test database."""
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

@pytest.fixture(scope="function")
def db_session(engine):
    """Create a new database session for a test."""
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # Clean up after test
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client for the FastAPI app."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app) as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()