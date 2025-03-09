# CLAUDE.md - Guide for ValueInvestorsClub Codebase

## Environment Setup
- Python Environment: 
  - Note: `python` may be aliased to homebrew python, while `python3` may not be aliased
  - Create virtual environment: `uv venv .venv` 
  - Activate: `source .venv/bin/activate`
  - Deactivate: `deactivate`

## Service Ports
- PostgreSQL Database: `5432` (default Postgres port)
- FastAPI Backend: `8000` (default FastAPI port)
- Frontend Web Server: `3000` (accessible in browser at http://localhost:3000)

## Dependency Management
- Core Requirements Files:
  - `requirements.txt`: Core production dependencies
  - `test-requirements.txt`: Testing dependencies
  - `requirements-dev.txt`: Development tools (includes both other files)
  - `api/requirements.txt`: API-specific dependencies (includes FastAPI)
  
- Installation Commands:
  - Production only: `uv pip install -r requirements.txt`
  - Test dependencies: `uv pip install -r test-requirements.txt`
  - Full development setup: `uv pip install -r requirements-dev.txt`
  - API dependencies: `uv pip install -r api/requirements.txt`
  
- Adding New Dependencies:
  - Production: `uv pip install <package> && uv pip freeze | grep <package> >> requirements.txt`
  - Testing: `uv pip install <package> && uv pip freeze | grep <package> >> test-requirements.txt`
  - API-specific: `uv pip install <package> && uv pip freeze | grep <package> >> api/requirements.txt`
  - IMPORTANT: Always use the virtual environment (`.venv`) for consistent dependency management
  - When installing locally for CI/CD with uv: Use `--system` flag with uv (e.g., `uv pip install --system -r requirements.txt`)
  - When in Docker: Use regular pip without `--system` flag (e.g., `pip install -r requirements.txt`)

## Commands
- Setup: `./install.sh` (installs dependencies with uv)
- Package Management: 
  - `uv add <package>` (for adding to pyproject.toml)
  - `uv pip install <package>` (for direct installation)
- Docker:
  - Start all services: `docker-compose up -d` (detached mode)
  - Start specific service: `docker-compose up -d <service-name>` (e.g., db, api, frontend)
  - Stop all services: `docker-compose down`
  - View logs: `docker-compose logs -f <service-name>`
  - Rebuild services: `docker-compose up -d --build`
- Scraping: 
  - `python scraper.py` (collect links)
  - `python ProcessLinks.py` (process links)
  - `scrapy crawl IdeaSpider` (scrape detailed data)
- API: `python -m api.main` (start FastAPI server)
- Database tools: `./startScript.sh` (setup/populate DB), `./describeSchema.sh` (view schema)
- Testing:
  - Local Testing:
    - Unified test runner: `./run_tests.sh` (run all tests)
      - Options: `--backend-only`, `--frontend-only`, `--e2e-only`, `--schema-only`, `--coverage`
    - Backend: `pytest -xvs api/tests/` (run backend tests)
    - Frontend: `cd frontend && npm test` (run frontend tests)
    - E2E: `cd frontend && npm run test:e2e` (run end-to-end tests)
    - API Contract: `python -m api.validate_schema` (validate API schema)
    - Test database setup: `python -m api.tests.setup_test_db --drop` (recreate test database)
    - Database Verification: `python -m pytest api/tests/test_schemas.py::test_production_database_tables_exist -v`
  
  - Docker-based Testing (preferred for CI/CD):
    - Unified Docker test runner: `./run_tests_docker.sh` (run all tests in Docker)
      - Options: 
        - `--lint-only`: Run only linting checks
        - `--backend-only`: Run only backend tests
        - `--frontend-only`: Run only frontend tests
        - `--e2e-only`: Run only end-to-end tests
        - `--schema-only`: Run only schema validation
    - All tests run in Docker containers with correct dependencies
    - Skip production DB tests: Add `-k "not test_production_database_tables_exist"` to pytest commands
    - Test environment variables:
      - `SKIP_DB_VERIFY=true`: Skip database verification in tests
      - `CI=true`: Run in CI/CD mode, skipping certain checks

## Code Style
- Dependency Management: Use uv with requirements files for dependencies
- Typing: Use type hints for all functions and SQLAlchemy column mappings
- Naming: snake_case for variables/functions, CamelCase for classes
- Imports: standard library → third-party → local modules
- Strings: Use f-strings for formatting
- Error handling: Use try/except blocks with specific exceptions
- Documentation: Triple-quoted docstrings for functions/classes
- ORM: Follow SQLAlchemy patterns for database models
- API: Use FastAPI best practices with Pydantic models
- Testing: All changes must pass existing tests; test failures are never acceptable

## Testing Strategy
- Write tests before making changes to existing functionality
- Ensure API contract changes are reflected in both server and client
- Backend tests:
  - Use pytest for unit/integration testing
  - Use FastAPI TestClient for API endpoint testing
  - Test database models with SQLAlchemy test fixtures
  - Validate request/response models against Pydantic schemas
  - Skip production database tests in CI with `-k "not test_production_database_tables_exist"`
- Frontend tests:
  - Use Jest and React Testing Library for component testing
  - Use MSW (Mock Service Worker) for API mocking
  - Test hooks separately with react-hooks-testing-library
  - Use TypeScript for type safety between API contracts
- Contract testing:
  - Generate OpenAPI schema from FastAPI
  - Validate TypeScript types against OpenAPI schema
  - Use shared Pydantic models between frontend and backend
  - In CI environments, use the existing schema file if FastAPI import fails
- Docker-based testing:
  - Use `docker-compose.test.yml` for consistent test environments
  - Run `./run_tests_docker.sh` with appropriate flags for specific test suites
  - Ensures all tests run in the same environment as production
  - Database is automatically set up for tests with consistent configuration
- CI workflow:
  - Run linting and type checking before tests
  - Run unit tests before integration tests
  - Test API contract changes separately
  - Run E2E tests with Cypress against development environment
  - Set appropriate environment variables for CI context

## Development Workflow
1. Write tests for the feature/fix you're implementing
2. Run existing tests to ensure your changes don't break anything
3. Implement your changes with proper type safety
4. If changing API contracts, update both server models and client types
   - Update the Pydantic models in `api/main.py` 
   - Update the TypeScript interfaces in `frontend/src/types/api.ts`
   - Run schema validation with `python -m api.validate_schema`
5. Run all tests to verify your implementation works
   - Use `./run_tests.sh` to run all tests
   - Fix any failing tests before proceeding
6. Submit PR only after all tests pass

## CI/CD Pipeline
The project uses GitHub Actions for continuous integration:
1. **Linting**: 
   - Checks Python code with ruff/mypy (using `--system` flag with uv)
   - Checks TypeScript with ESLint
2. **Backend Tests**: 
   - Runs pytest against a test database
   - Skips production database verification tests
   - Uses environment variables: `SKIP_DB_VERIFY=true`, `CI=true`
3. **Frontend Tests**: 
   - Runs Jest tests for React components and hooks
4. **API Contract Validation**: 
   - Ensures that API schemas are valid
   - Falls back to existing schema if FastAPI imports fail
5. **E2E Tests**: 
   - Runs Cypress tests against running servers

### Docker-Based CI Pipeline
For more reliable CI, use the Docker-based testing workflow:
1. Build and run tests in Docker containers using `docker-compose.test.yml`
2. Database is consistently set up for all test environments
3. All dependencies are properly installed in the container
4. Tests run in an environment that matches production

When submitting a PR:
- CI will automatically run all tests
- All checks must pass before merging
- Code coverage reports are generated and uploaded to Codecov
- Remember to run Docker-based tests locally before pushing: `./run_tests_docker.sh`