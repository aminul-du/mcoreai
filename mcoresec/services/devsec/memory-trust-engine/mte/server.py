from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .config import Config
from .engine import MTE

app = FastAPI(title="Memory Trust Engine", version="0.1.0")
mte = MTE(Config.default())

class MemoryWrite(BaseModel):
    source: str
    content: str

@app.post("/mte/write")
def write_memory(req: MemoryWrite):
    record = mte.write(req.source, req.content)
    if record["verdict"] == "BLOCK":
        raise HTTPException(status_code=403, detail={"verdict": "BLOCK", "checks": record["checks"]})
    return {"verdict": "PASS", "hash": record["hash"]}

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "mte"}
