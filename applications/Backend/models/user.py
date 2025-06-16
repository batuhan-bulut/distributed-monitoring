from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    __tablename__ = "users"  # this is the table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    
