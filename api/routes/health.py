"""
Health check routes for the ValueInvestorsClub API.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns a simple response indicating that the API is healthy.
    """
    return {"status": "healthy"}