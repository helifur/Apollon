import os
from dotenv import load_dotenv

from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import User


load_dotenv()


async def init():
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    db_name = os.getenv("MONGO_INITDB_DATABASE")
    host = os.getenv("MONGO_HOSTNAME")
    port = os.getenv("MONGO_PORT")

    client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}")

    db = client.users

    print(await client.list_database_names())

    await init_beanie(database=db, document_models=[User])
