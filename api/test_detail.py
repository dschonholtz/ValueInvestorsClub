#!/usr/bin/env python3
"""
Diagnostic script to identify issues with specific API endpoints
"""
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

# Import models
import sys
import os
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from ValueInvestorsClub.ValueInvestorsClub.models.Company import Company
from ValueInvestorsClub.ValueInvestorsClub.models.Description import Description
from ValueInvestorsClub.ValueInvestorsClub.models.User import User
from ValueInvestorsClub.ValueInvestorsClub.models.Catalysts import Catalysts
from ValueInvestorsClub.ValueInvestorsClub.models.Performance import Performance

# Database connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/ideas"
engine = create_engine(DATABASE_URL)

def test_get_idea_detail(idea_id):
    """
    Test the functionality of the idea detail endpoint directly
    """
    try:
        with Session(engine) as db:
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
                print(f"Error: Idea with ID {idea_id} not found")
                return
            
            # Print raw idea data to check structure
            print(f"Idea: {idea!r}")
            print(f"Company: {idea.company!r}")
            print(f"User: {idea.user!r}")
            
            # Query related data
            description = db.query(Description).filter(Description.idea_id == idea_id).first()
            catalysts = db.query(Catalysts).filter(Catalysts.idea_id == idea_id).first()
            performance = db.query(Performance).filter(Performance.idea_id == idea_id).first()
            
            print(f"Description: {description!r}")
            print(f"Catalysts: {catalysts!r}")
            print(f"Performance: {performance!r}")
            
            # Try to construct response - this will help identify serialization issues
            try:
                print("Attempting to create a response dictionary manually:")
                response = {
                    "id": idea.id,
                    "link": idea.link,
                    "company_id": idea.company_id,
                    "user_id": idea.user_id,
                    "date": idea.date.isoformat(),
                    "is_short": idea.is_short,
                    "is_contest_winner": idea.is_contest_winner,
                    "company": {
                        "ticker": idea.company.ticker if idea.company else None,
                        "company_name": idea.company.company_name if idea.company else None
                    } if idea.company else None,
                    "user": {
                        "username": idea.user.username if idea.user else None,
                        "user_link": idea.user.user_link if idea.user else None
                    } if idea.user else None,
                    "description": {
                        "description": description.description
                    } if description else None,
                    "catalysts": {
                        "catalysts": catalysts.catalysts
                    } if catalysts else None,
                    "performance": {
                        "nextDayOpen": performance.nextDayOpen if performance else None,
                        "nextDayClose": performance.nextDayClose if performance else None,
                        # Add other performance fields as needed
                    } if performance else None
                }
                print("Successfully created response dictionary")
            except Exception as e:
                print(f"Error creating response dictionary: {e}")
                traceback.print_exc()
            
    except Exception as e:
        print(f"Error in test_get_idea_detail: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Use the same ID from the debug script
    test_get_idea_detail("97174981-391c-4a21-afb4-2efc7d89b56c")