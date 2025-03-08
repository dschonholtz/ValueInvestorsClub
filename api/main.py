from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from pydantic import BaseModel, Field
import os

# Import models
from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from ValueInvestorsClub.ValueInvestorsClub.models.Company import Company
from ValueInvestorsClub.ValueInvestorsClub.models.Description import Description
from ValueInvestorsClub.ValueInvestorsClub.models.User import User
from ValueInvestorsClub.ValueInvestorsClub.models.Catalysts import Catalysts
from ValueInvestorsClub.ValueInvestorsClub.models.Performance import Performance

# Create FastAPI app
app = FastAPI(
    title="Value Investors Club API",
    description="Read-only API for accessing Value Investors Club data",
    version="1.0.0",
)

# Get DATABASE_URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/ideas"
)
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)


# Dependency for database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# Pydantic models for response serialization
class PerformanceResponse(BaseModel):
    nextDayOpen: Optional[float] = None
    nextDayClose: Optional[float] = None
    oneWeekClosePerf: Optional[float] = None
    twoWeekClosePerf: Optional[float] = None
    oneMonthPerf: Optional[float] = None
    threeMonthPerf: Optional[float] = None
    sixMonthPerf: Optional[float] = None
    oneYearPerf: Optional[float] = None
    twoYearPerf: Optional[float] = None
    threeYearPerf: Optional[float] = None
    fiveYearPerf: Optional[float] = None

    model_config = {"from_attributes": True}


class DescriptionResponse(BaseModel):
    description: str

    model_config = {"from_attributes": True}


class CatalystsResponse(BaseModel):
    catalysts: str

    model_config = {"from_attributes": True}


class CompanyResponse(BaseModel):
    ticker: str
    company_name: str

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    username: str
    user_link: str

    model_config = {"from_attributes": True}


class IdeaResponse(BaseModel):
    id: str
    link: Optional[str] = ""  # Make link optional with default empty string
    company_id: str
    user_id: str
    date: datetime
    is_short: bool
    is_contest_winner: bool

    model_config = {"from_attributes": True}


class IdeaDetailResponse(IdeaResponse):
    company: Optional[CompanyResponse] = None
    user: Optional[UserResponse] = None
    description: Optional[DescriptionResponse] = None
    catalysts: Optional[CatalystsResponse] = None
    performance: Optional[PerformanceResponse] = None

    model_config = {"from_attributes": True}


# API endpoints
@app.get("/ideas/", response_model=List[IdeaResponse])
def get_ideas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    company_id: Optional[str] = None,
    user_id: Optional[str] = None,
    is_short: Optional[bool] = None,
    is_contest_winner: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """
    Get investment ideas with optional filtering
    """
    try:
        query = db.query(Idea)

        # Apply filters
        if company_id:
            query = query.filter(Idea.company_id == company_id)
        if user_id:
            query = query.filter(Idea.user_id == user_id)
        if is_short is not None:
            query = query.filter(Idea.is_short == is_short)
        if is_contest_winner is not None:
            query = query.filter(Idea.is_contest_winner == is_contest_winner)
        if start_date:
            query = query.filter(func.date(Idea.date) >= start_date)
        if end_date:
            query = query.filter(func.date(Idea.date) <= end_date)

        # Ensure required fields are not NULL
        query = query.filter(Idea.id.isnot(None))
        query = query.filter(Idea.company_id.isnot(None))
        query = query.filter(Idea.user_id.isnot(None))
        query = query.filter(Idea.date.isnot(None))
        
        ideas = query.order_by(Idea.date.desc()).offset(skip).limit(limit).all()
        
        # Create a list of valid response objects
        result = []
        for idea in ideas:
            # Convert link to empty string if None
            if idea.link is None:
                idea.link = ""
            result.append(idea)
            
        return result
    except Exception as e:
        print(f"Error in get_ideas: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/ideas/{idea_id}", response_model=IdeaDetailResponse)
def get_idea_detail(idea_id: str, db: Session = Depends(get_db)):
    """
    Get complete details for a specific idea including related data
    """
    try:
        # Query idea with eager loading of related objects
        idea = (
            db.query(Idea)
            .options(
                joinedload(Idea.company),
                joinedload(Idea.user),
            )
            .filter(Idea.id == idea_id)
            .first()
        )
        
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        
        # Ensure link is not None
        if idea.link is None:
            idea.link = ""
            
        # Query related data
        description = db.query(Description).filter(Description.idea_id == idea_id).first()
        catalysts = db.query(Catalysts).filter(Catalysts.idea_id == idea_id).first()
        
        # Create base response from idea
        result = IdeaDetailResponse.model_validate(idea)
        
        # Manually attach related objects with explicit field mapping
        if description:
            result.description = DescriptionResponse(description=description.description)
        if catalysts:
            result.catalysts = CatalystsResponse(catalysts=catalysts.catalysts)
        
        # Try to get performance data, but don't fail if it doesn't exist
        try:
            performance = db.query(Performance).filter(Performance.idea_id == idea_id).first()
            if performance:
                result.performance = PerformanceResponse(
                    nextDayOpen=performance.nextDayOpen,
                    nextDayClose=performance.nextDayClose,
                    oneWeekClosePerf=performance.oneWeekClosePerf,
                    twoWeekClosePerf=performance.twoWeekClosePerf,
                    oneMonthPerf=performance.oneMonthPerf,
                    threeMonthPerf=performance.threeMonthPerf,
                    sixMonthPerf=performance.sixMonthPerf,
                    oneYearPerf=performance.oneYearPerf,
                    twoYearPerf=performance.twoYearPerf,
                    threeYearPerf=performance.threeYearPerf,
                    fiveYearPerf=performance.fiveYearPerf
                )
        except Exception as e:
            # Log the error but continue
            print(f"Error loading performance data: {e}")
            
        return result
    except Exception as e:
        print(f"Error in get_idea_detail: {e}")
        # Return a proper error response
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/companies/", response_model=List[CompanyResponse])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get companies with optional name/ticker search
    """
    query = db.query(Company)

    if search:
        search = f"%{search}%"
        query = query.filter(
            (Company.ticker.ilike(search)) | (Company.company_name.ilike(search))
        )

    companies = query.order_by(Company.ticker).offset(skip).limit(limit).all()
    return companies


@app.get("/users/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get users with optional username search
    """
    query = db.query(User)

    if search:
        search = f"%{search}%"
        query = query.filter(User.username.ilike(search))

    users = query.order_by(User.username).offset(skip).limit(limit).all()
    return users


@app.get("/ideas/{idea_id}/performance", response_model=PerformanceResponse)
def get_idea_performance(idea_id: str, db: Session = Depends(get_db)):
    """
    Get performance metrics for a specific idea
    """
    performance = db.query(Performance).filter(Performance.idea_id == idea_id).first()
    if not performance:
        raise HTTPException(status_code=404, detail="Performance data not found")
    
    # Create a response that explicitly maps the fields
    response = PerformanceResponse(
        nextDayOpen=performance.nextDayOpen,
        nextDayClose=performance.nextDayClose,
        oneWeekClosePerf=performance.oneWeekClosePerf,
        twoWeekClosePerf=performance.twoWeekClosePerf,
        oneMonthPerf=performance.oneMonthPerf,
        threeMonthPerf=performance.threeMonthPerf,
        sixMonthPerf=performance.sixMonthPerf,
        oneYearPerf=performance.oneYearPerf,
        twoYearPerf=performance.twoYearPerf,
        threeYearPerf=performance.threeYearPerf,
        fiveYearPerf=performance.fiveYearPerf
    )
    return response


@app.get("/ideas/{idea_id}/description", response_model=DescriptionResponse)
def get_idea_description(idea_id: str, db: Session = Depends(get_db)):
    """
    Get the full description text for an idea
    """
    description = db.query(Description).filter(Description.idea_id == idea_id).first()
    if not description:
        raise HTTPException(status_code=404, detail="Description not found")
    
    # Create a response that explicitly maps the fields
    response = DescriptionResponse(description=description.description)
    return response


@app.get("/ideas/{idea_id}/catalysts", response_model=CatalystsResponse)
def get_idea_catalysts(idea_id: str, db: Session = Depends(get_db)):
    """
    Get the catalysts text for an idea
    """
    catalysts = db.query(Catalysts).filter(Catalysts.idea_id == idea_id).first()
    if not catalysts:
        raise HTTPException(status_code=404, detail="Catalysts not found")
    
    # Create a response that explicitly maps the fields
    response = CatalystsResponse(catalysts=catalysts.catalysts)
    return response


# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

# Debug endpoint for idea detail
@app.get("/debug/ideas/{idea_id}")
def debug_idea_detail(idea_id: str, db: Session = Depends(get_db)):
    """
    Simple debug endpoint to get an idea by ID
    """
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Return just the idea data as a simple dict to test basic connectivity
    return {
        "id": idea.id,
        "link": idea.link,
        "company_id": idea.company_id,
        "user_id": idea.user_id,
        "date": idea.date.isoformat(),
        "is_short": idea.is_short,
        "is_contest_winner": idea.is_contest_winner
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
