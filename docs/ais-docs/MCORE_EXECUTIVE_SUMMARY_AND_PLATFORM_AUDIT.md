# 🛡️ MCore Sovereign Startup Platform Audit & Lossless Executive Summary
## Complete A-to-Z Local Architecture, 14-Project Inventory, Gap Analysis & Unification Blueprint
**Document Reference:** `MCORE-EXEC-SUM-001`  
**Classification:** Sovereign Startup Audit & Executive Knowledge Anchor  
**Founder & Final Authority:** Aminul Islam Shamim (AIS) | ID: `MCORE-FDR-AIS-001`  
**Host Target:** `mcorebd` (Debian GNU/Linux 13 Trixie / WSL2 Kernel `6.18.58.1-microsoft-standard-WSL2`)  
**Academic Alignment:** `AIS-DU-PMICS-PROJECT-SBOX` (Dhaka University PMICS)  
**Live Ingress Endpoints:** `https://api.mcoreai.dev` | `https://colab.mcoreai.dev` | `https://mcore-docs.me-419.workers.dev`  
**GCP Project Anchor:** `project-12884862-2ba9-4048-b03` (Number: `469173990872`)  
**Audit Date:** November 12, 2026 (UTC)  

---

## 1. Executive Summary & Historical Lineage

This executive document captures the **lossless operational history, current state, architectural gaps, and forward roadmap** of the MCore Sovereign Autonomous Intelligence Infrastructure (SAII). 

### Lossless Git Commit Lineage (`/srv/mcore/mcore365`)
The platform has evolved through continuous bare-metal and zero-cost engineering milestones:
1. `dcc0dba`: Initial fallback handling for AI endpoint authorization.
2. `6ef0e4a`: Zero-trust terminal AI daemon and multi-cloud container definitions.
3. `511a652`: Monorepo export and synchronization pipeline.
4. `781d455`: Bare-metal Python 3.14 Colab bridge deployment and Pyenv migration.
5. `3e026e0`: Systemd infrastructure orchestration (MTE, Gateway API, Terminal AI on Gemini 3.8 Flash, PG17 pgvector, Qdrant).
6. `bd7da74`: Golden-master deployment engine (`setup_master_devops_deploy.sh v1.1.0`) with automated state validation and audit trails.
7. `3b46cb5` & `1d1705b`: Phase 1 v1.1.0 execution logic with subshell isolation and link recovery.
8. `9a9adc4`: AIS-MCore Collaboration Chronicle and G1/G4 controlled Google Drive verification probe.
9. `3aff0bc`: Complete Dhaka University PMICS 6-pillar academic suite, live `ais-docs` portal, and sovereign domain mappings.

---

## 2. 360° Ecosystem Inventory: The 14 Startup Projects

An exhaustive audit of systemd daemons, process trees, network sockets, and file trees verifies **14 operational projects and core engines**:

```
MCORE SOVEREIGN PLATFORM ARCHITECTURE (14 PROJECTS)
│
├── 🟢 ACTIVE LIVE DAEMONS (7 Microservices & Databases)
│   ├── [1] mcoresec-api (Zero-Trust Security Gateway API) ────────► Port 8000
│   ├── [2] mcoresec-mte (Predictive Memory Trust Engine) ────────► Port 8100
│   ├── [3] terminal-ai (Sovereign Terminal AI Daemon) ───────────► Port 8200
│   ├── [4] colab-backend (Jupyter Colab Bridge - Python 3.14) ──► Port 8899
│   ├── [5] qdrant (Qdrant High-Performance Vector Database) ─────► Ports 6333/6334
│   ├── [6] postgresql (PostgreSQL 17 ACID Database Cluster) ────► Port 5432
│   └── [7] cloudflared (Cloudflare QUIC Zero-Trust Tunnel) ──────► Tunnel ais001
│
├── 🚀 FRONTEND & APPLICATION WORKSPACES (3 Projects)
│   ├── [8] fabric-web (Next.js 15.1.3 + React 19 Sovereign Dashboard)
│   ├── [9] mcp-gateway (Model Context Protocol Tool & Resource Router)
│   └── [10] cf-ai-worker (Cloudflare Edge Workers AI Ingestion Engine)
│
└── 🛡️ ACADEMIC, CONTAINER & GOVERNANCE ENGINES (4 Projects)
    ├── [11] AIS-DU-PMICS-PROJECT-SBOX (Dhaka University 6-Gate Academic Research)
    ├── [12] shorbornoBD-NativeBox (Sovereign Multi-Cloud Container Engine)
    ├── [13] MCoreNativeEngine (18-Plane SAII Constitutional Governance Plane)
    └── [14] Edge Workers Fleet (8x Micro-Workers: Edge Gateway, D1 API, etc.)
```

### Deep-Dive Specification of Active Services
| Project | Path / Working Directory | Port(s) | Runtime | Systemd Unit | Public Domain Target |
|---|---|---|---|---|---|
| **mcoresec-api** | `/srv/mcore/mcore365/mcoresec/services/api` | `127.0.0.1:8000` | Python 3.13 / FastAPI | `mcoresec-api.service` | `https://api.mcoreai.dev` |
| **mcoresec-mte** | `/srv/mcore/mcore365/mcoresec/services/devsec/memory-trust-engine` | `127.0.0.1:8100` | Python 3.13 / FastAPI | `mcoresec-mte.service` | Internal Memory Bus |
| **terminal-ai** | `/srv/mcore/mcore365/mcoresec/apps/terminal-ai` | `127.0.0.1:8200` | Python 3.13 / Google GenAI | `terminal-ai.service` | Internal Agent Bus |
| **colab-backend**| `/srv/aiseye` | `127.0.0.1:8899` | Python 3.14.0 (`aisdu-env`) | `colab-backend.service` | `https://colab.mcoreai.dev` |
| **qdrant** | `/var/lib/qdrant` | `0.0.0.0:6333, 6334` | Native Rust Binary (v1.20.0) | `qdrant.service` | Local Vector Store |
| **postgresql** | `/var/lib/postgresql/17/main` | `127.0.0.1:5432` | Native PostgreSQL 17.0 Cluster| `postgresql@17-main.service`| Relational ACID Store |
| **cloudflared** | `/home/mcoreai/.cloudflared` | `127.0.0.1:20241`, QUIC | Native Go Binary | `cloudflared.service` | Cloudflare Edge Mesh |

---

## 3. Network, Sockets & Zero-Trust Ingress Map

```
 [ Public Internet ]
         │
         ▼
 [ Cloudflare Global Anycast Edge ]
   ├── 2x Dhaka Datacenters ('dac06')
   └── 2x Singapore Datacenters ('sin07', 'sin22')
         │
         │ Encrypted QUIC UDP Tunnel ('ais001': 78d7fa3b-c30b-44eb-a474-d3d0aa2d963d)
         ▼
 [ Local Host Egress IP: 113.11.1.161 ]
         │
         ▼ (Local Network eth0: 172.23.180.160/20)
 [ Loopback Virtual Sockets: 127.0.0.1 ]
         ├── :8000 ──► api.mcoreai.dev   (Zero-Trust Gateway API)
         └── :8899 ──► colab.mcoreai.dev (Sovereign Python 3.14 Colab Bridge)
```

---

## 4. Empirical Gap Analysis (Root Cause Audit)

An objective audit revealed five structural friction points between the local development environment and the sovereign vision:

### GAP 1: Workspace Path Fragmentation
- **Finding:** Codebases are divided across `/srv/mcore/mcore365` (production microservices), `/opt/MCoreNativeEngine` (system engine), and `/home/mcoreai` (development packages & docs).
- **Impact:** CLI file tools (`read_file`, `write_file`, `list_directory`) fail when attempting to cross workspace boundaries.

### GAP 2: Dual Identity & UID Split (`root` vs. `mcoreai`)
- **Finding:** Five active CLI sessions are running as `root` (pts/3, pts/4, pts/6, pts/9, pts/13), while three are running as `mcoreai` (pts/7, pts/10, pts/11).
- **Impact:** Files written by `root` trigger `EACCES: Permission Denied` errors when `mcoreai` attempts to update them.

### GAP 3: Gemini CLI Security Sandbox Restrictions
- **Finding:** Running `list_directory("/")` failed with `Path not in workspace: Attempted path "/" resolves outside the allowed workspace directories: /home/mcoreai`.
- **Impact:** Agent cannot execute filesystem-wide directory operations directly without explicit `--workspace` parameters or directory consolidation.

### GAP 4: Credential & Environment Sprawl in `/srv`
- **Finding:** Ten `.env` variants (`.env.dev`, `.env.prod`, `.env.local`, `.env.test`, `.env.staging`, etc.) sit in plain text across `/srv/mcore/mcore365/mcoresec/`.
- **Impact:** High attack surface if files are accidentally staged to Git or read by unprivileged processes.

### GAP 5: Inactive Docker Runtime Daemon
- **Finding:** `docker ps` returns `Docker not running or no permissions`.
- **Impact:** Prevents automated local testing of multi-cloud container parity (`docker-compose.yml`, Cloud Run mocks).

---

## 5. Architectural Recommendations & Future Options

| Option | Architecture Model | Key Strengths | Operational Risks | Recommendation Score |
|---|---|---|---|---|
| **Option A** | **Keep Existing Structure** | Zero setup cost; existing scripts run as-is. | Continued path drift; frequent sandbox boundary errors. | 55/100 |
| **Option B** | **Partial Monorepo Consolidation** | Moves `/home` dev files into `/srv/mcore/mcore365`. | Requires re-pointing existing systemd service definitions. | 75/100 |
| **Option C** | **DevContainer / Strict Docker Isolation** | Perfect parity with GCP Cloud Run. | High overhead; shifts away from ultra-fast bare-metal runtimes. | 70/100 |
| **Option D** | **Enterprise Unified Control Plane** | Clean separation of Config (`/home`), Code (`/workspace`), and Data (`/srv`). Multi-workspace trust enabled. | One-time path realignment and symlink generation. | **95/100 (Recommended)** |

---

## 6. Permanent Zero-Downtime Hardening Playbook

To eliminate all workspace errors, permission crashes, and CLI friction permanently:

### Step 1: Standardize Process Ownership on User `mcoreai`
Enforce uniform ownership across all project directories:
```bash
sudo chown -R mcoreai:mcoreai /srv/mcore /srv/aiseye /opt/MCoreNativeEngine /home/mcoreai
```
*Rule: Never launch Gemini CLI via `sudo gemini`. Always run as native user `mcoreai`.*

### Step 2: Register All Workspaces in Trusted Folders
Update `/home/mcoreai/.gemini/trustedFolders.json` with all active project locations:
```json
{
  "/home/mcoreai": "TRUST_FOLDER",
  "/srv/mcore": "TRUST_FOLDER",
  "/srv/mcore/mcore365": "TRUST_FOLDER",
  "/srv/mcore/shorbornoBD-NativeBox": "TRUST_FOLDER",
  "/srv/aiseye": "TRUST_FOLDER",
  "/opt/MCoreNativeEngine": "TRUST_FOLDER"
}
```

### Step 3: Multi-Workspace CLI Invocation
Launch the CLI with multi-workspace flags to allow cross-directory analysis:
```bash
gemini --workspace /home/mcoreai --workspace /srv/mcore/mcore365 --workspace /srv/aiseye
```

### Step 4: Keep Strict Tier 4 Guardrails Active
Maintain `/home/mcoreai/.gemini/policies/mcore-guardrails.toml` with:
- Auto-allow for read-only diagnostics (`git status`, `df`, `free`, `uname`).
- Mandatory user confirmation for file modifications (`write_file`, `replace`).
- Absolute denial of destructive root commands (`rm -rf /`, `rm -rf /srv`).

---

## 7. Knowledge Portal & File Synchronization Target

To update `ais-docs` across all local mirrors:
1. Master Document: `/home/mcoreai/docs/MCORE_EXECUTIVE_SUMMARY_AND_PLATFORM_AUDIT.md`
2. Mirror Destination 1: `/srv/mcore/mcore365/docs/ais-docs/`
3. Mirror Destination 2: `/srv/aiseye/ais-docs/`
4. Public Cloudflare Workers CDN: `https://mcore-docs.me-419.workers.dev`
5. Public Colab Bridge: `https://colab.mcoreai.dev/tree/ais-docs`

---
*End of MCORE-EXEC-SUM-001 Executive Audit Record.*
