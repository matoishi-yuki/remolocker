from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas  # この行を変更

def get_toilets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Room).offset(skip).limit(limit).all()

# def get_toilet_by_name(db: Session, toilet_name: str):
#     return db.query(models.Toilet).filter(models.Toilet.toilet_name == toilet_name).first()
