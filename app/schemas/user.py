from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    password: str
    created_date: date

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None

    class Config:
        orm_mode = True
