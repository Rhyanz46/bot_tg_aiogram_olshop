from dotenv import load_dotenv
import os
load_dotenv()


class DatabaseConfig:
    def __init__(self):
        self.user: str = os.getenv("DATABASE_USER")
        self.pw: str = os.getenv("DATABASE_PW")
        self.host: str = os.getenv("DATABASE_HOST")
        self.db: str = os.getenv("DATABASE_DB")


class BotConfig:
    def __init__(self):
        self.token: str = os.getenv("BOT_API")
