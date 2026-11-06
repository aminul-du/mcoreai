import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MTE_URL: str = os.getenv("MTE_URL", "http://mte:8100")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()
