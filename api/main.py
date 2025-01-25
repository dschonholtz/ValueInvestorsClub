from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# Import your models
from ValueInvestorsClub.ValueInvestorsClub.models import (
    Base,
    Idea,
    Company,
    Description,
    User,
    Catalysts,
    Performance,
)

# Create FastAPI app
app = FastAPI(
    title="Value Investors Club API",
    description="Read-only API for accessing Value Investors Club data",
    version="1.0.0",
)

# Database connection
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost/ideas"
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)


# Pydantic models for response serialization
class IdeaResponse(BaseModel):
    id: str
    link: str
    company_id: str
    user_id: str
    date: datetime
    is_short: bool
    is_contest_winner: bool

    class Config:
        orm_mode = True


class CompanyResponse(BaseModel):
    ticker: str
    company_name: str

    class Config:
        orm_mode = True


# API endpoints
@app.get("/ideas/", response_model=List[IdeaResponse])
def get_ideas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    company_id: Optional[str] = None,
    user_id: Optional[str] = None,
    is_short: Optional[bool] = None,
):
    """
    Get investment ideas with optional filtering
    """
    with Session(engine) as session:
        query = session.query(Idea)

        if company_id:
            query = query.filter(Idea.company_id == company_id)
        if user_id:
            query = query.filter(Idea.user_id == user_id)
        if is_short is not None:
            query = query.filter(Idea.is_short == is_short)

        ideas = query.offset(skip).limit(limit).all()
        return ideas


@app.get("/companies/", response_model=List[CompanyResponse])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = None,
):
    """
    Get companies with optional name/ticker search
    """
    with Session(engine) as session:
        query = session.query(Company)

        if search:
            search = f"%{search}%"
            query = query.filter(
                (Company.ticker.ilike(search)) | (Company.company_name.ilike(search))
            )

        companies = query.offset(skip).limit(limit).all()
        return companies


@app.get("/ideas/{idea_id}/performance")
def get_idea_performance(idea_id: str):
    """
    Get performance metrics for a specific idea
    """
    with Session(engine) as session:
        performance = (
            session.query(Performance).filter(Performance.idea_id == idea_id).first()
        )
        if not performance:
            raise HTTPException(status_code=404, detail="Performance data not found")
        return performance


@app.get("/ideas/{idea_id}/description")
def get_idea_description(idea_id: str):
    """
    Get the full description text for an idea
    """
    with Session(engine) as session:
        description = (
            session.query(Description).filter(Description.idea_id == idea_id).first()
        )
        if not description:
            raise HTTPException(status_code=404, detail="Description not found")
        return description


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
