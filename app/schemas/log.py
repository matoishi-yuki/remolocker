from datetime import time
from typing import Optional
from pydantic import BaseModel,Field
from datetime import date


class LogBase(BaseModel):
    id: Optional[int] = None
    message: str = Field(..., alias="mesage")
    created_at: date = None


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: Optional[int] = None  # この行を変更

    class Config:
        orm_mode = True
