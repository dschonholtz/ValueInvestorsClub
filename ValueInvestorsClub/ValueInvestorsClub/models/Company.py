"""
The company sql alchemy base class
"""
try:
    from ValueInvestorsClub.models.Base import Base
except ImportError:
    # This is a bit of an ugly mess but it enables the spider to work and the ipynb to work up a few dirs.
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Company(Base):
    __tablename__ = "companies"
    ticker: Mapped[str] = mapped_column(String(32), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(128))

    def __repr__(self) -> str:
        return f"id(id={self.id!r}, ticker={self.ticker!r}, companyName={self.company_name!r})"