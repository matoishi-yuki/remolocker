from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Place, Room, User
from ..schemas import PlaceCreate, RoomCreate, UserCreate

router = APIRouter()

# 管理者用のビルディング、トイレ、ユーザーの取得・更新・削除のエンドポイントをここに追加します
