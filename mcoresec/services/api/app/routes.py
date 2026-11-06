import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .config import settings

router = APIRouter()

class MemoryIn(BaseModel):
    source: str
    content: str

@router.post("/api/memory")
async def write_memory(req: MemoryIn):
    """Gateway routes memory writes through the MTE before accepting."""
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(f"{settings.MTE_URL}/mte/write", json=req.model_dump(), timeout=5.0)
            r.raise_for_status()
            return {"gateway": "accepted", "mte": r.json()}
        except httpx.HTTPStatusError as e:
            # MTE returned 403 (blocked)
            raise HTTPException(status_code=403, detail=e.response.json())
        except httpx.RequestError:
            # MTE is down -> Fail closed
            raise HTTPException(status_code=503, detail="MTE Unavailable — Fail Closed")

@router.get("/healthz")
def healthz():
    return {"status": "ok", "service": "api"}
