from sqlalchemy import Column, Integer, String, ForeignKey, Time, DateTime
from ..database.db import Base
from datetime import datetime
import pytz


class Reserve(Base):
    __tablename__ = "reserves"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, index=True)
    room_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('UTC')))
    end_time = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('UTC')))
    status = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('UTC')))
    price = Column(Integer)

