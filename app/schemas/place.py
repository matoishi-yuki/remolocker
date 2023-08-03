from pydantic import BaseModel, Field

class PlaceBase(BaseModel):
    name: str = Field(..., alias="name")
    address: str = Field(..., alias="address")
    latitude: float
    longitude: float

class PlaceCreate(PlaceBase):
    photo: bytes = None

class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True
