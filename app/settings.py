import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self):
        self.VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "musaned_verify_token")
        self.APP_ENV = os.getenv("APP_ENV", "dev")


settings = Settings()