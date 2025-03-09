# CLAUDE.md - Guide for ValueInvestorsClub Codebase

## Commands
- Setup: `./install.sh` (installs dependencies with uv)
- Package Management: 
  - `uv add <package>` (for adding to pyproject.toml)
  - `uv pip install <package>` (for direct installation)
- Database: `docker-compose up` (starts PostgreSQL)
- Scraping: 
  - `python3 scraper.py` (collect links)
  - `python3 ProcessLinks.py` (process links)
  - `scrapy crawl IdeaSpider` (scrape detailed data)
- API: `python3 -m api.main` (start FastAPI server)
- Database tools: `./startScript.sh` (setup/populate DB), `./describeSchema.sh` (view schema)
- Testing:
  - Unified test runner: `./run_tests.sh` (run all tests)
    - Options: `--backend-only`, `--frontend-only`, `--e2e-only`, `--schema-only`, `--coverage`
  - Backend: `pytest -xvs api/tests/` (run backend tests)
  - Frontend: `cd frontend && npm test` (run frontend tests)
  - E2E: `cd frontend && npm run test:e2e` (run end-to-end tests)
  - API Contract: `python3 -m api.validate_schema` (validate API schema)
  - Test database setup: `python -m api.tests.setup_test_db --drop` (recreate test database)

## Code Style
- Dependency Management: Use uv and pyproject.toml for dependencies
- Typing: Use type hints for all functions and SQLAlchemy column mappings
- Naming: snake_case for variables/functions, CamelCase for classes
- Imports: standard library → third-party → local modules
- Strings: Use f-strings for formatting
- Error handling: Use try/except blocks with specific exceptions
- Documentation: Triple-quoted docstrings for functions/classes
- ORM: Follow SQLAlchemy patterns for database models
- API: Use FastAPI best practices with Pydantic models

## Testing Strategy
- Write tests before making changes to existing functionality
- Ensure API contract changes are reflected in both server and client
- Backend tests:
  - Use pytest for unit/integration testing
  - Use FastAPI TestClient for API endpoint testing
  - Test database models with SQLAlchemy test fixtures
  - Validate request/response models against Pydantic schemas
- Frontend tests:
  - Use Jest and React Testing Library for component testing
  - Use MSW (Mock Service Worker) for API mocking
  - Test hooks separately with react-hooks-testing-library
  - Use TypeScript for type safety between API contracts
- Contract testing:
  - Generate OpenAPI schema from FastAPI
  - Validate TypeScript types against OpenAPI schema
  - Use shared Pydantic models between frontend and backend
- CI workflow:
  - Run linting and type checking before tests
  - Run unit tests before integration tests
  - Test API contract changes separately
  - Run E2E tests with Cypress against development environment

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
1. **Linting**: Checks Python code with ruff/mypy and TypeScript with ESLint
2. **Backend Tests**: Runs pytest against a test database
3. **Frontend Tests**: Runs Jest tests for React components and hooks
4. **API Contract Validation**: Ensures that API schemas are valid
5. **E2E Tests**: Runs Cypress tests against running servers

When submitting a PR:
- CI will automatically run all tests
- All checks must pass before merging
- Code coverage reports are generated and uploaded to Codecov