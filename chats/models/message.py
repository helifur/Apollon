import datetime
from beanie import Document


class Message(Document):
    chatId: str
    senderUsername: str
    text: str
    time: datetime.datetime

    class Settings:
        name = "messages"
