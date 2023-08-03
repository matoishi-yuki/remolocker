from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from ..models.log import Log as LogModel
import datetime
import os


#depend fast apiでないと使えない
def add_db_log(message: str):
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.datetime.now(tz_jst)


    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = "sqlite:///" + basedir + "/../remolocker.db"
    # 引数 connect_args を追加して check_same_thread を False に設定
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    new_log = LogModel(
        message=message,
        created_at=dt_aware4
    )
    db.add(new_log)
    db.commit()
    db.close()
