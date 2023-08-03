from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..models.reserve import Reserve as ReserveModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..models.room import Room as RoomModel
from sqlalchemy.orm import sessionmaker
import datetime
from .switchbot import lock
import os
from ..database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/schedule")
def device_check():
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = "sqlite:///" + basedir + "/../remolocker.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()
    print("call_event")
    print(DATABASE_URL)
    reserves = db.query(ReserveModel).filter(ReserveModel.status == "reserve").all()

    tz_jst = datetime.timezone(datetime.timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.datetime.now(tz_jst).strftime("%Y-%m-%d %H:%M")
    print(dt_aware4)

    for r in reserves:
        print(r.end_time)
        if r.end_time.strftime("%Y-%m-%d %H:%M") < dt_aware4:
            room = db.query(RoomModel).filter(RoomModel.id == r.room_id).first()
            if room is not None:
                lock(room.device_id)
                print("lock")
                r.status = "end"
    db.commit()
    db.close()
    return {
        "debug": {"db": DATABASE_URL, "time": dt_aware4}
    }

