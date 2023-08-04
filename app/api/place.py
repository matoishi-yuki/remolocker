import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional, List
from ..models.place import Place
from ..models.room import Room as RoomModel
from ..schemas.room import Room
from sqlalchemy.orm import Session
from .authentication import *
from ..models.user import User as UserModel
router = APIRouter()

# Use environment variable if it exists, otherwise use the default path
MEDIA_PATH = os.environ.get("MEDIA_PATH", "media/building_photos")


@router.get("/admin/places")
def get_places(db: Session = Depends(get_db)):
    places = db.query(Place).all()
    return places


@router.get("/places")
def get_places(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    places = db.query(Place).all()
    return places


@router.post("/admin/places")
def create_places(
        name: str = Form(...),
        address: str = Form(...),
        photo: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
):
    # ... (the rest of the code remains the same)

    if photo:
        # Check if the directory exists, and create it if not
        if not os.path.exists(MEDIA_PATH):
            os.makedirs(MEDIA_PATH)

        photo_path = os.path.join(MEDIA_PATH, photo.filename)
        with open(photo_path, "wb") as f:
            f.write(photo.file.read())
    else:
        photo_path = None

    new_places = Place(
        name=name,
        address=address,
        photo=photo_path
    )
    db.add(new_places)
    db.commit()
    db.refresh(new_places)
    return new_places


@router.get("/places/{place_id}/rooms")
def get_places_rooms(place_id: int,
                          response_model=List[Room],
                          db: Session = Depends(get_db)):
    rooms = db.query(RoomModel).filter(RoomModel.place_id == place_id).all()
    return rooms
