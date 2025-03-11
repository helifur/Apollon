import datetime
from beanie import Document


class Message(Document):
    chatId: str
    senderId: str
    text: str
    time: datetime.timedelta

    class Settings:
        name = "messages"
