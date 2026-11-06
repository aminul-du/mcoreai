import logging
from fastapi import FastAPI
from .routes import router
from .config import settings

logging.basicConfig(level=settings.LOG_LEVEL.upper())
app = FastAPI(title="mcoresec-api", version="0.1.0")
app.include_router(router)
