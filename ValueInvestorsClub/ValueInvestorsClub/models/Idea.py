from sqlalchemy import ForeignKey
from sqlalchemy import DateTime, Boolean, Float, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

try:
    from ValueInvestorsClub.models.Base import Base
except ImportError:
    # This is a bit of an ugly mess but it enables the spider to work and the ipynb to work up a few dirs.
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base

class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(256))
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.ticker"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_link"))
    date: Mapped[DateTime] = mapped_column(DateTime)
    is_short : Mapped[bool] = mapped_column(Boolean)
    is_contest_winner : Mapped[bool] = mapped_column(Boolean)
    
    # Relationships
    company = relationship("Company", backref="ideas")
    user = relationship("User", backref="ideas")
    description = relationship("Description", uselist=False, backref="idea")
    catalysts = relationship("Catalysts", uselist=False, backref="idea")
    performance = relationship("Performance", uselist=False, backref="idea")


    def __repr__(self) -> str:
        return (f"Idea(id={self.id!r}, "
            f"companyId={self.company_id!r}, "
            f"link={self.link!r},"
            f"userId={self.user_id!r}, "
            f"date={self.date!r}, "
            f"isShort={self.is_short!r}, "
            f"isContestWinner={self.is_contest_winner!r})")

