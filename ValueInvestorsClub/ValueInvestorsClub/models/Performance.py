"""
A sql alchemy table for storing pricing information
"""
try:
    from ValueInvestorsClub.models.Base import Base
except ImportError:
    # This is a bit of an ugly mess but it enables the spider to work and the ipynb to work up a few dirs.
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey


class Performance(Base):
    __tablename__ = "performance"
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), primary_key=True)
    # sameDayOpen: Mapped[float] = mapped_column(Float)
    # sameDayClose: Mapped[float] = mapped_column(Float)
    nextDayOpen: Mapped[float] = mapped_column(Float)
    nextDayClose: Mapped[float] = mapped_column(Float)
    # perf metrics are percentage changes from nextDayClose
    oneWeekClosePerf: Mapped[float] = mapped_column(Float, nullable=True)
    twoWeekClosePerf: Mapped[float] = mapped_column(Float, nullable=True)
    oneMonthPerf: Mapped[float] = mapped_column(Float, nullable=True)
    threeMonthPerf: Mapped[float] = mapped_column(Float, nullable=True)
    sixMonthPerf: Mapped[float] = mapped_column(Float, nullable=True)
    oneYearPerf: Mapped[float] = mapped_column(Float, nullable=True)
    twoYearPerf: Mapped[float] = mapped_column(Float, nullable=True)
    threeYearPerf: Mapped[float] = mapped_column(Float, nullable=True)
    fiveYearPerf: Mapped[float] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return (f"Performance(idea_id={self.idea_id!r}, "
            f"nextDayOpen={self.nextDayOpen!r}, "
            f"nextDayClose={self.nextDayClose!r}, "
            f"oneWeekClosePerf={self.oneWeekClosePerf!r}, "
            f"twoWeekClosePerf={self.twoWeekClosePerf!r}, "
            f"oneMonthPerf={self.oneMonthPerf!r}, "
            f"threeMonthPerf={self.threeMonthPerf!r}, "
            f"sixMonthPerf={self.sixMonthPerf!r}, "
            f"oneYearPerf={self.oneYearPerf!r}, "
            f"twoYearPerf={self.twoYearPerf!r}, "
            f"threeYearPerf={self.threeYearPerf!r}, "
            f"fiveYearPerf={self.fiveYearPerf!r})"
            )