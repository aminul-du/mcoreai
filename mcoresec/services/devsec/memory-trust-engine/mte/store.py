import json
from pathlib import Path


class MemoryStore:
    def __init__(self, trusted: Path, quarantine: Path):
        self.trusted = trusted
        self.quarantine = quarantine
        self.trusted.parent.mkdir(parents=True, exist_ok=True)
        self.quarantine.parent.mkdir(parents=True, exist_ok=True)
        self.trusted.touch(exist_ok=True)
        self.quarantine.touch(exist_ok=True)

    def last_hash(self) -> str:
        lines = self.trusted.read_text().strip().splitlines()
        if not lines:
            return "0" * 64
        return json.loads(lines[-1])["hash"]

    def append(self, record: dict, *, quarantine: bool = False) -> None:
        target = self.quarantine if quarantine else self.trusted
        with target.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def counts(self) -> tuple[int, int]:
        t = sum(1 for _ in self.trusted.open()) if self.trusted.exists() else 0
        q = sum(1 for _ in self.quarantine.open()) if self.quarantine.exists() else 0
        return t, q
