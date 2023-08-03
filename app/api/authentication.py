from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..database import get_db
from ..models import user as user_model
from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_user(db, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        print("get_current_user")
        print(token)

        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
        email: str = payload.get("sub")
        print(email)

        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials1")
        user = get_user(db, email=email)
        print(user.password)
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials2")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials3")
    return user



class Token(BaseModel):
    access_token: str
    token_type: str



class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    print(request.username)
    print(request.password)

    user = await authenticate_user(db, request.username, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    expires = datetime.utcnow() + timedelta(hours=1)
    token_data = {
        "sub": user.email,
        "exp": expires,
    }
    roles = ["USER", ]

    token = jwt.encode(token_data, os.environ["SECRET_KEY"], algorithm="HS256")
    return {"access_token": token, "token_type": "bearer",
            "user": {"user_id": user.id, "username": user.username, "email": user.email, "roles": roles},
            }
