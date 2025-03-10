"""
Routes for users in the ValueInvestorsClub API.
"""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from api.database import get_db
from api.models import User
from api.schemas import UserResponse

router = APIRouter()


@router.get("/users/", response_model=List[UserResponse])
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