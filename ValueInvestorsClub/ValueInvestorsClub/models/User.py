"""
The users for each user in the ValueInvestorsClub
"""
try:
    from ValueInvestorsClub.models.Base import Base
except ImportError:
    # This is a bit of an ugly mess but it enables the spider to work and the ipynb to work up a few dirs.
    from ValueInvestorsClub.ValueInvestorsClub.models.Base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(64))
    user_link: Mapped[str] = mapped_column(String(128), primary_key=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, userLink={self.user_link!r})"