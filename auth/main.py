import datetime
import os
import jwt
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv

from auth.models.user import User
from auth.database.database import init


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield  # Здесь приложение запускается


app = FastAPI(lifespan=lifespan)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3


def get_current_user():
    pass


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username) -> User | None:
    return await User.find(User.username == username).first_or_none()


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return True


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALG)

    return token


class AuthRequest(BaseModel):
    username: str
    password: str


class SignupRequest(AuthRequest):
    name: str


@app.post("/register")
async def reg_user(request: SignupRequest):
    name = request.name
    username = request.username
    password = request.password

    if await get_user(username):
        return {"status": status.HTTP_409_CONFLICT, "detail": "Username already taken!"}

    password = get_password_hash(password)

    candidate = User(name=name, username=username, hashed_password=password, desc="")

    await candidate.insert()

    return {"status": status.HTTP_200_OK}


@app.post("/auth")
async def auth_user(request: AuthRequest):
    username = request.username
    password = request.password

    if not await authenticate_user(username, password):
        return {
            "status": status.HTTP_409_CONFLICT,
            "detail": "Invalid username or password!",
        }

    token = create_access_token({"username": username})

    return token
