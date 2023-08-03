from pydantic import BaseModel


class ReserveCheck(BaseModel):
    room_id: int
    start_time: str = None
    end_time: str = None


class ReserveAdd(BaseModel):
    place_id: int
    room_id: int
    start_time: str = None
    end_time: str = None
    price: int


