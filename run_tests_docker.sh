#!/bin/bash
set -e

# Define colors for better readability
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to running all tests if no args provided
RUN_BACKEND=true
RUN_FRONTEND=true
RUN_E2E=true
RUN_SCHEMA=true

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --backend-only)
            RUN_BACKEND=true
            RUN_FRONTEND=false
            RUN_E2E=false
            RUN_SCHEMA=false
            shift
            ;;
        --frontend-only)
            RUN_BACKEND=false
            RUN_FRONTEND=true
            RUN_E2E=false
            RUN_SCHEMA=false
            shift
            ;;
        --e2e-only)
            RUN_BACKEND=false
            RUN_FRONTEND=false
            RUN_E2E=true
            RUN_SCHEMA=false
            shift
            ;;
        --schema-only)
            RUN_BACKEND=false
            RUN_FRONTEND=false
            RUN_E2E=false
            RUN_SCHEMA=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --backend-only    Run only backend tests"
            echo "  --frontend-only   Run only frontend tests"
            echo "  --e2e-only        Run only end-to-end tests"
            echo "  --schema-only     Run only schema validation tests"
            echo "  --help            Display this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
done

# Function to run tests and report results
run_test() {
    local test_name=$1
    local service_name=$2
    
    echo -e "${YELLOW}Running $test_name tests...${NC}"
    
    # Run the test service
    docker-compose -f docker-compose.test.yml run --rm $service_name
    
    # Check if the tests passed
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $test_name tests passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ $test_name tests failed!${NC}"
        return 1
    fi
}

# Make sure the test database is up
echo -e "${BLUE}Starting test database...${NC}"
docker-compose -f docker-compose.test.yml up -d test-db

# Initialize result tracking
EXIT_CODE=0

# Run tests based on flags
if [ "$RUN_BACKEND" = true ]; then
    run_test "Backend" "backend-tests" || EXIT_CODE=1
fi

if [ "$RUN_SCHEMA" = true ]; then
    run_test "Schema" "schema-tests" || EXIT_CODE=1
fi

if [ "$RUN_FRONTEND" = true ]; then
    run_test "Frontend" "frontend-tests" || EXIT_CODE=1
fi

if [ "$RUN_E2E" = true ]; then
    run_test "End-to-End" "e2e-tests" || EXIT_CODE=1
fi

# Clean up resources
echo -e "${BLUE}Cleaning up test environment...${NC}"
docker-compose -f docker-compose.test.yml down

# Final results
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
else
    echo -e "${RED}Some tests failed. Please check the output above.${NC}"
fi

exit $EXIT_CODE