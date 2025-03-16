from json import load
import os
from fastapi import FastAPI, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import RequestBody
from pydantic import BaseModel
from typing import Annotated
from dotenv import load_dotenv
import grpc
import jwt

import protobuf.chats_pb2_grpc as chats_pb2_grpc
import protobuf.chats_pb2 as chats_pb2
from routes.auth import router


app = FastAPI()
app.include_router(router)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


class CreateChatRequest(BaseModel):
    firstUserId: str
    secondUserId: str


@app.post("/create_chat")
async def create_chat(request: CreateChatRequest):
    with grpc.insecure_channel("localhost:50051") as channel:
        client = chats_pb2_grpc.ChatsStub(channel)
        response = client.CreateChat(
            chats_pb2.MultipleUsers(
                firstUserId=request.firstUserId, secondUserId=request.secondUserId
            )
        )
        print(response)

    return {"status": 200}


@app.get("/chats/")
async def get_chats(access_token: str = Cookie(None)):
    data = jwt.decode(access_token, key=os.getenv("SECRET_KEY"), algorithms="HS256")
    print(data)
    res = []
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        client = chats_pb2_grpc.ChatsStub(channel)
        arg = chats_pb2.User(username=data["username"])
        async for elem in client.GetChats(arg):
            participants = list(elem.participants)
            participants.remove(data["username"])
            res.append({"chatId": elem.chatId, "username": participants[0]})

    print(res)

    return {"status": 200, "data": res}
