from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import pytz

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True, nullable=True, unique=True)
    password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('UTC')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('UTC')), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
