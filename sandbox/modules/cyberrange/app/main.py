"""Cyber-Range module — runs as UID 1001 in Alpine."""
import os
from fastapi import FastAPI

app = FastAPI(title="Fabric Cyber-Range", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "cyberrange", "uid": os.getuid()}


@app.get("/ready")
async def ready():
    return {"status": "ready"}


@app.get("/scenarios")
async def scenarios():
    return {"scenarios": [], "module": "cyber-range"}
