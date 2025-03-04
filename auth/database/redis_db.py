import redis
import os
from dotenv import load_dotenv


def init_redis():
    load_dotenv()
    host = os.getenv("REDIS_HOSTNAME")
    port = os.getenv("REDIS_PORT")
    user = os.getenv("REDIS_USER")
    password = os.getenv("REDIS_PASSWORD")

    return redis.Redis(host=host, port=port)
