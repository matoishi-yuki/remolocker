from sqlalchemy import Column, Integer, String, ForeignKey, Time,DateTime
from ..database.db import Base
from datetime import datetime
import pytz

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('UTC')))
