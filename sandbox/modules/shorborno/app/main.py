"""ShorbornoAI module — runs as UID 1001 in Alpine."""
import os
from fastapi import FastAPI

app = FastAPI(title="Fabric ShorbornoAI", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "shorborno", "uid": os.getuid()}


@app.get("/ready")
async def ready():
    return {"status": "ready"}


@app.get("/models")
async def models():
    return {"models": [], "module": "shorborno-ai"}
