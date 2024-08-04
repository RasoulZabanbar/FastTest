from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base

import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
































