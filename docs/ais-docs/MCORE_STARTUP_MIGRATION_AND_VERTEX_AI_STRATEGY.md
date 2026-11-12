# 🛡️ MCore Sovereign Startup Migration & Vertex AI Data Store Strategy
## End-to-End Local-to-Cloud Knowledge Ingestion, Architecture Formatting & CLI Trust Policy Blueprint
**Document Reference:** `MCORE-STRAT-VAI-001`  
**Classification:** Venture-Ready / Confidential Academic & Startup Architecture Record  
**Founder & Final Authority:** Aminul Islam Shamim (AIS) | ID: `MCORE-FDR-AIS-001`  
**Host Target:** `mcorebd` (Debian 13 Trixie / Sovereign Bare-Metal Architecture)  
**Academic Alignment:** `AIS-DU-PMICS-PROJECT-SBOX` (Dhaka University PMICS)  
**Live Portal Anchor:** `https://colab.mcoreai.dev/tree/ais-docs`  
**GCP Project Anchor:** `project-12884862-2ba9-4048-b03` (Project Number: `469173990872`)  
**Publication Date:** November 10, 2026 (UTC)  

---

## 1. Executive Summary & Venture Mission

This executive blueprint defines the comprehensive operational strategy connecting Founder Aminul Islam Shamim’s local sovereign engineering stack to Google Cloud’s enterprise Vertex AI Data Store ecosystem. 

Designed to satisfy institutional venture capital due diligence, startup accelerator benchmarks (Y Combinator, Techstars, Google for Startups), and Dhaka University PMICS academic criteria, this strategy achieves three critical goals:
1. **Sovereign Local-to-Cloud Knowledge Pipeline:** Connects the local monorepo (`/srv/mcore/mcore365` and `/home/mcoreai`) directly to Google Cloud Vertex AI Search and Conversation Data Stores.
2. **Zero-Downtime Startup Migration:** Preserves zero-cost bare-metal performance locally on `mcorebd` while guaranteeing 100% container parity with Google Cloud Run (`shorbornoai-launch`).
3. **Cryptographic Policy & Trust Governance:** Codifies the DeepSeek code-ingestion protocol and Gemini CLI Tier 4 policy engine guardrails.

---

## 2. Local-to-Vertex AI Gap Analysis (Empirical Audit Findings)

An exhaustive empirical audit of the local microservice stack and active Google Cloud environment identified four actionable integration gaps:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        EMPIRICAL GAP ANALYSIS: LOCAL ↔ GCP                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP 1: Project ID Configuration Drift in terminal-ai                                   │
│ • /srv/mcore/mcore365/mcoresec/apps/terminal-ai/main.py defines fallback project        │
│   '595209408050', whereas active project is 'project-12884862-2ba9-4048-b03'.       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP 2: Inactive Vertex AI Flag in Local Inference Daemon                               │
│ • USE_VERTEX_AI is currently defaulted to false, causing terminal-ai to fall back to   │
│   Gemini Developer API keys rather than native Vertex AI IAM credentials.              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP 3: Absence of Provisioned Vertex AI Search Data Store                              │
│ • Discovery Engine API query confirms zero active data stores in GCP project.          │
│ • Monorepo documents and schemas currently lack an automated cloud vector index.       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP 4: Missing GCS Knowledge Sync Pipeline                                             │
│ • Monorepo architecture docs (docs/, schemas/, MCORE-DOCS-001) are not currently       │
│   automatically synced to a dedicated Google Cloud Storage Knowledge Bucket.          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. End-to-End Blueprint: Connecting Monorepo to Vertex AI Data Store

The diagram below illustrates the dual-tier hybrid architecture: low-latency, sovereign memory runs locally on bare metal (Qdrant + MTE), while broad enterprise reasoning is grounded via Google Cloud Vertex AI Search Data Store.

```
 [ Local Host: mcorebd ]                                 [ Google Cloud Platform ]
 /home/mcoreai & /srv/mcore/mcore365                     project-12884862-2ba9-4048-b03
 ┌─────────────────────────────────┐                     ┌───────────────────────────────┐
 │ 1. Monorepo Knowledge Fabric    │                     │ 3. Cloud Storage Bucket       │
 │    • docs/ & MCORE-DOCS-001     │ ── gsutil rsync ──► │    gs://mcore-knowledge-store │
 │    • schemas & DOMAIN-MAP.md    │                     │    (Unstructured Markdown)    │
 └────────────────┬────────────────┘                     └───────────────┬───────────────┘
                  │                                                      │
                  ▼                                                      ▼
 ┌─────────────────────────────────┐                     ┌───────────────────────────────┐
 │ 2. Local Sovereign Private RAG  │                     │ 4. Vertex AI Search DataStore │
 │    • Qdrant (:6333) - HNSW      │                     │    Collection: default        │
 │    • MTE Poison Filter (:8100)  │                     │    Engine: mcore-knowledge    │
 └────────────────┬────────────────┘                     └───────────────┬───────────────┘
                  │                                                      │
                  ▼                                                      ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │ 5. MCore Unified Inference Engine (terminal-ai :8200 & Cloud Run shorbornoai)         │
 │    • Google GenAI SDK v1 (Python 3.14)                                                │
 │    • Grounding Tool: types.Tool(retrieval=types.Retrieval(vertex_ai_search=...))      │
 └───────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Step 1: Provision the GCS Knowledge Bucket
Create a dedicated, versioned Cloud Storage bucket in your target region (`us-central1`):
```bash
gcloud storage buckets create gs://mcore-knowledge-store-469173990872 \
  --project=project-12884862-2ba9-4048-b03 \
  --location=us-central1 \
  --uniform-bucket-level-access
```

### 3.2 Step 2: Automated Monorepo Knowledge Sync Script
Add this automated sync task to `setup_master_devops_deploy.sh`:
```bash
#!/usr/bin/env bash
# Sync curated monorepo knowledge documents to GCS
TARGET_BUCKET="gs://mcore-knowledge-store-469173990872/monorepo-corpus"

mkdir -p /home/mcoreai/staging/knowledge-corpus
cp -u /srv/mcore/mcore365/docs/MCORE-DOCS-001.md /home/mcoreai/staging/knowledge-corpus/
cp -u /home/mcoreai/docs/*.md /home/mcoreai/staging/knowledge-corpus/
cp -u /srv/mcore/mcore365/sandbox/DOMAIN-MAP.md /home/mcoreai/staging/knowledge-corpus/

gcloud storage rsync -r /home/mcoreai/staging/knowledge-corpus "$TARGET_BUCKET"
```

### 3.3 Step 3: Create the Vertex AI Search Data Store
In Google Cloud Discovery Engine (Vertex AI Agent Builder / Search):
1. **Create Data Store:** Choose **Cloud Storage** $\rightarrow$ select `gs://mcore-knowledge-store-469173990872/monorepo-corpus/*`.
2. **Data Format:** Unstructured (Markdown / PDF / Text).
3. **Chunking Strategy:** Chunk size: 500 tokens, 10% overlap.
4. **Data Store ID:** `mcore-monorepo-docs`.

### 3.4 Step 4: Native Python 3.14 Integration in `terminal-ai`
Update `/srv/mcore/mcore365/mcoresec/apps/terminal-ai/main.py` to enable grounded Vertex AI Search retrieval:

```python
from google import genai
from google.genai import types

# Initialize Vertex AI Client with Application Default Credentials
client = genai.Client(
    vertexai=True,
    project="project-12884862-2ba9-4048-b03",
    location="us-central1"
)

# Ground generation with the Vertex AI Search Data Store
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                retrieval=types.Retrieval(
                    vertex_ai_search=types.VertexAISearch(
                        datastore="projects/469173990872/locations/global/collections/default_collection/dataStores/mcore-monorepo-docs"
                    )
                )
            )
        ]
    )
)
```

---

## 4. Startup Migration Strategy: Bare-Metal to Cloud Parity

To scale MCore into a multi-million-dollar AI venture without prematurely burning cash on cloud compute, we maintain a **3-Phase Evolution Architecture**:

| Phase | Operational Mode | Compute Location | Monthly Cost | Compliance Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Sovereign Bare-Metal (Current)** | Native Debian 13 systemd daemons (`:8000`, `:8100`, `:8200`, `:8899`) | Host `mcorebd` | **$0.00** | G0–G5 (DU Academic Verified) |
| **Phase 2: Hybrid Edge Gateway** | Cloudflare AI Workers (`cf-ai-worker`) + Argo QUIC Tunnel Ingress | Cloudflare Edge + `mcorebd` | **$0.00** (Free Tier) | SOC2 Boundary Separation |
| **Phase 3: Multi-Region Cloud Run** | Cloud Run (`shorbornoai-launch`) + Vertex AI Data Store | GCP `us-central1` | Autoscaling on demand | SOC2 Type II / Enterprise Ready |

### Strict Container Parity Rule
All microservices must execute identically whether running directly on bare-metal or inside Google Cloud Run. Every Dockerfile adheres to unprivileged execution:
```dockerfile
FROM python:3.14-slim-bookworm
RUN adduser --disabled-password --gecos "" --uid 1000 mcoreai
WORKDIR /app
COPY --chown=mcoreai:mcoreai . /app
USER 1000:1000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Architectural Asset Formatting Protocol (DeepSeek Ingestion)

To consolidate historical code and architecture blueprints generated with external LLMs (e.g. DeepSeek) into our local Knowledge Fabric, assets must adhere to this standardized ingestion schema:

### 5.1 Machine-Readable Block Structure
```markdown
===FILE_START===
Path: [relative/path/to/target/file.ext]
Category: [Architecture | DevOps | Microservice | Security | Database | EdgeWorker]
Description: [One-line technical summary of component responsibility]
Dependencies: [List of packages, ports, or runtime prerequisites]

```[language]
[Full, complete, un-truncated production code. Zero placeholders.]
```
===FILE_END===
```

### 5.2 Local Archive Directory Taxonomy
All ingested files are stored in `/home/mcoreai/archive/deepseek-ingest/`:
* `01_architecture/` — High-level network topologies, threat models, and sequence diagrams.
* `02_docker_and_k8s/` — Container manifests, compose files, and healthchecks.
* `03_services_and_apis/` — Python FastAPI, Rust policy modules, and Node.js gateway code.
* `04_scripts_and_devops/` — Bash deployment pipelines, backup automations, and systemd units.
* `05_security_and_mte/` — Memory trust scoring formulas and prompt quarantine logic.
* `INGEST_MANIFEST.json` — Cryptographic SHA-256 index of every ingested module.

---

## 6. Gemini CLI Trust Policy & Security Guardrails

*Governed by official specifications: [Policy Engine](https://geminicli.com/docs/reference/policy-engine/) • [Trusted Folders](https://geminicli.com/docs/cli/trusted-folders/)*

To ensure safe, autonomous developer assistance without unintended side effects, the following controls are deployed across host `mcorebd`:

### 6.1 Active Configuration Status
* **Folder Trust (`~/.gemini/trustedFolders.json`):**
  ```json
  {
    "/home/mcoreai": "TRUST_FOLDER",
    "/srv/mcore/mcore365": "TRUST_FOLDER"
  }
  ```
* **Security Settings (`~/.gemini/settings.json`):**
  - `security.disableYoloMode: true` (Strictly forbids unconstrained auto-execution).
  - `security.enablePermanentToolApproval: true` (Permits permanent rule addition).
  - `security.autoAddToPolicyByDefault: false` (Prevents silent auto-approvals).
  - `security.environmentVariableRedaction: true` (Masks tokens and credentials).

### 6.2 Tier 4 User Policy Guardrails (`~/.gemini/policies/mcore-guardrails.toml`)
* **Auto-Allowed Actions (`allow`):** Routine inspection commands (`git status`, `git log`, `git branch`, `git diff`, `uname`, `df`).
* **Manual Confirmation Required (`ask_user`):**
  - File writes and modifications (`write_file`, `replace`).
  - Destructive commands (`rm`, `git reset`, `git clean`, `dropdb`).
  - Cloud infrastructure & deployments (`gcloud`, `terraform`, `wrangler deploy`, `docker push`).
  - Privilege escalation & credentials (`sudo`, `su`, `passwd`, `ssh-keygen`).
* **Unconditionally Denied (`deny`):**
  - Catastrophic root path deletions (`rm -rf /`, `rm -rf /srv`, `rm -rf /home`).

---

## 7. Document Verification & Google Drive Web Ingress

This document is compiled and live across your sovereign web documentation endpoints:
* **Colab Portal Ingress:** `https://colab.mcoreai.dev/tree/ais-docs`
* **Local Colab Anchor:** `/srv/aiseye/ais-docs/MCORE_STARTUP_MIGRATION_AND_VERTEX_AI_STRATEGY.md`
* **Sovereign Monorepo Source:** `/srv/mcore/mcore365/docs/ais-docs/MCORE_STARTUP_MIGRATION_AND_VERTEX_AI_STRATEGY.md`
* **Edge Cloudflare Pages:** `https://mcore-docs.me-419.workers.dev`

---

**Authored and Certified by MCore Architecture Engine on behalf of Founder Aminul Islam Shamim (AIS).**
