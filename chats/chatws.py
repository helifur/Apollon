import datetime
import socketio
import jwt
import os
import uvicorn
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
socket_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)


@sio.event
async def connect(sid, environ):
    for i in range(10):
        print("connect ", sid)

    await sio.emit("join_room")


@sio.event
def disconnect(sid):
    for i in range(10):
        print("disconnect ", sid)


@sio.event
async def join_room(sid, data):
    chatId = data["chatId"]
    username = jwt.decode(
        data["userToken"], key=os.getenv("SECRET_KEY"), algorithms="HS256"
    )["username"]

    await sio.enter_room(sid, room=chatId)

    candidates = await Message.find({"chatId": chatId}).to_list()
    messages = []

    for elem in candidates:
        messages.append(
            {
                "time": elem.time.strftime("%Y-%m-%d %H:%M:%S"),
                "text": elem.text,
                "amISender": True if elem.senderUsername == username else False,
            }
        )

    await sio.emit("update_messages", messages, to=sid)


@sio.event
async def message(sid, data):
    username = jwt.decode(
        data["access_token"], key=os.getenv("SECRET_KEY"), algorithms="HS256"
    )

    print("RECEIVED SID:", sid)
    time = datetime.datetime.now()

    candidate = Message(
        chatId=data["chatId"],
        senderUsername=username["username"],
        text=data["text"],
        time=time,
    )

    await candidate.insert()
    print("OK")

    print(
        "People in room:",
    )

    await sio.send(
        {
            "text": data["text"],
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": True,
        },
        room=data["chatId"],
    )


if __name__ == "__main__":
    uvicorn.run(socket_app)
