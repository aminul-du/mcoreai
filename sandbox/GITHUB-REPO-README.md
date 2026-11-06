# Meticulous Core AI (MCoreAI)
## Universal Documentation, Evidence & AI Knowledge Fabric

**MCORE-DOCS-001** — Cloudflare Tunnel & Networking Strategy

### Repository: https://github.com/aminul-du/mcoreai.git

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/aminul-du/mcoreai.git
cd mcoreai

# 2. Configure
cp .env.example .env
# Edit .env with your Cloudflare API token, tunnel token, passwords

# 3. Deploy everything
chmod +x deploy.sh && ./deploy.sh

# 4. Or deploy step by step
make up          # Start Docker services
make health      # Check health
make deploy      # Deploy via SSH to production
```

## What's in this repo

```
mcoreai/
├── deploy.sh                         # End-to-end deployment script
├── docker-compose.yml                # Base config (dev/staging)
├── docker-compose.prod.yml           # Production overlay (zero-downtime)
├── docker-compose.home.yml           # Home network (WSL bridge access)
├── docker-bake.hcl                   # Buildx multi-arch matrix
├── Makefile                           # Standardized operations
├── .env.example                       # Config template
├── .env.production                    # Production env template
│
├── apps/web/                         # Next.js frontend (Alpine, UID 1001)
│   ├── Dockerfile                      # Multi-stage Node Alpine
│   ├── package.json
│   ├── next.config.js
│   └── .required-env
│
├── services/
│   ├── Dockerfile.python              # Shared multi-stage Python Alpine
│   ├── ingestion/                     # FastAPI ingestion workers
│   │   ├── requirements.txt
│   │   └── app/main.py
│   └── policy-core/                   # Rust/Axum policy core
│       ├── Dockerfile                 # Multi-stage Rust Alpine
│       ├── Cargo.toml
│       └── src/main.rs
│
├── modules/                           # Isolated domain modules
│   ├── neteng/                        # Network engineering
│   ├── cyberrange/                    # Cyber-range
│   └── shorborno/                     # ShorbornoAI
│
├── workers/                           # 9 Cloudflare Workers
│   ├── mcore-edge-gateway/            # JWT validation + audit
│   ├── mcore-health-monitor/         # Cron health checks
│   ├── mcore-ai-fabric/              # Llama 3.1 + BGE + D1
│   ├── mcore-d1-api/                 # CRUD API
│   ├── mcore-compliance-report/      # Compliance reports
│   ├── mcore-browser-collector/      # Browser Rendering
│   ├── mcore-ai-search/              # Semantic search
│   ├── mcore-webhook/                # Provider webhooks
│   └── mcore-gateway/                # Master API router
│
├── infra/
│   ├── entrypoint.sh                  # Non-root entrypoint (UID 1001)
│   ├── healthcheck.py                 # Universal health check
│   └── postgres/init/01-init.sql      # DB schema
│
├── pages/
│   ├── mcore-identity/                # Identity banner
│   └── status/                        # Status dashboard
│
├── cloudflared/
│   └── config.yml                     # Locally-managed tunnel config
│
├── mcore-tunnel/                      # Python automation CLI
│   ├── setup.sh                        # venv setup
│   ├── requirements.txt
│   ├── mcore_local_ai.py              # Local AI connector
│   └── mcore/                         # Python package
│       ├── config.py                   # Settings from env
│       ├── api_client.py               # Cloudflare API wrapper
│       ├── tunnel_manager.py           # Tunnel CRUD
│       ├── dns_manager.py              # DNS routing
│       ├── access_manager.py           # Zero Trust Access
│       ├── audit_logger.py             # Audit logs
│       ├── warp_network.py             # Private network
│       └── cli.py                      # Click CLI
│
└── .github/workflows/
    ├── deploy.yml                     # Full CI/CD (test→build→deploy→scan)
    ├── ci-cd.yml                      # Matrix CI/CD
    └── security.yml                   # SAST, SBOM, secret scan
```

## Live Resources (56 total)

| Category | Count | Details |
|---|---|---|
| Workers | 9 | edge-gateway, health-monitor, ai-fabric, d1-api, compliance-report, browser-collector, ai-search, webhook, gateway |
| Worker Routes | 10 | api/*, docs/*, ais001/api/*, ais001/data/*, cf-ais001/*, report/*, capture/*, search/*, hooks/*, gateway/* |
| Tunnel CNAMEs | 11 | ais001, app, ssh, api, docs, cf-ais001, report, capture, search, hooks, gateway |
| D1 Tables | 5 | audit_log, documents, policies, providers, evidence_links (36 records) |
| KV | 1 | mcore-tunnel-state |
| Queue | 1 | mcore-ingestion |
| AI Search | 1 | mcore-fabric / mcore-docs |
| Workers AI | 2 | Llama 3.1 8B + BGE embeddings |
| Pages | 1 | mcore-status.pages.dev |
| Cron Triggers | 3 | health (5min), compliance (daily), search (daily) |
| Security | 11 | HTTP/3, 0-RTT, Early Hints, HSTS, TLS 1.2+, HTTPS, Brotli, Cache, WAF, DDoS |

## GitHub Actions Secrets Required

| Secret | Value |
|---|---|
| `CF_API_TOKEN` | Cloudflare API token |
| `CF_ACCOUNT_ID` | `41903f4febb2c66dffd4ffcae558e692` |
| `WSL_HOST` | Your Debian/WSL host IP |
| `WSL_USER` | SSH username |
| `WSL_SSH_KEY` | SSH private key |

## Identity

| Field | Value |
|---|---|
| Entity | Meticulous Core Inc. (MCore) |
| Founder | Aminul Islam Shamim (AIS) |
| Operator ID | MCORE-FDR-AIS-001 |
| Baseline | @AIS-DU |
| Project | shorbornoai.com (DU-PROJECT) |
| Contact | shorbornoai@gmail.com / me@aminul-du.com |
