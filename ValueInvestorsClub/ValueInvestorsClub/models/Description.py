"""
The description model is used to store the catalysts for a given idea.
It just has the id and the catalyst text.
"""

from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Description(Base):
    __tablename__ = "description"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(32767))

    def __repr__(self) -> str:
        return f"Description(id={self.id!r}, catalyst={self.description!r})"