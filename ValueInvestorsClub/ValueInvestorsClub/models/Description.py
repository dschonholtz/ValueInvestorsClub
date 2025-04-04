"""
The description model is used to store the catalysts for a given idea.
It just has the id and the catalyst text.
"""
try:
    from ValueInvestorsClub.models.Base import Base
    from ValueInvestorsClub.models.Idea import Idea
except ImportError:
    # This is a bit of an ugly mess but it enables the spider to work and the ipynb to work up a few dirs.
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
    from ValueInvestorsClub.ValueInvestorsClub.models.Idea import Idea
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey

class Description(Base):
    __tablename__ = "descriptions"

    idea_id: Mapped[str] = mapped_column(ForeignKey(Idea.id), primary_key=True)
    description: Mapped[str] = mapped_column(String(128000))

    def __repr__(self) -> str:
        return f"Description(idea_id={self.idea_id!r}, description={self.description!r})"