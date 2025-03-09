#!/bin/bash
set -e

# Run tests script - for local development and CI/CD
# This script sets up the test environment and runs tests

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Parse command line args
BACKEND_ONLY=false
FRONTEND_ONLY=false
SCHEMA_ONLY=false
E2E_ONLY=false
SKIP_DB_SETUP=false
COVERAGE=false

for arg in "$@"
do
    case $arg in
        --backend-only)
        BACKEND_ONLY=true
        shift
        ;;
        --frontend-only)
        FRONTEND_ONLY=true
        shift
        ;;
        --schema-only)
        SCHEMA_ONLY=true
        shift
        ;;
        --e2e-only)
        E2E_ONLY=true
        shift
        ;;
        --skip-db-setup)
        SKIP_DB_SETUP=true
        shift
        ;;
        --coverage)
        COVERAGE=true
        shift
        ;;
        *)
        # Unknown option
        ;;
    esac
done

# Step 1: Setup - for E2E tests, make sure Docker is running
if [ "$E2E_ONLY" = true ]; then
    echo -e "${YELLOW}Checking if Docker is running for E2E tests...${NC}"
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Docker is running.${NC}"
    
    # Ensure PostgreSQL is running (for E2E tests only)
    echo -e "${YELLOW}Checking if PostgreSQL is running...${NC}"
    if ! docker-compose ps | grep db | grep -q "Up"; then
        echo -e "${YELLOW}PostgreSQL container is not running. Starting it...${NC}"
        docker-compose down -v && docker-compose up -d db
        
        # Wait for PostgreSQL to be ready
        echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
        attempt=0
        max_attempts=30
        while [ $attempt -lt $max_attempts ]; do
            if docker exec valueinvestorsclub-db-1 pg_isready -U postgres > /dev/null 2>&1; then
                echo -e "${GREEN}PostgreSQL is ready!${NC}"
                break
            fi
            echo -n "."
            attempt=$((attempt+1))
            sleep 2
        done
        
        if [ $attempt -eq $max_attempts ]; then
            echo -e "${RED}Failed to start PostgreSQL within timeout period.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}PostgreSQL is running.${NC}"
    fi
fi

# Note: Backend tests now use SQLite in-memory database, so no setup needed

# Step 3: Backend tests
if [ "$BACKEND_ONLY" = true ] || [ "$FRONTEND_ONLY" = false -a "$SCHEMA_ONLY" = false -a "$E2E_ONLY" = false ]; then
    echo -e "${YELLOW}Running backend tests...${NC}"
    if [ "$COVERAGE" = true ]; then
        pytest -xvs api/tests/ --cov=api --cov-report=term-missing
    else
        pytest -xvs api/tests/
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Backend tests failed.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Backend tests passed.${NC}"
fi

# Step 4: Schema validation tests
if [ "$SCHEMA_ONLY" = true ] || [ "$FRONTEND_ONLY" = false -a "$BACKEND_ONLY" = false -a "$E2E_ONLY" = false ]; then
    echo -e "${YELLOW}Running schema validation...${NC}"
    python -m api.validate_schema
    if [ $? -ne 0 ]; then
        echo -e "${RED}Schema validation failed.${NC}"
        exit 1
    fi
    
    # Frontend schema validation is commented out for now as it requires npm to be installed
    # cd frontend && npm run validate-schema
    # if [ $? -ne 0 ]; then
    #     echo -e "${RED}Frontend schema validation failed.${NC}"
    #     exit 1
    # fi
    
    echo -e "${GREEN}Schema validation passed.${NC}"
fi

# Step 5: Frontend tests
if [ "$FRONTEND_ONLY" = true ] || [ "$BACKEND_ONLY" = false -a "$SCHEMA_ONLY" = false -a "$E2E_ONLY" = false ]; then
    echo -e "${YELLOW}Running frontend tests...${NC}"
    cd frontend
    if [ "$COVERAGE" = true ]; then
        npm test -- --coverage
    else
        npm test
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Frontend tests failed.${NC}"
        exit 1
    fi
    cd ..
    echo -e "${GREEN}Frontend tests passed.${NC}"
fi

# Step 6: E2E tests
if [ "$E2E_ONLY" = true ] || [ "$FRONTEND_ONLY" = false -a "$BACKEND_ONLY" = false -a "$SCHEMA_ONLY" = false ]; then
    echo -e "${YELLOW}Running E2E tests...${NC}"
    
    # Start backend API server in the background
    echo -e "${YELLOW}Starting API server...${NC}"
    python -m api.main &
    API_PID=$!
    
    # Start frontend server in the background
    echo -e "${YELLOW}Starting frontend server...${NC}"
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    
    # Wait for servers to be ready
    echo -e "${YELLOW}Waiting for servers to start...${NC}"
    sleep 5
    
    # Run Cypress tests
    cd frontend && npm run test:e2e
    E2E_RESULT=$?
    
    # Kill the background processes
    kill $API_PID $FRONTEND_PID
    
    if [ $E2E_RESULT -ne 0 ]; then
        echo -e "${RED}E2E tests failed.${NC}"
        exit 1
    fi
    echo -e "${GREEN}E2E tests passed.${NC}"
fi

echo -e "${GREEN}All tests completed successfully!${NC}"
exit 0