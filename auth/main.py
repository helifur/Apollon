import datetime
import logging
import os
import jwt
import grpc
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv

from models.user import User
from database.main_db import init
from database.redis_db import init_redis
from protobuf import auth_pb2, auth_pb2_grpc


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = init_redis()
SECRET_KEY = os.getenv("SECRET_KEY")
ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthRequest(BaseModel):
    username: str
    password: str


class SignupRequest(AuthRequest):
    name: str


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


async def create_token(data: dict, expires: datetime.timedelta):
    to_encode = data.copy()
    exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        seconds=expires.total_seconds()
    )
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALG)

    return token


def cache_refresh_token(token: str, username: str):
    return redis_client.setex(
        f"refresh_{username}", datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), token
    )


"""@app.post("/register")
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


@app.get("/checkredis")
async def checkredis():
    return redis_client.get("refresh_jakebro")


@app.post("/auth")
async def auth_user(request: AuthRequest):
    username = request.username
    password = request.password

    if not await authenticate_user(username, password):
        return {
            "status": status.HTTP_409_CONFLICT,
            "detail": "Invalid username or password!",
        }

    access_token = create_token(
        {"username": username}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"username": username}, datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    cache_refresh_token(refresh_token, username)  # redis cache

    response = JSONResponse(content={"status": status.HTTP_200_OK})
    response.set_cookie(key="access_token", value=access_token)

    return response"""


class AuthServicer(auth_pb2_grpc.AuthServicer):
    async def GetToken(self, request, context):
        username = request.username
        password = request.password

        if not await authenticate_user(username, password):
            return auth_pb2.AuthData(token=None)

        access_token = await create_token(
            {"username": username},
            datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = await create_token(
            {"username": username}, datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        cache_refresh_token(refresh_token, username)  # redis cache

        return auth_pb2.AuthData(token=access_token)


async def serve():
    await init()
    server = grpc.aio.server()

    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    server.add_insecure_port("[::]:50052")
    print("Server started at port 50052!")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.get_event_loop().run_until_complete(serve())
