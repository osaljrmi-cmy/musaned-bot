import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self):
        self.VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "musaned_verify_token")
        self.APP_ENV = os.getenv("APP_ENV", "dev")
        self.SUPERVISOR_WA_ID = os.getenv("SUPERVISOR_WA_ID", "")


settings = Settings()