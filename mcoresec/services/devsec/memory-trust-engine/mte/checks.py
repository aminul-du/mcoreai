import hashlib
from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    ok: bool
    reason: str


def check_provenance(source: str, trusted: tuple[str, ...]) -> CheckResult:
    if source in trusted:
        return CheckResult("provenance", True, f"source '{source}' in trusted list")
    return CheckResult("provenance", False, f"source '{source}' NOT in trusted list")


def check_injection(content: str, patterns: tuple[str, ...]) -> CheckResult:
    lower = content.lower()
    for p in patterns:
        if p in lower:
            return CheckResult("injection", False, f"matched pattern: '{p}'")
    return CheckResult("injection", True, "no injection patterns matched")


def check_chain(prev_hash: str, content: str) -> tuple[CheckResult, str]:
    new_hash = hashlib.sha256((prev_hash + content).encode("utf-8")).hexdigest()
    return CheckResult("chain", True, f"new_hash={new_hash[:16]}..."), new_hash


def run_all(
    source: str,
    content: str,
    trusted: tuple[str, ...],
    patterns: tuple[str, ...],
    prev_hash: str,
) -> tuple[list[CheckResult], str, bool]:
    results = [
        check_provenance(source, trusted),
        check_injection(content, patterns),
    ]
    chain_r, new_hash = check_chain(prev_hash, content)
    results.append(chain_r)
    all_ok = all(r.ok for r in results)
    return results, new_hash, all_ok
