"""
Pydantic models for request/response schemas for the ValueInvestorsClub API.
"""
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class PerformanceResponse(BaseModel):
    """Performance metrics for an investment idea."""
    # Base performance values
    nextDayOpen: Optional[float] = None
    nextDayClose: Optional[float] = None
    
    # Traditional performance metrics
    oneWeekClosePerf: Optional[float] = None
    twoWeekClosePerf: Optional[float] = None
    oneMonthPerf: Optional[float] = None
    threeMonthPerf: Optional[float] = None
    sixMonthPerf: Optional[float] = None
    oneYearPerf: Optional[float] = None
    twoYearPerf: Optional[float] = None
    threeYearPerf: Optional[float] = None
    fiveYearPerf: Optional[float] = None
    
    # Timeline data for each performance period
    # These could be used to create time-series visualizations
    timeline_labels: Optional[List[str]] = None
    timeline_values: Optional[List[float]] = None
    
    # Performance breakdown by time period with normalized values
    # Useful for comparing across different time periods
    performance_periods: Optional[Dict[str, float]] = None

    model_config = {"from_attributes": True}


class DescriptionResponse(BaseModel):
    """Description of an investment idea."""
    description: str

    model_config = {"from_attributes": True}


class CatalystsResponse(BaseModel):
    """Catalysts for an investment idea."""
    catalysts: str

    model_config = {"from_attributes": True}


class CompanyResponse(BaseModel):
    """Company information."""
    ticker: str
    company_name: str

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    """User information."""
    username: str
    user_link: str

    model_config = {"from_attributes": True}


class IdeaResponse(BaseModel):
    """Basic information about an investment idea."""
    id: str
    link: Optional[str] = ""  # Make link optional with default empty string
    company_id: str
    user_id: str
    date: datetime
    is_short: bool
    is_contest_winner: bool

    model_config = {"from_attributes": True}


class IdeaDetailResponse(IdeaResponse):
    """Detailed information about an investment idea, including related data."""
    company: Optional[CompanyResponse] = None
    user: Optional[UserResponse] = None
    description: Optional[DescriptionResponse] = None
    catalysts: Optional[CatalystsResponse] = None
    performance: Optional[PerformanceResponse] = None

    model_config = {"from_attributes": True}