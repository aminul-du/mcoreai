import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TRUSTED_SOURCES = (
    "mcore-docs",
    "github-attestation",
    "internal-ingest",
    "operator:aminul",
)

DEFAULT_INJECTION_PATTERNS = (
    "ignore previous",
    "ignore all previous",
    "disregard previous",
    "forget previous",
    "ignore the above",
    "new instructions",
    "you are now",
    "system:",
    "assistant:",
    "override",
    "<|im_start|>",
    "<|im_end|>",
    "[inst]",
    "[/inst]",
    "###instruction",
)


@dataclass
class Config:
    store_path: Path
    quarantine_path: Path
    evidence_dir: Path
    trusted_sources: tuple[str, ...] = DEFAULT_TRUSTED_SOURCES
    injection_patterns: tuple[str, ...] = DEFAULT_INJECTION_PATTERNS

    @classmethod
    def default(cls) -> "Config":
        base_env = os.environ.get("MTE_DATA_DIR")
        base = Path(base_env) if base_env else Path(__file__).parent.parent / "data"
        ev_env = os.environ.get("MTE_EVIDENCE_DIR")
        ev = Path(ev_env) if ev_env else Path(__file__).parent.parent.parent.parent.parent / "evidence"
        return cls(
            store_path=base / "trusted.jsonl",
            quarantine_path=base / "quarantine.jsonl",
            evidence_dir=ev,
        )
