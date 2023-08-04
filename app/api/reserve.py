from fastapi import APIRouter, Depends, Form
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.reserve import Reserve as ReserveModel
from ..models.room import Room as RoomModel
from ..models.place import Place as PlaceModel
from ..models.user import User as UserModel
from datetime import datetime, timedelta, timezone
from ..schemas.reserve import ReserveCheck as ReserveCheckModel
from ..schemas.reserve import ReserveAdd as ReserveAddModel
from .log import add_db_log
from .authentication import *
import json

router = APIRouter()


# 予約チェック
@router.post("/reserves/check")
def check_reserves(request: ReserveCheckModel, current_user: UserModel = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    # async_result2 = asyncio.run(get_current_user)
    # 時間を整形
    stime = datetime.strptime(request.start_time, '%Y-%m-%d %H:%M')
    etime = datetime.strptime(request.end_time, '%Y-%m-%d %H:%M')

    print(stime.time())
    print(etime.time())
    # 条件に合うトイレがあるか検索
    rooms = db.query(RoomModel). \
        filter(RoomModel.id == request.room_id,
               RoomModel.start_time < stime.time(),
               RoomModel.end_time > etime.time(), ).all()

    if len(rooms) == 0:
        return 0

    tz_jst = timezone(timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.now(tz_jst)
    # 現在時間より先の予約の有無
    reserves = db.query(ReserveModel). \
        filter(ReserveModel.room_id == request.room_id,
               ReserveModel.start_time > dt_aware4,
               ReserveModel.status == "reserve",
               ).all()

    if len(reserves) == 0:
        return 1
    else:
        return 0


# 予約追加
@router.post("/reserves/add")
def add_reserves(request: ReserveAddModel, current_user: UserModel = Depends(get_current_user),
                 db: Session = Depends(get_db),
                 ):
    if request.start_time and isinstance(request.start_time, str):
        start_time = datetime.strptime(request.start_time, "%Y-%m-%d %H:%M")

    if request.end_time and isinstance(request.end_time, str):
        end_time = datetime.strptime(request.end_time, "%Y-%m-%d %H:%M")

    tz_jst = timezone(timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.now(tz_jst)

    new_reserve = ReserveModel(
        place_id=request.place_id,
        room_id=request.room_id,
        user_id=current_user.id,
        start_time=start_time,
        end_time=end_time,
        status="reserve",
        created_at=dt_aware4,
        price=request.price
    )
    db.add(new_reserve)
    db.commit()
    db.refresh(new_reserve)
    # unlock("CB6EFE376844")
    add_db_log("add reserve")
    return 0


# 予約削除
@router.put("/reserves/{reserve_id}/cancel")
def remove_reserves(reserve_id: int, current_user: UserModel = Depends(get_current_user),
                    db: Session = Depends(get_db),
                    ):
    tz_jst = timezone(timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.now(tz_jst)

    reserve = db.query(ReserveModel). \
        filter(ReserveModel.id == reserve_id,
               ReserveModel.status == "reserve",
               ReserveModel.start_time > dt_aware4
               ).first()

    if reserve is None:
        return 0

    reserve.status = "cancel"
    db.commit()
    return 0


# ユーザーと予約情報取得
@router.get("/users/current")
def get_user_ifno(current_user: UserModel = Depends(get_current_user),
                  db: Session = Depends(get_db),
                  ):
    tz_jst = timezone(timedelta(hours=9))  # UTC とは9時間差
    dt_aware4 = datetime.now(tz_jst)

    reserve = db.query(ReserveModel). \
        filter(ReserveModel.user_id == current_user.id,
               ReserveModel.end_time > dt_aware4,
               ReserveModel.status == "reserve").first()

    roles = ["USER", ]
    if reserve is None:
        return {
            "user": {"user_id": current_user.id, "username": current_user.username, "email": current_user.email,
                     "roles": roles},
            "reserve": {None}
        }
    else:

        room = db.query(RoomModel). \
            filter(RoomModel.id == reserve.room_id,
                   ).first()
        place = db.query(PlaceModel). \
            filter(PlaceModel.id == reserve.place_id,
                   ).first()
        print(room.name)
        return {
            "user": {"id": current_user.id, "username": current_user.username, "email": current_user.email,
                     "roles": roles},
            "reserve": {"id": reserve.id, "start_time": reserve.start_time.strftime('%Y-%m-%d %H:%M'),
                        "end_time": reserve.end_time.strftime('%Y-%m-%d %H:%M'),
                        "price": reserve.price,
                        "room": {"id": room.id, "name": room.name, "device_status": room.device_status},
                        "place": {"id": place.id, "name": place.name}
                        }

        }


# 予約情報の取得
@router.get("/reserves")
def get_reserves(current_user: UserModel = Depends(get_current_user), response_model=List[ReserveModel],
                 db: Session = Depends(get_db),
                 ):
    reserves = db.query(ReserveModel). \
        filter(ReserveModel.user_id == current_user.id,
               ).all()

    strJson = "["
    for r in reserves:
        place = db.query(PlaceModel).filter(PlaceModel.id == r.place_id).first()
        room = db.query(RoomModel).filter(RoomModel.id == r.room_id).first()

        strJson += "{"
        strJson += ("\"id\": " + str(r.id) + ",")
        strJson += ("\"place_id\": " + str(r.place_id) + ",")
        strJson += ("\"place_name\": " + str(place.name) + ",")
        strJson += ("\"room_id\": " + str(r.room_id) + ",")
        strJson += ("\"room_name\": " + str(room.name) + ",")
        strJson += ("\"user_id\": " + str(r.user_id) + ",")
        stime = r.start_time.strftime('%Y-%m-%d %H:%M')
        etime = r.end_time.strftime('%Y-%m-%d %H:%M')
        strJson += ("\"start_time\": " + "\"" + stime + "\"" + ",")
        strJson += ("\"end_time\": " + "\"" + etime + "\"" + ",")
        strJson += ("\"status\": " + "\"" + str(r.status) + "\"" + ",")
        strJson += ("\"created_at\": " + "\"" + str(r.created_at) + "\"" + ",")
        strJson += ("\"price\": " + str(r.price))
        strJson += "},"
    strJson = strJson[:-1]
    strJson += "]"
    print("--------------------------------------------------------")
    print(strJson)
    
    student_json = json.loads(strJson)

    return student_json

