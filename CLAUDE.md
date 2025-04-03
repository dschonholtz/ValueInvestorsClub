# CLAUDE.md - Guide for ValueInvestorsClub Codebase

## IMPORTANT: ALWAYS USE DOCKER
- **NEVER directly execute Python code or activate virtual environments outside Docker**
- All Python code, commands, and tests MUST be run through Docker
- Running Python directly may cause environment conflicts and execution problems
- This is especially critical for tools like Claude/LLMs where Python environments may not work correctly

## Quick Start (Docker Required)
- **Start all services**: `docker-compose up -d`
- **Run tests in Docker**: `./run_tests_docker.sh` (required method)
- **Service URLs**:
  - Frontend: http://localhost:3000
  - API: http://localhost:8000
  - Database: localhost:5432

## Docker Commands (Required)
- **Start services**: `docker-compose up -d` (all) or `docker-compose up -d <service-name>` (specific)
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs -f <service-name>`
- **Rebuild services**: `docker-compose up -d --build`
- **Run tests**: `./run_tests_docker.sh` with options:
  - `--lint-only`: Only lint checks
  - `--backend-only`: Only backend tests
  - `--frontend-only`: Only frontend tests
  - `--e2e-only`: Only end-to-end tests
  - `--schema-only`: Only schema validation
- **Run commands in container**: `docker-compose exec <service-name> <command>`
  - Example: `docker-compose exec api ruff check .`

## Local Environment (NOT RECOMMENDED)
- Local Python environments should be avoided in favor of Docker
- If you must use a local environment, handle with extreme caution
- Never attempt to directly activate Python environments through tools like Claude/LLMs

## Dependency Management
- **Requirements files**:
  - `requirements.txt`: Core production dependencies
  - `test-requirements.txt`: Testing dependencies
  - `requirements-dev.txt`: Development tools (includes both above)
  - `api/requirements.txt`: API-specific dependencies
- **Important flags**:
  - Local CI/CD: Use `--system` flag with uv (e.g., `uv pip install --system -r requirements.txt`)
  - Docker: Use regular pip without flags (e.g., `pip install -r requirements.txt`)

## Project Commands
- **Database**: `./startScript.sh` (setup/populate), `./describeSchema.sh` (view schema)
- **API**: `docker-compose up -d api` or `python -m api.main` (local)
- **Frontend**: `docker-compose up -d frontend` or `cd frontend && npm start` (local)
- **Scraping**: Use Docker or run with proper environment:
  - `python scraper.py` (collect links)
  - `python ProcessLinks.py` (process links)
  - `scrapy crawl IdeaSpider` (scrape detailed data)

## Code Style Essentials
- **Python**: Use type hints, snake_case, f-strings, proper error handling
- **TypeScript/React**: Follow existing patterns, use TypeScript for type safety
- **API Contracts**: Keep Pydantic models and TypeScript interfaces in sync
- **Tests**: Always required for new features or changes

## API Contract Changes
1. Update Pydantic models in `api/main.py`
2. Update TypeScript interfaces in `frontend/src/types/api.ts`
3. Validate schema: `python -m api.validate_schema` or use Docker testing

## Development Workflow (Preferred)
1. Write tests for your feature/fix
2. Implement changes with proper type safety
3. Run Docker-based tests: `./run_tests_docker.sh`
4. Fix any test failures
5. Submit PR after all tests pass in Docker environment

## CI Pipeline
The project uses GitHub Actions with Docker-based testing:
- Tests run in containers with consistent dependencies
- All checks must pass before merging
- Code coverage reports uploaded to Codecov
- Environment variables (CI=true, SKIP_DB_VERIFY=true) set automatically

**Always run Docker-based tests locally before pushing**: `./run_tests_docker.sh`