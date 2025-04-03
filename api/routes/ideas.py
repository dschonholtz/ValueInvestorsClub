"""
Routes for investment ideas in the ValueInvestorsClub API.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from api.database import get_db
from api.models import Idea, Description, Catalysts, Performance
from api.schemas import (
    IdeaResponse,
    IdeaDetailResponse,
    DescriptionResponse,
    CatalystsResponse,
    PerformanceResponse,
)

router = APIRouter()


@router.get("/ideas/", response_model=List[IdeaResponse])
def get_ideas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    company_id: Optional[str] = None,
    user_id: Optional[str] = None,
    is_short: Optional[bool] = None,
    is_contest_winner: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    has_performance: Optional[bool] = None,
    min_performance: Optional[float] = None,
    max_performance: Optional[float] = None,
    performance_period: str = Query("one_year_perf", description="Which performance period to filter/sort by"),
    sort_by: str = Query("date", description="Field to sort by. Can be date or performance"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    """
    Get investment ideas with optional filtering and sorting by performance.
    """
    try:
        # Start with a query on Idea
        query = db.query(Idea)
        
        # Determine if we need to join with Performance table
        needs_performance_join = (
            has_performance is not None or 
            min_performance is not None or 
            max_performance is not None or
            sort_by == "performance"
        )
        
        # Join with Performance if needed for filtering or sorting
        if needs_performance_join:
            query = query.outerjoin(Performance, Idea.id == Performance.idea_id)
        
        # Apply basic filters
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

        # Apply performance filters
        if has_performance is not None:
            if has_performance:
                query = query.filter(Performance.idea_id.isnot(None))
            else:
                query = query.filter(or_(
                    Performance.idea_id.is_(None),
                    and_(
                        # For filtering out ideas without any performance data where all metrics are null
                        Performance.oneWeekClosePerf.is_(None),
                        Performance.twoWeekClosePerf.is_(None),
                        Performance.oneMonthPerf.is_(None),
                        Performance.threeMonthPerf.is_(None),
                        Performance.sixMonthPerf.is_(None),
                        Performance.oneYearPerf.is_(None),
                        Performance.twoYearPerf.is_(None),
                        Performance.threeYearPerf.is_(None),
                        Performance.fiveYearPerf.is_(None)
                    )
                ))
        
        # Map performance_period to database column
        perf_column = None
        if performance_period == "one_week_perf":
            perf_column = Performance.oneWeekClosePerf
        elif performance_period == "two_week_perf":
            perf_column = Performance.twoWeekClosePerf
        elif performance_period == "one_month_perf":
            perf_column = Performance.oneMonthPerf
        elif performance_period == "three_month_perf":
            perf_column = Performance.threeMonthPerf
        elif performance_period == "six_month_perf":
            perf_column = Performance.sixMonthPerf
        elif performance_period == "one_year_perf":
            perf_column = Performance.oneYearPerf
        elif performance_period == "two_year_perf":
            perf_column = Performance.twoYearPerf
        elif performance_period == "three_year_perf":
            perf_column = Performance.threeYearPerf
        elif performance_period == "five_year_perf":
            perf_column = Performance.fiveYearPerf
        else:
            perf_column = Performance.oneYearPerf  # Default
        
        # Apply min/max performance filters if column is determined
        if perf_column is not None:
            if min_performance is not None:
                query = query.filter(perf_column >= min_performance)
            if max_performance is not None:
                query = query.filter(perf_column <= max_performance)
        
        # Ensure required fields are not NULL
        query = query.filter(Idea.id.isnot(None))
        query = query.filter(Idea.company_id.isnot(None))
        query = query.filter(Idea.user_id.isnot(None))
        query = query.filter(Idea.date.isnot(None))
        
        # Apply sorting
        if sort_by == "performance" and perf_column is not None:
            if sort_order.lower() == "asc":
                query = query.order_by(perf_column.asc())
            else:
                query = query.order_by(perf_column.desc())
        else:
            # Default to date sorting
            if sort_order.lower() == "asc":
                query = query.order_by(Idea.date.asc())
            else:
                query = query.order_by(Idea.date.desc())
        
        ideas = query.offset(skip).limit(limit).all()
        
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


@router.get("/ideas/{idea_id}", response_model=IdeaDetailResponse)
def get_idea_detail(idea_id: str, db: Session = Depends(get_db)):
    """
    Get complete details for a specific idea including related data.
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
            # Make sure the 404 is not caught by the general exception handler
            print(f"Idea with ID {idea_id} not found")
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
                # Create base performance response with standard metrics
                perf_response = PerformanceResponse(
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
                
                # Add timeline data
                timeline_periods = [
                    ("1W", performance.oneWeekClosePerf),
                    ("2W", performance.twoWeekClosePerf),
                    ("1M", performance.oneMonthPerf),
                    ("3M", performance.threeMonthPerf),
                    ("6M", performance.sixMonthPerf),
                    ("1Y", performance.oneYearPerf),
                    ("2Y", performance.twoYearPerf),
                    ("3Y", performance.threeYearPerf),
                    ("5Y", performance.fiveYearPerf)
                ]
                
                # Filter out None values
                valid_periods = [(label, value) for label, value in timeline_periods if value is not None]
                
                if valid_periods:
                    perf_response.timeline_labels = [period[0] for period in valid_periods]
                    perf_response.timeline_values = [period[1] for period in valid_periods]
                    
                    # Create performance periods dictionary
                    perf_response.performance_periods = {
                        period[0]: period[1] for period in valid_periods
                    }
                
                result.performance = perf_response
        except Exception as e:
            # Log the error but continue
            print(f"Error loading performance data: {e}")
            
        return result
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        print(f"Error in get_idea_detail: {e}")
        # Return a proper error response for other exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/ideas/{idea_id}/performance", response_model=PerformanceResponse)
def get_idea_performance(idea_id: str, db: Session = Depends(get_db)):
    """
    Get performance metrics for a specific idea including timeline data.
    """
    try:
        performance = db.query(Performance).filter(Performance.idea_id == idea_id).first()
        if not performance:
            raise HTTPException(status_code=404, detail="Performance data not found")
        
        # Get the core performance metrics
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
        
        # Create timeline data from the performance metrics
        # Define the timeline periods and labels
        timeline_periods = [
            ("1W", performance.oneWeekClosePerf),
            ("2W", performance.twoWeekClosePerf),
            ("1M", performance.oneMonthPerf),
            ("3M", performance.threeMonthPerf),
            ("6M", performance.sixMonthPerf),
            ("1Y", performance.oneYearPerf),
            ("2Y", performance.twoYearPerf),
            ("3Y", performance.threeYearPerf),
            ("5Y", performance.fiveYearPerf)
        ]
        
        # Filter out None values and create the timeline data
        valid_periods = [(label, value) for label, value in timeline_periods if value is not None]
        
        if valid_periods:
            response.timeline_labels = [period[0] for period in valid_periods]
            response.timeline_values = [period[1] for period in valid_periods]
            
            # Create performance periods dictionary
            response.performance_periods = {
                period[0]: period[1] for period in valid_periods
            }
        
        return response
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        print(f"Error in get_idea_performance: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/ideas/{idea_id}/description", response_model=DescriptionResponse)
def get_idea_description(idea_id: str, db: Session = Depends(get_db)):
    """
    Get the full description text for an idea.
    """
    try:
        description = db.query(Description).filter(Description.idea_id == idea_id).first()
        if not description:
            raise HTTPException(status_code=404, detail="Description not found")
        
        # Create a response that explicitly maps the fields
        response = DescriptionResponse(description=description.description)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        print(f"Error in get_idea_description: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/ideas/{idea_id}/catalysts", response_model=CatalystsResponse)
def get_idea_catalysts(idea_id: str, db: Session = Depends(get_db)):
    """
    Get the catalysts text for an idea.
    """
    try:
        catalysts = db.query(Catalysts).filter(Catalysts.idea_id == idea_id).first()
        if not catalysts:
            raise HTTPException(status_code=404, detail="Catalysts not found")
        
        # Create a response that explicitly maps the fields
        response = CatalystsResponse(catalysts=catalysts.catalysts)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        print(f"Error in get_idea_catalysts: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Debug endpoint for idea detail
@router.get("/debug/ideas/{idea_id}")
def debug_idea_detail(idea_id: str, db: Session = Depends(get_db)):
    """
    Simple debug endpoint to get an idea by ID.
    """
    try:
        idea = db.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        
        # Return just the idea data as a simple dict to test basic connectivity
        # Ensure date is properly converted to string (handles both datetime and date objects)
        idea_date = idea.date.isoformat() if hasattr(idea.date, 'isoformat') else str(idea.date)
        
        return {
            "id": idea.id,
            "link": idea.link or "",
            "company_id": idea.company_id,
            "user_id": idea.user_id,
            "date": idea_date,
            "is_short": idea.is_short,
            "is_contest_winner": idea.is_contest_winner
        }
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        print(f"Error in debug_idea_detail: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")