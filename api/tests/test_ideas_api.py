"""
Integration tests for the ideas API endpoints.

These tests verify that the API endpoints work correctly with the query parameters
that the frontend will use, ensuring contract compatibility.
"""
import pytest
from datetime import datetime, timedelta
import uuid
from fastapi import status

# Import models
from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from ValueInvestorsClub.ValueInvestorsClub.models.Company import Company
from ValueInvestorsClub.ValueInvestorsClub.models.User import User
from ValueInvestorsClub.ValueInvestorsClub.models.Description import Description
from ValueInvestorsClub.ValueInvestorsClub.models.Catalysts import Catalysts
from ValueInvestorsClub.ValueInvestorsClub.models.Performance import Performance

# Create test data
@pytest.fixture
def test_data(db_session):
    """Create test data for ideas API tests."""
    # Create companies
    company1 = Company(
        ticker="AAPL",
        company_name="Apple Inc."
    )
    company2 = Company(
        ticker="MSFT",
        company_name="Microsoft Corporation"
    )
    
    # Create users
    user1 = User(
        username="TestUser1",
        user_link="https://valueinvestorsclub.com/users/testuser1"
    )
    user2 = User(
        username="TestUser2",
        user_link="https://valueinvestorsclub.com/users/testuser2"
    )
    
    db_session.add_all([company1, company2, user1, user2])
    db_session.commit()
    
    # Create ideas
    now = datetime.now()
    idea1_id = str(uuid.uuid4())
    idea2_id = str(uuid.uuid4())
    idea3_id = str(uuid.uuid4())
    
    idea1 = Idea(
        id=idea1_id,
        link="https://valueinvestorsclub.com/ideas/1",
        company_id=company1.ticker,  # Use ticker as FK
        user_id=user1.user_link,    # Use user_link as FK
        date=now,
        is_short=False,
        is_contest_winner=True
    )
    
    idea2 = Idea(
        id=idea2_id,
        link="https://valueinvestorsclub.com/ideas/2",
        company_id=company2.ticker,  # Use ticker as FK
        user_id=user1.user_link,    # Use user_link as FK
        date=now - timedelta(days=30),
        is_short=True,
        is_contest_winner=False
    )
    
    idea3 = Idea(
        id=idea3_id,
        link="https://valueinvestorsclub.com/ideas/3",
        company_id=company1.ticker,  # Use ticker as FK
        user_id=user2.user_link,    # Use user_link as FK
        date=now - timedelta(days=60),
        is_short=False,
        is_contest_winner=False
    )
    
    db_session.add_all([idea1, idea2, idea3])
    db_session.commit()
    
    # Create descriptions, catalysts, and performance
    description1 = Description(
        idea_id=idea1_id,
        description="Test description for idea 1"
    )
    
    description2 = Description(
        idea_id=idea2_id,
        description="Test description for idea 2"
    )
    
    description3 = Description(
        idea_id=idea3_id,
        description="Test description for idea 3"
    )
    
    catalysts1 = Catalysts(
        idea_id=idea1_id,
        catalysts="Test catalysts for idea 1"
    )
    
    catalysts2 = Catalysts(
        idea_id=idea2_id,
        catalysts="Test catalysts for idea 2"
    )
    
    performance1 = Performance(
        idea_id=idea1_id,
        nextDayOpen=1.0,
        nextDayClose=1.05,
        oneWeekClosePerf=1.1,
        twoWeekClosePerf=1.15,
        oneMonthPerf=1.2,
        threeMonthPerf=1.3,
        sixMonthPerf=1.4,
        oneYearPerf=1.5,
        twoYearPerf=1.6,
        threeYearPerf=1.7,
        fiveYearPerf=1.8
    )
    
    db_session.add_all([
        description1, description2, description3,
        catalysts1, catalysts2, performance1
    ])
    db_session.commit()
    
    return {
        "companies": [company1, company2],
        "users": [user1, user2],
        "ideas": [idea1, idea2, idea3],
        "descriptions": [description1, description2, description3],
        "catalysts": [catalysts1, catalysts2],
        "performances": [performance1]
    }

# Test cases
def test_get_ideas_basic(client, test_data):
    """Test basic retrieval of ideas."""
    response = client.get("/ideas/")
    assert response.status_code == status.HTTP_200_OK
    
    ideas = response.json()
    assert len(ideas) == 3
    
    # Check that all ideas are returned with the right fields
    for idea in ideas:
        assert "id" in idea
        assert "link" in idea
        assert "company_id" in idea
        assert "user_id" in idea
        assert "date" in idea
        assert "is_short" in idea
        assert "is_contest_winner" in idea

def test_get_ideas_with_company_filter(client, test_data):
    """Test filtering ideas by company_id matching frontend request."""
    company_ticker = test_data["companies"][0].ticker  # Use ticker as company_id
    response = client.get(f"/ideas/?company_id={company_ticker}")
    assert response.status_code == status.HTTP_200_OK
    
    ideas = response.json()
    assert len(ideas) == 2
    
    # All returned ideas should have the specified company_id
    for idea in ideas:
        assert idea["company_id"] == company_ticker

def test_get_ideas_with_user_filter(client, test_data):
    """Test filtering ideas by user_id matching frontend request."""
    user_link = test_data["users"][0].user_link  # Use user_link as user_id
    response = client.get(f"/ideas/?user_id={user_link}")
    assert response.status_code == status.HTTP_200_OK
    
    ideas = response.json()
    assert len(ideas) == 2
    
    # All returned ideas should have the specified user_id
    for idea in ideas:
        assert idea["user_id"] == user_link

def test_get_ideas_with_short_filter(client, test_data):
    """Test filtering ideas by is_short matching frontend request."""
    response = client.get("/ideas/?is_short=true")
    assert response.status_code == status.HTTP_200_OK
    
    ideas = response.json()
    assert len(ideas) == 1
    
    # All returned ideas should be shorts
    for idea in ideas:
        assert idea["is_short"] is True

def test_get_ideas_with_contest_winner_filter(client, test_data):
    """Test filtering ideas by is_contest_winner matching frontend request."""
    response = client.get("/ideas/?is_contest_winner=true")
    assert response.status_code == status.HTTP_200_OK
    
    ideas = response.json()
    assert len(ideas) == 1
    
    # All returned ideas should be contest winners
    for idea in ideas:
        assert idea["is_contest_winner"] is True

def test_get_ideas_with_pagination(client, test_data):
    """Test ideas pagination matching frontend request."""
    # Get first page (2 ideas)
    response = client.get("/ideas/?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    
    page1 = response.json()
    assert len(page1) == 2
    
    # Get second page (1 idea)
    response = client.get("/ideas/?skip=2&limit=2")
    assert response.status_code == status.HTTP_200_OK
    
    page2 = response.json()
    assert len(page2) == 1
    
    # Make sure the ideas are different
    page1_ids = [idea["id"] for idea in page1]
    page2_ids = [idea["id"] for idea in page2]
    assert len(set(page1_ids).intersection(set(page2_ids))) == 0

def test_get_idea_detail(client, test_data):
    """Test retrieving detailed idea information."""
    idea_id = test_data["ideas"][0].id
    response = client.get(f"/ideas/{idea_id}")
    assert response.status_code == status.HTTP_200_OK
    
    idea = response.json()
    
    # Check all expected fields in detail response
    assert idea["id"] == idea_id
    assert "company" in idea
    assert "user" in idea
    assert "description" in idea
    assert "catalysts" in idea
    assert "performance" in idea
    
    # Check nested fields
    assert idea["company"]["ticker"] == "AAPL"
    assert idea["company"]["company_name"] == "Apple Inc."
    assert idea["user"]["username"] == "TestUser1"
    assert idea["description"]["description"] == "Test description for idea 1"
    assert idea["catalysts"]["catalysts"] == "Test catalysts for idea 1"
    assert idea["performance"]["oneMonthPerf"] == 1.2

def test_get_idea_detail_not_found(client):
    """Test 404 error for non-existent idea."""
    response = client.get(f"/ideas/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_idea_performance(client, test_data):
    """Test retrieving idea performance data."""
    idea_id = test_data["ideas"][0].id
    response = client.get(f"/ideas/{idea_id}/performance")
    assert response.status_code == status.HTTP_200_OK
    
    performance = response.json()
    
    # Check all performance fields
    assert performance["nextDayOpen"] == 1.0
    assert performance["nextDayClose"] == 1.05
    assert performance["oneWeekClosePerf"] == 1.1
    assert performance["twoWeekClosePerf"] == 1.15
    assert performance["oneMonthPerf"] == 1.2
    assert performance["threeMonthPerf"] == 1.3
    assert performance["sixMonthPerf"] == 1.4
    assert performance["oneYearPerf"] == 1.5
    assert performance["twoYearPerf"] == 1.6
    assert performance["threeYearPerf"] == 1.7
    assert performance["fiveYearPerf"] == 1.8

def test_get_companies(client, test_data):
    """Test retrieving companies."""
    response = client.get("/companies/")
    assert response.status_code == status.HTTP_200_OK
    
    companies = response.json()
    assert len(companies) == 2
    
    # Check company data
    tickers = [company["ticker"] for company in companies]
    assert "AAPL" in tickers
    assert "MSFT" in tickers

def test_get_companies_with_search(client, test_data):
    """Test searching companies matching frontend search feature."""
    response = client.get("/companies/?search=App")
    assert response.status_code == status.HTTP_200_OK
    
    companies = response.json()
    assert len(companies) == 1
    assert companies[0]["ticker"] == "AAPL"
    assert companies[0]["company_name"] == "Apple Inc."

def test_get_users(client, test_data):
    """Test retrieving users."""
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    
    users = response.json()
    assert len(users) == 2
    
    # Check user data
    usernames = [user["username"] for user in users]
    assert "TestUser1" in usernames
    assert "TestUser2" in usernames

def test_get_users_with_search(client, test_data):
    """Test searching users matching frontend search feature."""
    response = client.get("/users/?search=User1")
    assert response.status_code == status.HTTP_200_OK
    
    users = response.json()
    assert len(users) == 1
    assert users[0]["username"] == "TestUser1"