from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time

from ..schemas.room import Room, RoomCreate, KeyStatus
from ..models.room import Room as RoomModel

from ..models.reserve import Reserve as ReserveModel
from ..models.user import User as UserModel
from .switchbot import lock as switchbot_lock
from .switchbot import unlock as switchbot_unlock
from .sesame import lock as sesame_lock
from .sesame import unlock as sesame_unlock
from .authentication import *
router = APIRouter()

# Use environment variable if it exists, otherwise use the default path
MEDIA_PATH = os.environ.get("MEDIA_PATH", "media/toilet_photos")


@router.get("/admin/rooms", response_model=List[Room])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(RoomModel).all()
    return rooms


@router.get("/rooms", response_model=List[Room])
def get_rooms(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    rooms = db.query(RoomModel).all()
    return rooms



@router.post("/admin/rooms", response_model=Room)
def create_rooms(
    place_id: int = Form(...),
    device_id: str = Form(...),
    name: str = Form(...),
    type: str = Form(...),
    start_time: Optional[time] = Form(None),
    end_time: Optional[time] = Form(None),
    photo: Optional[UploadFile] = File(None),
    price: int = Form(...),
    device_type: int = Form(...),
    db: Session = Depends(get_db),
):

    if photo:
        # Check if the directory exists, and create it if not
        if not os.path.exists(MEDIA_PATH):
            os.makedirs(MEDIA_PATH)

        photo_path = os.path.join(MEDIA_PATH, photo.filename)
        with open(photo_path, "wb") as f:
            f.write(photo.file.read())
    else:
        photo_path = None

    if start_time and isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%H:%M").time()

    if end_time and isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%H:%M").time()

    new_room = RoomModel(
        place_id=place_id,
        device_id=device_id,
        name=name,
        type=type,
        start_time=start_time,
        end_time=end_time,
        photo=photo_path,
        price=price,
        device_status="lock",
        device_type=device_type
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# 施錠
@router.put("/rooms/{room_id}/lock")
def lock_key(room_id: int, reserve_id: KeyStatus, current_user: UserModel = Depends(get_current_user),
             db: Session = Depends(get_db),
             ):
    print("lock_key")
    reserve = db.query(ReserveModel).filter(ReserveModel.id == reserve_id.reserve_id,
                                            ReserveModel.user_id == current_user.id).first()

    if reserve is None:
        return None

    if reserve.status == "end" or reserve.status == "cancel":
        return None

    if reserve.room_id != room_id:
        return None

    room = db.query(RoomModel).filter(RoomModel.id == room_id).first()

    if room is None:
        return None

    if room.device_type == "sesame":
        sesame_lock(room.device_id)
    else:
        switchbot_lock(room.device_id)

    room.device_status = "lock"
    db.commit()

    return room


# 開錠
@router.put("/rooms/{room_id}/unlock")
def unlock_key(room_id: int, reserve_id: KeyStatus, current_user: UserModel = Depends(get_current_user),
               db: Session = Depends(get_db),
               ):
    print("unlock_key")
    reserve = db.query(ReserveModel).filter(ReserveModel.id == reserve_id.reserve_id,
                                            ReserveModel.user_id == current_user.id).first()

    if reserve is None:
        return None

    if reserve.status == "end" or reserve.status == "cancel":
        return None

    if reserve.room_id != room_id:
        return None

    room = db.query(RoomModel).filter(RoomModel.id == room_id).first()

    if room is None:
        return None

    if room.device_type == "sesame":
        sesame_unlock(room.device_id)
    else:
        switchbot_unlock(room.device_id)

    room.device_status = "unlock"
    db.commit()

    return room
