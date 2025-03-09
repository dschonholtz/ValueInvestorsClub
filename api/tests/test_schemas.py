"""
Tests to validate that API response schemas match the types expected by the frontend
and to ensure the database is properly set up.

This ensures that contract changes are properly reflected on both sides and that
the database tables necessary for the application to function are created.
"""
import os
import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
from sqlalchemy import inspect, create_engine

# Import response models from main API
from api.main import (
    IdeaResponse,
    IdeaDetailResponse,
    CompanyResponse,
    UserResponse,
    PerformanceResponse
)

# Import frontend type definitions (mocked here for testing)
# In a real implementation, you might generate these from TypeScript
# using a tool like openapi-typescript-codegen
class FrontendIdeaType(BaseModel):
    id: str
    link: str
    company_id: str
    user_id: str
    date: str  # Frontend uses string for dates
    is_short: bool
    is_contest_winner: bool

class FrontendCompanyType(BaseModel):
    ticker: str
    company_name: str

class FrontendUserType(BaseModel):
    username: str
    user_link: str

class FrontendDescriptionType(BaseModel):
    description: str

class FrontendCatalystsType(BaseModel):
    catalysts: str

class FrontendPerformanceType(BaseModel):
    nextDayOpen: Optional[float]
    nextDayClose: Optional[float]
    oneWeekClosePerf: Optional[float]
    twoWeekClosePerf: Optional[float]
    oneMonthPerf: Optional[float]
    threeMonthPerf: Optional[float]
    sixMonthPerf: Optional[float]
    oneYearPerf: Optional[float]
    twoYearPerf: Optional[float]
    threeYearPerf: Optional[float]
    fiveYearPerf: Optional[float]

class FrontendIdeaDetailType(FrontendIdeaType):
    company: Optional[FrontendCompanyType]
    user: Optional[FrontendUserType]
    description: Optional[FrontendDescriptionType]
    catalysts: Optional[FrontendCatalystsType]
    performance: Optional[FrontendPerformanceType]

def test_idea_response_schema_compatibility():
    """Test that backend IdeaResponse schema is compatible with frontend type."""
    # Sample data that should be valid for both schemas
    sample_data = {
        "id": "123",
        "link": "https://example.com",
        "company_id": "456",
        "user_id": "789",
        "date": "2023-01-01T12:00:00",
        "is_short": False,
        "is_contest_winner": True
    }
    
    # Validate with both schemas
    backend_model = IdeaResponse(**sample_data)
    frontend_model = FrontendIdeaType(**sample_data)
    
    # Convert to dict and compare
    backend_dict = backend_model.model_dump()
    frontend_dict = frontend_model.model_dump()
    
    # Check that every field in frontend model is present in backend model
    for key in frontend_dict:
        assert key in backend_dict, f"Field {key} missing in backend model"

def test_performance_response_schema_compatibility():
    """Test that backend PerformanceResponse schema is compatible with frontend type."""
    sample_data = {
        "nextDayOpen": 1.0,
        "nextDayClose": 1.1,
        "oneWeekClosePerf": 1.2,
        "twoWeekClosePerf": 1.3,
        "oneMonthPerf": 1.4,
        "threeMonthPerf": 1.5,
        "sixMonthPerf": 1.6,
        "oneYearPerf": 1.7,
        "twoYearPerf": 1.8,
        "threeYearPerf": 1.9,
        "fiveYearPerf": 2.0
    }
    
    # Validate with both schemas
    backend_model = PerformanceResponse(**sample_data)
    frontend_model = FrontendPerformanceType(**sample_data)
    
    # Convert to dict and compare
    backend_dict = backend_model.model_dump()
    frontend_dict = frontend_model.model_dump()
    
    # Check that every field in frontend model is present in backend model
    for key in frontend_dict:
        assert key in backend_dict, f"Field {key} missing in backend model"

def test_company_response_schema_compatibility():
    """Test that backend CompanyResponse schema is compatible with frontend type."""
    sample_data = {
        "ticker": "AAPL",
        "company_name": "Apple Inc."
    }
    
    # Validate with both schemas
    backend_model = CompanyResponse(**sample_data)
    frontend_model = FrontendCompanyType(**sample_data)
    
    # Convert to dict and compare
    backend_dict = backend_model.model_dump()
    frontend_dict = frontend_model.model_dump()
    
    # Check that every field in frontend model is present in backend model
    for key in frontend_dict:
        assert key in backend_dict, f"Field {key} missing in backend model"

def test_user_response_schema_compatibility():
    """Test that backend UserResponse schema is compatible with frontend type."""
    sample_data = {
        "username": "testuser",
        "user_link": "https://example.com/users/testuser"
    }
    
    # Validate with both schemas
    backend_model = UserResponse(**sample_data)
    frontend_model = FrontendUserType(**sample_data)
    
    # Convert to dict and compare
    backend_dict = backend_model.model_dump()
    frontend_dict = frontend_model.model_dump()
    
    # Check that every field in frontend model is present in backend model
    for key in frontend_dict:
        assert key in backend_dict, f"Field {key} missing in backend model"

def test_idea_detail_response_schema_compatibility():
    """Test that backend IdeaDetailResponse schema is compatible with frontend type."""
    sample_data = {
        "id": "123",
        "link": "https://example.com",
        "company_id": "456",
        "user_id": "789",
        "date": "2023-01-01T12:00:00",
        "is_short": False,
        "is_contest_winner": True,
        "company": {
            "ticker": "AAPL",
            "company_name": "Apple Inc."
        },
        "user": {
            "username": "testuser",
            "user_link": "https://example.com/users/testuser"
        },
        "description": {
            "description": "Test description"
        },
        "catalysts": {
            "catalysts": "Test catalysts"
        },
        "performance": {
            "nextDayOpen": 1.0,
            "nextDayClose": 1.1,
            "oneWeekClosePerf": 1.2,
            "twoWeekClosePerf": 1.3,
            "oneMonthPerf": 1.4,
            "threeMonthPerf": 1.5,
            "sixMonthPerf": 1.6,
            "oneYearPerf": 1.7,
            "twoYearPerf": 1.8,
            "threeYearPerf": 1.9,
            "fiveYearPerf": 2.0
        }
    }
    
    # Validate with both schemas
    backend_model = IdeaDetailResponse(**sample_data)
    frontend_model = FrontendIdeaDetailType(**sample_data)
    
    # Convert to dict and compare
    backend_dict = backend_model.model_dump()
    frontend_dict = frontend_model.model_dump()
    
    # Check that every field in frontend model is present in backend model
    for key in frontend_dict:
        assert key in backend_dict, f"Field {key} missing in backend model"
    
    # Check nested fields
    for key in frontend_dict["company"]:
        assert key in backend_dict["company"], f"Field company.{key} missing in backend model"
    
    for key in frontend_dict["user"]:
        assert key in backend_dict["user"], f"Field user.{key} missing in backend model"
    
    for key in frontend_dict["performance"]:
        assert key in backend_dict["performance"], f"Field performance.{key} missing in backend model"

def test_production_database_tables_exist():
    """
    Test that all required tables exist in the production database.
    
    This test verifies that the database has been properly initialized with all
    required tables. It will fail if tables are missing, which would cause
    'relation does not exist' errors in production.
    
    The test is skipped if the SKIP_DB_VERIFY environment variable is set.
    """
    if os.environ.get('SKIP_DB_VERIFY', '').lower() in ('true', '1', 't', 'yes'):
        pytest.skip("Skipping production database verification due to SKIP_DB_VERIFY setting")

    # Get database connection string from environment or use default
    db_url = os.environ.get(
        'DATABASE_URL', 
        'postgresql+psycopg2://postgres:postgres@localhost:5432/ideas'
    )
    
    try:
        # Connect to the database
        engine = create_engine(db_url)
        inspector = inspect(engine)
        
        # List of required tables
        required_tables = [
            'ideas', 
            'companies', 
            'users', 
            'descriptions', 
            'catalyst', 
            'performance'
        ]
        
        # Get actual tables in the database
        existing_tables = inspector.get_table_names()
        
        # Check if all required tables exist
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            pytest.fail(f"Missing tables in production database: {', '.join(missing_tables)}.\n"
                       f"Run ./startScript.sh to set up the database properly.")
        
        # Verify key columns in ideas table as an extra check
        columns = {c['name'] for c in inspector.get_columns('ideas')}
        required_columns = {'id', 'link', 'company_id', 'user_id', 'date', 'is_short', 'is_contest_winner'}
        missing_columns = required_columns - columns
        
        if missing_columns:
            pytest.fail(f"Missing columns in ideas table: {', '.join(missing_columns)}")
            
    except Exception as e:
        pytest.fail(f"Failed to connect to the production database: {str(e)}.\n"
                   f"Make sure the database is running and properly configured.")