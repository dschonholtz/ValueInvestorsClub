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