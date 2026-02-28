from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "change_me")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "change_me")
    PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID", "change_me")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    APP_ENV: str = os.getenv("APP_ENV", "dev")

settings = Settings()
