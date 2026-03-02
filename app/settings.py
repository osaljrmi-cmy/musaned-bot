import os
from dotenv import load_dotenv

# تحميل .env محلياً فقط (Render يعتمد على Environment مباشرة)
load_dotenv()


class Settings:
    @property
    def VERIFY_TOKEN(self) -> str:
        return os.getenv("VERIFY_TOKEN", "change_me")

    @property
    def APP_ENV(self) -> str:
        return os.getenv("APP_ENV", "dev")

settings = Settings()