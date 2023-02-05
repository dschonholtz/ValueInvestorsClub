from sqlalchemy import ForeignKey
from sqlalchemy import DateTime, Boolean, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ValueInvestorsClub.models.Base import Base

class Idea(Base):
    __tablename__ = "idea"

    id: Mapped[int] = mapped_column(primary_key=True)
    companyId: Mapped[int] = mapped_column(ForeignKey("company.id"))
    descriptionId: Mapped[int] = mapped_column(ForeignKey("description.id"))
    catalystId: Mapped[int] = mapped_column(ForeignKey("catalyst.id"))
    userId: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    date: Mapped[str] = mapped_column(DateTime)
    isShort : Mapped[bool] = mapped_column(Boolean)
    isContestWinner : Mapped[bool] = mapped_column(Boolean)
    price: Mapped[float] = mapped_column(Float)
    price1Mo: Mapped[float] = mapped_column(Float)
    price3Mo: Mapped[float] = mapped_column(Float)
    price6Mo: Mapped[float] = mapped_column(Float)
    price1Yr: Mapped[float] = mapped_column(Float)
    price2Yr: Mapped[float] = mapped_column(Float)
    price3Yr: Mapped[float] = mapped_column(Float)
    price5Yr: Mapped[float] = mapped_column(Float)


    def __repr__(self) -> str:
        return f"Idea(id={self.id!r}, companyId={self.companyId!r}, descriptionId={self.descriptionId!r}, catalystId={self.catalystId!r}, userId={self.userId!r}, date={self.date!r}, isShort={self.isShort!r}, isContestWinner={self.isContestWinner!r}, price={self.price!r}, price1Mo={self.price1Mo!r}, price3Mo={self.price3Mo!r}, price6Mo={self.price6Mo!r}, price1Yr={self.price1Yr!r}, price2Yr={self.price2Yr!r}, price3Yr={self.price3Yr!r}, price5Yr={self.price5Yr!r})"

