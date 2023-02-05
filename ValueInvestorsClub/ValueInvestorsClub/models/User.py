"""
The users for each user in the ValueInvestorsClub
"""
from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    userLink: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, userLink={self.userLink!r})"