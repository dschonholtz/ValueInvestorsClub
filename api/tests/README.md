# API Integration Tests

This directory contains integration tests for the ValueInvestorsClub API.

## Running the Tests

To run all tests:

```bash
pytest -xvs api/tests/
```

To run a specific test file:

```bash
pytest -xvs api/tests/test_ideas_api.py
```

To run a specific test:

```bash
pytest -xvs api/tests/test_ideas_api.py::test_get_ideas_with_company_filter
```

## Test Structure

1. **Database fixtures**: Tests use a test database with sample data created in fixtures
2. **API client**: Tests use FastAPI's TestClient to make requests to the API
3. **Test cases**: Each test focuses on a specific API endpoint and feature

## Testing Strategy

### Integration Tests

The tests in this directory verify that:

1. API endpoints return the expected status codes and data
2. Query parameters work correctly (e.g., filtering, pagination)
3. API contract is maintained between frontend and backend

### Schema Validation

Schema validation tests ensure that:

1. API response schemas match the types expected by the frontend
2. Contract changes are properly reflected on both sides

## Setting Up Test Database

Before running tests, you need to create a test database:

```bash
# Create test database
createdb -U postgres ideas_test

# Run migrations on test database
# Add your migration commands here
```

## Adding New Tests

When adding new features or endpoints:

1. Add test cases to the appropriate test file
2. Test all query parameters and edge cases
3. Update the schema validation tests if needed