from mte.config import Config
from mte.engine import MTE


def make_mte(tmp_path):
    cfg = Config(
        store_path=tmp_path / "trusted.jsonl",
        quarantine_path=tmp_path / "quarantine.jsonl",
        evidence_dir=tmp_path / "evidence",
    )
    return MTE(cfg), cfg


def test_clean_memory_passes(tmp_path):
    mte, cfg = make_mte(tmp_path)
    r = mte.write("mcore-docs", "CIA Integrity means data has not been altered.")
    assert r["verdict"] == "PASS"
    assert all(c["ok"] for c in r["checks"])
    assert cfg.store_path.read_text().count("\n") == 1
    assert cfg.quarantine_path.read_text() == ""
