from os import access
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import grpc
from pydantic import BaseModel

import protobuf.auth_pb2 as auth_pb2
import protobuf.auth_pb2_grpc as auth_pb2_grpc


router = APIRouter()


class AuthRequest(BaseModel):
    username: str
    password: str


@router.post("/auth")
async def auth_user(request: AuthRequest):
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        client = auth_pb2_grpc.AuthStub(channel)
        res = await client.GetToken(
            auth_pb2.UserCredentials(
                username=request.username, password=request.password
            )
        )

    if not res.access_token:
        return {"status": status.HTTP_409_CONFLICT}

    response = JSONResponse(content={"status": status.HTTP_200_OK})
    response.set_cookie(key="access_token", value=res.access_token)

    return response
