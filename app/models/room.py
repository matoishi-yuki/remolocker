from sqlalchemy import Column, Integer, String, ForeignKey, Time
from ..database.db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, index=True)
    device_id = Column(String, index=True)
    name = Column(String, index=True)  # 名前を変更
    type = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    photo = Column(String)
    price = Column(Integer)
    device_status = Column(String)
    device_type = Column(String)
