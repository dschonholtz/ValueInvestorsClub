"""
Routes for companies in the ValueInvestorsClub API.
"""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from api.database import get_db
from api.models import Company
from api.schemas import CompanyResponse

router = APIRouter()


@router.get("/companies/", response_model=List[CompanyResponse])
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