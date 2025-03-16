from typing import List
from beanie import Document


class Chat(Document):
    participants: List[str]
    is_unread: bool = False
