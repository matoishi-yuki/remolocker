from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = "sqlite:///" + basedir+"/../remolocker.db"

# 引数 connect_args を追加して check_same_thread を False に設定
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
