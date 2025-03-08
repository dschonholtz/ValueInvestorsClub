#!/usr/bin/env python3
"""
Test script for the idea detail endpoint with detailed diagnostics
"""
import sys
import os
import traceback
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

# Import models
from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from ValueInvestorsClub.ValueInvestorsClub.models.Company import Company
from ValueInvestorsClub.ValueInvestorsClub.models.Description import Description
from ValueInvestorsClub.ValueInvestorsClub.models.User import User
from ValueInvestorsClub.ValueInvestorsClub.models.Catalysts import Catalysts
from ValueInvestorsClub.ValueInvestorsClub.models.Performance import Performance

# Define manually what we expect our Pydantic models to look like
class CompanyResponse(BaseModel):
    ticker: str
    company_name: str
    
    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    username: str
    user_link: str
    
    model_config = {"from_attributes": True}

class DescriptionResponse(BaseModel):
    description: str
    
    model_config = {"from_attributes": True}

class CatalystsResponse(BaseModel):
    catalysts: str
    
    model_config = {"from_attributes": True}

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

class IdeaResponse(BaseModel):
    id: str
    link: str
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

# Database connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/ideas"
engine = create_engine(DATABASE_URL)

def get_idea_detail(idea_id):
    """
    Replicate the functionality of the idea detail endpoint directly
    """
    try:
        with Session(engine) as db:
            # Query idea with eager loading of related objects
            print(f"Step 1: Querying for idea with ID {idea_id}")
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
                print(f"Error: Idea with ID {idea_id} not found")
                return
            
            print(f"Step 2: Successfully found idea: {idea!r}")
            print(f"Company: {idea.company!r}")
            print(f"User: {idea.user!r}")
            
            # Query related data
            print("Step 3: Querying related data")
            description = db.query(Description).filter(Description.idea_id == idea_id).first()
            print(f"Description: {description!r}")
            
            catalysts = db.query(Catalysts).filter(Catalysts.idea_id == idea_id).first()
            print(f"Catalysts: {catalysts!r}")
            
            # You might need to try/except this if it's failing
            print("Step 4: Querying performance data")
            try:
                performance = db.query(Performance).filter(Performance.idea_id == idea_id).first()
                print(f"Performance: {performance!r}")
            except Exception as e:
                print(f"Error querying performance: {e}")
                print(traceback.format_exc())
                performance = None
            
            # Try to manually validate each model first
            print("Step 5: Validating individual models")
            try:
                company_model = CompanyResponse.model_validate(idea.company) if idea.company else None
                print(f"Company model validation successful: {company_model}")
            except Exception as e:
                print(f"Error validating company model: {e}")
                print(traceback.format_exc())
                
            try:
                user_model = UserResponse.model_validate(idea.user) if idea.user else None
                print(f"User model validation successful: {user_model}")
            except Exception as e:
                print(f"Error validating user model: {e}")
                print(traceback.format_exc())
                
            try:
                description_model = DescriptionResponse.model_validate(description) if description else None
                print(f"Description model validation successful: {description_model}")
            except Exception as e:
                print(f"Error validating description model: {e}")
                print(traceback.format_exc())
                
            try:
                catalysts_model = CatalystsResponse.model_validate(catalysts) if catalysts else None
                print(f"Catalysts model validation successful: {catalysts_model}")
            except Exception as e:
                print(f"Error validating catalysts model: {e}")
                print(traceback.format_exc())
                
            try:
                performance_model = PerformanceResponse.model_validate(performance) if performance else None
                print(f"Performance model validation successful: {performance_model}")
            except Exception as e:
                print(f"Error validating performance model: {e}")
                print(traceback.format_exc())
            
            # Now try to construct the full response
            print("Step 6: Building complete response")
            try:
                idea_model = IdeaResponse.model_validate(idea)
                print(f"Idea model validation successful: {idea_model}")
            except Exception as e:
                print(f"Error validating idea model: {e}")
                print(traceback.format_exc())
                return
            
            try:
                # Convert idea to full detail response
                result = IdeaDetailResponse.model_validate(idea)
                print(f"Base IdeaDetailResponse validation successful: {result}")
                
                # Manually attach related objects that were already validated
                if description and description_model:
                    result.description = description_model
                if catalysts and catalysts_model:
                    result.catalysts = catalysts_model
                if performance and performance_model:
                    result.performance = performance_model
                
                print("Final response constructed successfully:")
                print_model(result)
                return result
            except Exception as e:
                print(f"Error building final response: {e}")
                print(traceback.format_exc())
            
    except Exception as e:
        print(f"Unhandled error in get_idea_detail: {e}")
        print(traceback.format_exc())

def print_model(model):
    """Recursively print a pydantic model as a dict"""
    if not model:
        print("None")
        return
    
    # Get dictionary representation
    model_dict = model.model_dump()
    
    # Pretty print nested dictionary
    def pretty_print_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key}:")
                pretty_print_dict(value, indent + 2)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                print(" " * indent + f"{key}:")
                for item in value:
                    pretty_print_dict(item, indent + 2)
            else:
                print(" " * indent + f"{key}: {value}")
    
    pretty_print_dict(model_dict)

if __name__ == "__main__":
    # Use the same ID from the debug script
    if len(sys.argv) > 1:
        idea_id = sys.argv[1]
    else:
        idea_id = "97174981-391c-4a21-afb4-2efc7d89b56c"  # Default test ID
    
    print(f"Testing get_idea_detail with ID: {idea_id}")
    result = get_idea_detail(idea_id)