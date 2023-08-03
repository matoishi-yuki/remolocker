print("main.py start ======================================== call")
import asyncio
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import user, room, authentication, place, reserve, log, schedule_event
from app.database import Base, engine
from app.api.admin import router as admin_router
from pathlib import Path
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
logging.basicConfig(level=logging.DEBUG)
# Load environment variables from .env file
env_path = basedir + "/../.env"
load_dotenv(dotenv_path=env_path)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/media", StaticFiles(directory="app/media"), name="media")
origins = [
    "http://localhost:3000",  # ReactアプリのURLを指定します
    "https://sorashiro.com",  # ReactアプリのURLを指定します
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router, prefix="/api", tags=["authentication"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(room.router, prefix="/api", tags=["room"])
app.include_router(schedule_event.router, prefix="/api", tags=["schedule"])
app.include_router(place.router, prefix="/api", tags=["place"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(reserve.router, prefix="/api", tags=["reserve"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
