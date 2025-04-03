#!/usr/bin/env python3
"""
Test database setup script.

This script creates and initializes a test database for running API integration tests.
It can be run manually or as part of CI/CD pipeline.

Usage:
    python -m api.tests.setup_test_db
"""
import os
import sys
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Database settings
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

# Use 'test-db' as the host when running in a Docker container, otherwise use localhost
is_docker = os.path.exists('/.dockerenv')
DB_HOST = os.environ.get('DB_HOST', 'test-db' if is_docker else 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Use the database name from DATABASE_URL if available
database_url = os.environ.get('DATABASE_URL', '')
if database_url and 'test_ideas' in database_url:
    DB_NAME = 'test_ideas'
else:
    DB_NAME = os.environ.get('TEST_DB_NAME', 'ideas_test')

# PostgreSQL connection string for administrative access (connecting to 'postgres' database)
ADMIN_DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

# Test database connection string
TEST_DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_test_database():
    """Create the test database if it doesn't exist."""
    # Connect to the default postgres database
    try:
        # Try to connect with retry mechanism
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                engine = create_engine(ADMIN_DB_URL)
                conn = engine.connect()
                conn.execution_options(isolation_level="AUTOCOMMIT")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt+1} failed: {e}")
                    print(f"Retrying in {retry_delay} seconds...")
                    import time
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to connect to database after {max_retries} attempts")
                    raise
        
        # Check if test database exists and drop it if requested
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
            print(f"Dropped existing test database '{DB_NAME}'")
        except Exception as e:
            print(f"Error dropping database: {e}")
        
        # Create the test database
        try:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Created test database '{DB_NAME}'")
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
        finally:
            conn.close()
            engine.dispose()
        
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def initialize_test_database():
    """Initialize the test database with schema and test data."""
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
    
    # Create engine for the test database
    engine = create_engine(TEST_DB_URL)
    
    # Create all tables
    try:
        Base.metadata.create_all(engine)
        print("Created database schema")
        return True
    except Exception as e:
        print(f"Error creating schema: {e}")
        return False

def main():
    """Main function to set up the test database."""
    parser = argparse.ArgumentParser(description='Set up test database for API tests')
    parser.add_argument('--drop', action='store_true', help='Drop existing database before creating')
    args = parser.parse_args()
    
    # Create the test database
    if args.drop or not database_exists():
        success = create_test_database()
        if not success:
            return 1
    
    # Initialize the database schema
    success = initialize_test_database()
    if not success:
        return 1
    
    print("Test database setup complete!")
    return 0

def database_exists():
    """Check if the test database exists."""
    try:
        engine = create_engine(TEST_DB_URL)
        with engine.connect():
            return True
    except (ProgrammingError, OperationalError):
        return False

if __name__ == "__main__":
    sys.exit(main())