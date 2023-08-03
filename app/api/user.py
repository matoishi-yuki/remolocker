from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..schemas import user as user_schema
from ..models import user as user_model
from ..database import get_db
from .authentication import get_password_hash
from typing import List

router = APIRouter()


@router.get("/admin/users", response_model=List[user_schema.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users


@router.post("/admin/users", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(username=user.username, email=user.email, password=hashed_password, created_at=user.created_date)
    try:
        db.add(db_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user
