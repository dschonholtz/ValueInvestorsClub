"""
Routes package for the ValueInvestorsClub API.
Contains all API route handlers.
"""
from api.routes.health import router as health_router
from api.routes.ideas import router as ideas_router
from api.routes.companies import router as companies_router
from api.routes.users import router as users_router

__all__ = [
    "health_router",
    "ideas_router", 
    "companies_router", 
    "users_router"
]