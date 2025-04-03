"""
Integration test for the Load More button functionality in IdeasPage.

This test specifically focuses on verifying that the backend API correctly handles
pagination requests that would come from the "Load More" button in the frontend.
"""
import pytest
from datetime import datetime, timedelta
import uuid
from fastapi import status

# Import models
from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from ValueInvestorsClub.ValueInvestorsClub.models.Company import Company
from ValueInvestorsClub.ValueInvestorsClub.models.User import User
from ValueInvestorsClub.ValueInvestorsClub.models.Performance import Performance

# Create a larger dataset for pagination testing
@pytest.fixture
def pagination_test_data(db_session):
    """Create a larger set of test data for pagination testing."""
    # Create company and user for test data
    company = Company(
        ticker="AAPL",
        company_name="Apple Inc."
    )
    
    user = User(
        username="TestUser",
        user_link="https://valueinvestorsclub.com/users/testuser"
    )
    
    db_session.add_all([company, user])
    db_session.commit()
    
    # Create 25 ideas to test pagination
    ideas = []
    performances = []
    now = datetime.now()
    
    for i in range(25):
        idea_id = str(uuid.uuid4())
        
        # Create idea with incremental dates
        idea = Idea(
            id=idea_id,
            link=f"https://valueinvestorsclub.com/ideas/{i}",
            company_id=company.ticker,
            user_id=user.user_link,
            date=now - timedelta(days=i),  # Newest first
            is_short=i % 2 == 0,  # Alternate between long and short
            is_contest_winner=i % 5 == 0  # Every 5th is a contest winner
        )
        
        # Create performance data for every idea
        performance = Performance(
            idea_id=idea_id,
            nextDayOpen=1.0 + (i * 0.01),
            nextDayClose=1.05 + (i * 0.01),
            oneWeekClosePerf=1.1 + (i * 0.02),
            twoWeekClosePerf=1.15 + (i * 0.02),
            oneMonthPerf=1.2 + (i * 0.03),
            threeMonthPerf=1.3 + (i * 0.03),
            sixMonthPerf=1.4 + (i * 0.04),
            oneYearPerf=1.5 + (i * 0.05),
            twoYearPerf=1.6 + (i * 0.05),
            threeYearPerf=1.7 + (i * 0.06),
            fiveYearPerf=1.8 + (i * 0.06)
        )
        
        ideas.append(idea)
        performances.append(performance)
    
    db_session.add_all(ideas + performances)
    db_session.commit()
    
    return {
        "company": company,
        "user": user,
        "ideas": ideas,
        "performances": performances
    }

def test_load_more_button_pagination(client, pagination_test_data):
    """
    Test the pagination functionality that would be used by the Load More button.
    
    This test simulates the API calls that would occur when:
    1. Initially loading the ideas page (skip=0, limit=X)
    2. Clicking the Load More button (skip=X, limit=X)
    """
    # Verify the initial total number of ideas
    response = client.get("/ideas/")
    assert response.status_code == status.HTTP_200_OK
    all_ideas = response.json()
    assert len(all_ideas) == 25
    
    # Test pagination with 10 items per page
    limit = 10
    
    # Get first page (first 10 ideas)
    response = client.get(f"/ideas/?skip=0&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    page1 = response.json()
    assert len(page1) == limit
    
    # Get second page (next 10 ideas) - simulates clicking "Load More"
    response = client.get(f"/ideas/?skip={limit}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    page2 = response.json()
    assert len(page2) == limit
    
    # Get third page (remaining 5 ideas) - simulates clicking "Load More" again
    response = client.get(f"/ideas/?skip={limit*2}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    page3 = response.json()
    assert len(page3) == 5  # Only 5 ideas remaining
    
    # Verify that all pages contain different ideas (no duplicates)
    page1_ids = [idea["id"] for idea in page1]
    page2_ids = [idea["id"] for idea in page2]
    page3_ids = [idea["id"] for idea in page3]
    
    # Check no overlap between pages
    assert len(set(page1_ids).intersection(set(page2_ids))) == 0
    assert len(set(page1_ids).intersection(set(page3_ids))) == 0
    assert len(set(page2_ids).intersection(set(page3_ids))) == 0
    
    # Check that the total number of ideas across all pages matches the total
    assert len(page1_ids) + len(page2_ids) + len(page3_ids) == 25
    
    # Verify order (by date desc is default)
    for i in range(len(page1) - 1):
        # Dates should be in descending order (newest first)
        assert datetime.fromisoformat(page1[i]["date"].replace('Z', '+00:00')) >= \
               datetime.fromisoformat(page1[i+1]["date"].replace('Z', '+00:00'))

def test_load_more_with_filters(client, pagination_test_data):
    """
    Test pagination with filters applied, simulating the "Load More" button
    when filters are active.
    """
    # Test with filter: is_short=true
    limit = 5
    
    # First page with filter
    response = client.get(f"/ideas/?is_short=true&skip=0&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    filtered_page1 = response.json()
    assert all(idea["is_short"] for idea in filtered_page1)
    
    # Load more with same filter
    response = client.get(f"/ideas/?is_short=true&skip={limit}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    filtered_page2 = response.json()
    assert all(idea["is_short"] for idea in filtered_page2)
    
    # Check no overlap between pages
    page1_ids = [idea["id"] for idea in filtered_page1]
    page2_ids = [idea["id"] for idea in filtered_page2]
    assert len(set(page1_ids).intersection(set(page2_ids))) == 0

def test_load_more_with_ordering(client, pagination_test_data):
    """
    Test pagination with different sort orders, simulating the "Load More" button
    with different sort options.
    """
    limit = 8
    
    # Test with performance sorting
    # First page
    response = client.get(f"/ideas/?sort_by=performance&performance_period=one_year_perf&sort_order=desc&skip=0&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    perf_page1 = response.json()
    assert len(perf_page1) == limit
    
    # Load more with same sort
    response = client.get(f"/ideas/?sort_by=performance&performance_period=one_year_perf&sort_order=desc&skip={limit}&limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    
    perf_page2 = response.json()
    
    # Check no overlap between pages
    page1_ids = [idea["id"] for idea in perf_page1]
    page2_ids = [idea["id"] for idea in perf_page2]
    assert len(set(page1_ids).intersection(set(page2_ids))) == 0
    
    # Test ordering of performance values
    # We need to get performance data for validation
    if len(perf_page1) > 1:
        # Get performance data for first two ideas to verify ordering
        idea1_id = perf_page1[0]["id"]
        idea2_id = perf_page1[1]["id"]
        
        perf1_response = client.get(f"/ideas/{idea1_id}/performance")
        perf2_response = client.get(f"/ideas/{idea2_id}/performance")
        
        if perf1_response.status_code == 200 and perf2_response.status_code == 200:
            perf1 = perf1_response.json()
            perf2 = perf2_response.json()
            
            # For desc ordering, first item should have higher or equal performance
            assert perf1["oneYearPerf"] >= perf2["oneYearPerf"]

def test_empty_results_for_pagination(client, pagination_test_data):
    """
    Test pagination behavior when there are no more results to load.
    This simulates clicking "Load More" when no more data is available.
    """
    # Get all ideas
    total_ideas = len(pagination_test_data["ideas"])
    
    # Request beyond the total number of ideas
    response = client.get(f"/ideas/?skip={total_ideas}&limit=10")
    assert response.status_code == status.HTTP_200_OK
    
    # Should return an empty list, not an error
    overflow_page = response.json()
    assert isinstance(overflow_page, list)
    assert len(overflow_page) == 0

def test_request_more_than_available(client, pagination_test_data):
    """
    Test requesting more items than are available.
    This simulates clicking "Load More" when fewer items remain than the limit.
    """
    # Get first 20 ideas
    response = client.get("/ideas/?skip=0&limit=20")
    assert response.status_code == status.HTTP_200_OK
    
    first_batch = response.json()
    assert len(first_batch) == 20
    
    # Request the remaining ideas (should be 5)
    response = client.get("/ideas/?skip=20&limit=10")  # Asking for 10, but only 5 remain
    assert response.status_code == status.HTTP_200_OK
    
    remaining = response.json()
    assert len(remaining) == 5  # Should only return the remaining 5
