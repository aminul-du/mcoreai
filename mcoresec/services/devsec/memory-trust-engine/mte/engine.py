from datetime import datetime, timezone
from .checks import run_all
from .config import Config
from .store import MemoryStore


class MTE:
    def __init__(self, config: Config):
        self.config = config
        self.store = MemoryStore(config.store_path, config.quarantine_path)

    def write(self, source: str, content: str) -> dict:
        prev_hash = self.store.last_hash()
        results, new_hash, all_ok = run_all(
            source, content,
            self.config.trusted_sources,
            self.config.injection_patterns,
            prev_hash,
        )
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "content": content,
            "prev_hash": prev_hash,
            "hash": new_hash,
            "checks": [{"name": r.name, "ok": r.ok, "reason": r.reason} for r in results],
            "verdict": "PASS" if all_ok else "BLOCK",
        }
        self.store.append(record, quarantine=not all_ok)
        return record
