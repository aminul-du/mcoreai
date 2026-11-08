# 📊 Data Provenance, Licensing & Integrity Charter
## AIS-DU-PMICS-PROJECT-SBOX Data Governance

**Project Identifier:** `AIS-DU-PMICS-PROJECT-SBOX`  
**Data Custodian:** Founder Aminul Islam Shamim (AIS)  
**Licensing Baseline:** Sovereign Research Commons (Open Academic Attribution)  
**Cryptographic Integrity:** Standard SHA-256 Digest  

---

## 1. Dataset Taxonomy & Partitioning

1. **Clean Baseline Corpus (`clean_provenance_v1.jsonl`):**
   * Curated enterprise zero-trust policy statements, architectural documentation, and verified system prompts.
   * Designated trusted sources: `mcore-docs`, `github-attestation`, `internal-ingest`, `operator:aminul`.
2. **Adversarial Hazard Corpus (`adversarial_injection_v1.jsonl`):**
   * Synthetic and standardized prompt injection, system role override, jailbreak, and delimiter escape vectors.
   * Designated untrusted sources: `attacker`, `untrusted-web`, `external-feed`.

---

## 2. Integrity & Cryptographic Chain

Every dataset item must be indexed in `dataset_manifest.json` with an unalterable SHA-256 hash before entering an experimental pipeline. Any hash discrepancy triggers an immediate experimental abort.
