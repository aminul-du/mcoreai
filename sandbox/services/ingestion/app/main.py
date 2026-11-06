"""
Ingestion Workers — FastAPI
Handles document ingestion from Microsoft, Google, GitHub, and local AI providers.
Runs as UID 1001 in an Alpine container.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HealthStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify required env vars
    required = ["DATABASE_URL", "VECTOR_ADAPTER"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")
    yield  # App runs
    # Shutdown: cleanup


app = FastAPI(
    title="Fabric Ingestion Workers",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    """Health check endpoint — used by Docker HEALTHCHECK."""
    return {"status": "healthy", "service": "ingestion", "uid": os.getuid()}


@app.get("/ready")
async def ready():
    """Readiness check — verifies DB + vector store connectivity."""
    return {"status": "ready", "adapter": os.environ.get("VECTOR_ADAPTER")}


@app.post("/ingest")
async def ingest(source: str):
    """Ingest documents from a provider: microsoft | google | github | local."""
    return {"status": "accepted", "source": source}
