import asyncio
import os
import sys
import logging
from datetime import datetime, timezone
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from google import genai

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
logger = logging.getLogger("terminal-ai")

MTE_WRITE_URL = os.getenv("MTE_WRITE_URL", "http://127.0.0.1:8100/mte/write")
MTE_TIMEOUT_SECONDS = float(os.getenv("MTE_TIMEOUT_SECONDS", "5.0"))

# Vertex AI / Gemini Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "595209408050")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
USE_VERTEX_AI = os.getenv("USE_VERTEX_AI", "false").lower() in ("true", "1", "yes")
VERTEX_MODEL_NAME = os.getenv("VERTEX_MODEL_NAME", "gemini-3.8-flash")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "PLACEHOLDER")

vertex_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vertex_model
    logger.info("Initializing AI Client (Vertex=%s)...", USE_VERTEX_AI)
    try:
        if USE_VERTEX_AI:
            client = genai.Client(
                vertexai=True, 
                project=GCP_PROJECT_ID, 
                location=GCP_LOCATION,
                api_key=GEMINI_API_KEY
            )
            logger.info(f"Vertex AI initialized for project {GCP_PROJECT_ID}.")
        else:
            client = genai.Client(api_key=GEMINI_API_KEY, vertexai=False)
            logger.info("Gemini Developer API initialized.")
        vertex_model = client
    except Exception as exc:
        logger.error("AI Initialization Failure: %s", exc)
        raise RuntimeError(exc) from exc
    yield
    logger.info("Shutting down Terminal AI.")

app = FastAPI(title="MCore Terminal AI", version="1.0.0", lifespan=lifespan)

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    status: str = "success"
    response: str
    mte_verdict: str = "PASS"

@app.get("/healthz")
async def healthz():
    return {"status": "healthy", "service": "terminal-ai"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    logger.info("Session '%s': Submitting prompt to MTE", payload.session_id)
    mte_payload = {"source": "terminal-ai", "content": payload.prompt}

    try:
        async with httpx.AsyncClient(timeout=MTE_TIMEOUT_SECONDS) as client:
            mte_response = await client.post(MTE_WRITE_URL, json=mte_payload)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="MTE unreachable")

    if mte_response.status_code == status.HTTP_403_FORBIDDEN:
        reason = mte_response.json().get("detail", {}).get("verdict", "Blocked")
        logger.warning("Session '%s' BLOCKED by MTE.", payload.session_id)
        return JSONResponse(
            status_code=403,
            content={"status": "blocked", "mte_verdict": "BLOCK", "quarantine_reason": reason}
        )

    if vertex_model is None:
        raise HTTPException(status_code=500, detail="Vertex AI uninitialized")

    try:
        # Non-blocking async thread dispatch for GenAI inference
        response = await asyncio.to_thread(
            vertex_model.models.generate_content,
            model=VERTEX_MODEL_NAME,
            contents=payload.prompt
        )
        ai_text = response.text if response and response.text else ""
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Vertex AI failed: {exc}")

    return ChatResponse(status="success", response=ai_text, mte_verdict="PASS")
