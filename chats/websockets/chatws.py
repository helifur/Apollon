import datetime
import socketio
import jwt
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI


from chats.database.database import init
from chats.models.message import Message


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

sio = socketio.AsyncServer(
    cors_allowed_origins=origins,
    async_mode="asgi",
    logger=True,
    engineio_logger=True,
)
app = FastAPI(lifespan=lifespan)
socket_app = socketio.ASGIApp(sio)

app.mount("/", socket_app)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


@sio.event
async def fetch_messages(sid, data):
    print(data)
    chatId = data["chatId"]

    candidates = await Message.find({"chatId": chatId}).to_list()
    messages = []

    for elem in candidates:
        messages.append(
            {"time": elem.time.strftime("%Y-%m-%d %H:%M:%S"), "text": elem.text}
        )

    print(messages)

    await sio.emit("fetch_messages", {"status": 200, "data": messages}, to=sid)


@sio.event
async def message(sid, data):
    username = jwt.decode(
        data["access_token"], key=os.getenv("SECRET_KEY"), algorithms="HS256"
    )

    print(username)
    time = datetime.datetime.now()

    candidate = Message(
        chatId=data["chatId"],
        senderUsername=username["username"],
        text=data["text"],
        time=time,
    )

    await candidate.insert()
    print("OK")

    return {"text": data["text"], "time": time.strftime("%Y-%m-%d %H:%M:%S")}
