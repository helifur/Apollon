import grpc
import logging
import asyncio
from concurrent import futures

import protobuf.chats_pb2 as chats_pb2
import protobuf.chats_pb2_grpc as chats_pb2_grpc

from database.database import init
from models.chats import Chat
from models.message import Message
from beanie.operators import In


class ChatServicer(chats_pb2_grpc.ChatsServicer):
    async def GetChats(self, request, context):
        candidates = await Chat.find_all(
            request.username in Chat.participants
        ).to_list()

        for elem in candidates:
            yield chats_pb2.Chat(chatId=str(elem.id), participants=elem.participants)

    async def CreateChat(self, request, context):
        candidate = Chat(participants=[request.firstUserId, request.secondUserId])
        await candidate.insert()
        print(type(candidate.id))

        return chats_pb2.Chat(
            chatId=str(candidate.id), participants=candidate.participants
        )

    async def GetMessages(self, request, context):
        candidates = await Message.find_all(Message.chatId == request.chatId).to_list()

        for elem in candidates:
            yield chats_pb2.Message(
                chatId=elem.chatId,
                senderId=elem.senderId,
                text=elem.text,
                time=elem.time,
            )


async def serve():
    await init()
    server = grpc.aio.server()

    chats_pb2_grpc.add_ChatsServicer_to_server(ChatServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Server started at port 50051!")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.get_event_loop().run_until_complete(serve())
