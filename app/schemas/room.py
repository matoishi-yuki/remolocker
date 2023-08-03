from datetime import time
from typing import Optional
from pydantic import BaseModel


class RoomBase(BaseModel):
    place_id: int
    device_id: str
    gender: str
    name: str
    type: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    photo: Optional[str] = None
    price: int
    device_status: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: Optional[int] = None  # この行を変更

    class Config:
        orm_mode = True


class KeyStatus(BaseModel):
    reserve_id: int
