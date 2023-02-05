"""
The catalyst model is used to store the catalysts for a given idea.
It just has the id and the catalyst text.
"""

from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Catalyst(Base):
    __tablename__ = "catalyst"

    id: Mapped[int] = mapped_column(primary_key=True)
    catalyst: Mapped[str] = mapped_column(String(2048))

    def __repr__(self) -> str:
        return f"Catalyst(id={self.id!r}, catalyst={self.catalyst!r})"