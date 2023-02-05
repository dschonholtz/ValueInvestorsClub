"""
SQL Alchemy Base class that other sql alchemy classes will inherit from.
"""
from sqlalchemy.ext.declarative import DeclarativeBase


class Base(DeclarativeBase):
    pass