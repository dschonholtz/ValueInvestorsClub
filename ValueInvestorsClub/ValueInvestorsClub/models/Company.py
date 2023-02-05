"""
The company sql alchemy base class
"""

from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Company(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(8))
    companyName: Mapped[str] = mapped_column(String(32))

    def __repr__(self) -> str:
        return f"id(id={self.id!r}, ticker={self.ticker!r}, companyName={self.companyName!r})"