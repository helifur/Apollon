from beanie import Document


class User(Document):
    name: str
    username: str
    hashed_password: str
    desc: str = ""

    class Settings:
        collection = "users"
