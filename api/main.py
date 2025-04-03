"""
Main entry point for the Value Investors Club API.
Creates the FastAPI application and includes all routes.
"""
import uvicorn
from fastapi import FastAPI

from api.routes import health_router, ideas_router, companies_router, users_router

# Create FastAPI app
app = FastAPI(
    title="Value Investors Club API",
    description="Read-only API for accessing Value Investors Club data",
    version="1.0.0",
)

# Include all routers
app.include_router(health_router)
app.include_router(ideas_router)
app.include_router(companies_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
