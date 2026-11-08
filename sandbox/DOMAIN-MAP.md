# MCORE-DOCS-001 — Complete Domain & Subdomain Map
## All Hostnames, Workers, Routes, and Purposes

**Account:** Me@aminul-du.com's Account (`41903f4febb2c66dffd4ffcae558e692`)
**Tunnel ID:** `78d7fa3b-c30b-44eb-a474-d3d0aa2d963d`
**Team Domain:** `mcore-fdr-ais-001.cloudflareaccess.com`
**Last Updated:** 2026-11-06

---

## 1. Zone: `mcoreai.dev` (Dev / Agent / AI)

**Zone ID:** `c77c97a0d3a3119bae817ae56b1914be`
**Status:** Active · Proxied (orange cloud) on all CNAMEs
**Tunnel:** `78d7fa3b-c30b-44eb-a474-d3d0aa2d963d.cfargotunnel.com`

| # | Subdomain | Full Hostname | DNS Type | Target | Proxied | Worker Route | Worker | Purpose | Access |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `ais001` | `ais001.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `ais001.mcoreai.dev/api/*` | mcore-ai-fabric | Dev/Agent → WSL `:8000` + AI chat/embed/compliance | Zero Trust Access |
| 2 | `ais001` | `ais001.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `ais001.mcoreai.dev/data/*` | mcore-d1-api | D1 CRUD API (documents, policies, audit, stats) | Zero Trust Access |
| 3 | `cf-ais001` | `cf-ais001.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `cf-ais001.mcoreai.dev/*` | mcore-ai-fabric | Local AI (Ollama) + AI Fabric (chat, embed, local, compliance) | Zero Trust Access |
| 4 | `api` | `api.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `api.mcoreai.dev/*` | mcore-edge-gateway | Edge API gateway — JWT validation + audit logging | Zero Trust Access |
| 5 | `docs` | `docs.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `docs.mcoreai.dev/*` | mcore-edge-gateway | Documentation gateway — JWT validation + audit | Zero Trust Access |
| 6 | `app` | `app.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | — (direct tunnel) | — | App → tunnel → WSL service | Zero Trust Access |
| 7 | `ssh` | `ssh.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | — (direct tunnel) | — | SSH → tunnel → WSL `:22` | WARP + Access |
| 8 | `report` | `report.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `report.mcoreai.dev/*` | mcore-compliance-report | Compliance reports (CIA, SOC2, ISO27001, NIST) + audit log | Zero Trust Access |
| 9 | `capture` | `capture.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `capture.mcoreai.dev/*` | mcore-browser-collector | Browser Rendering — screenshots + web scraping as evidence | Zero Trust Access |
| 10 | `search` | `search.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `search.mcoreai.dev/*` | mcore-ai-search | Document indexing + semantic search (BGE embeddings) | Zero Trust Access |
| 11 | `hooks` | `hooks.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `hooks.mcoreai.dev/*` | mcore-webhook | Webhook receiver (GitHub, Microsoft, Google, generic) | Service Token |
| 12 | `gateway` | `gateway.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | `gateway.mcoreai.dev/*` | mcore-gateway | Master API gateway — routes to all other Workers | Zero Trust Access |
| 13 | `colab` | `colab.mcoreai.dev` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | — (direct tunnel) | — | Colab Bridge → tunnel → WSL `:8899` (Python 3.14 kernel) | Token + Zero Trust |

### Email Records (mcoreai.dev)

| # | Name | Type | Content | Purpose |
|---|---|---|---|---|
| 13 | `mcoreai.dev` | MX | `route1.mx.cloudflare.net` (priority 10) | Email routing |
| 14 | `mcoreai.dev` | MX | `route2.mx.cloudflare.net` (priority 20) | Email routing |
| 15 | `mcoreai.dev` | MX | `route3.mx.cloudflare.net` (priority 30) | Email routing |
| 16 | `mcoreai.dev` | TXT | `v=spf1 include:_spf.mx.cloudflare.net ~all` | SPF |
| 17 | `_dmarc.mcoreai.dev` | TXT | `v=DMARC1; p=none` | DMARC |
| 18 | `cf2024-1._domainkey.mcoreai.dev` | TXT | `v=DKIM1; h=sha256; k=rsa; ...` | DKIM |
| 19 | `_dmarc.mcoreai.dev` | TXT | `v=DMARC1; p=none` | TLSRPT |

---

## 2. Zone: `shorbornoai.com` (Production / DU-PROJECT)

**Zone ID:** `931cfa9a5124df8bf54206d2a783fb3d`
**Status:** Active
**Production Target:** GCP Cloud Run (URL pending — needs CNAME)

| # | Name | Type | Content | Proxied | Purpose | Status |
|---|---|---|---|---|---|---|
| 20 | `shorbornoai.com` | CNAME | `<GCP Cloud Run URL>` | 🟠 Yes | Production → GCP Cloud Run | ⚠ Pending URL |
| 21 | `shorbornoai.com` | MX | `route1.mx.cloudflare.net` (priority 10) | ⚫ No | Email routing | ✅ Created |
| 22 | `shorbornoai.com` | MX | `route2.mx.cloudflare.net` (priority 20) | ⚫ No | Email routing | ✅ Created |
| 23 | `shorbornoai.com` | MX | `route3.mx.cloudflare.net` (priority 30) | ⚫ No | Email routing | ✅ Created |
| 24 | `shorbornoai.com` | TXT | `v=spf1 include:_spf.mx.cloudflare.net ~all` | ⚫ No | SPF | ✅ Created |
| 25 | `_dmarc.shorbornoai.com` | TXT | `v=DMARC1; p=none` | ⚫ No | DMARC | ✅ Created |

---

## 3. Workers.dev Subdomains (Edge Compute)

**Workers Subdomain:** `me-419.workers.dev`

| # | Worker | URL | Bindings | Endpoints | Cron |
|---|---|---|---|---|---|
| 26 | mcore-edge-gateway | `mcore-edge-gateway.me-419.workers.dev` | KV + D1 | `/__health` (JWT validation + audit) | — |
| 27 | mcore-health-monitor | `mcore-health-monitor.me-419.workers.dev` | KV | `/status` `/status/run` | `*/5 * * * *` |
| 28 | mcore-ai-fabric | `mcore-ai-fabric.me-419.workers.dev` | AI + D1 + KV | `/chat` `/embed` `/local` `/compliance` `/evidence` `/providers` `/stats` `/documents` | — |
| 29 | mcore-d1-api | `mcore-d1-api.me-419.workers.dev` | D1 + KV | `/documents` `/policies` `/audit` `/evidence-links` `/stats` | — |
| 30 | mcore-compliance-report | `mcore-compliance-report.me-419.workers.dev` | D1 + KV | `/report` `/audit` | `0 0 * * *` (daily) |
| 31 | mcore-browser-collector | `mcore-browser-collector.me-419.workers.dev` | Browser + D1 + KV | `/capture` `/scrape` | — |
| 32 | mcore-ai-search | `mcore-ai-search.me-419.workers.dev` | AI + D1 + KV | `/index` `/search` `/semantic` | `0 2 * * *` (daily) |
| 33 | mcore-webhook | `mcore-webhook.me-419.workers.dev` | D1 + KV | `/github` `/microsoft` `/google` `/generic` | — |
| 34 | mcore-gateway | `mcore-gateway.me-419.workers.dev` | — | `/` (routes to all Workers) | — |

---

## 4. Cloudflare Pages

| # | Project | URL | Purpose | Status |
|---|---|---|---|---|
| 35 | mcore-status | `mcore-status.pages.dev` | Live health dashboard — auto-refreshes every 30s, checks all 11 services | ✅ Deployed |

---

## 5. Cloudflare Data Resources

| # | Resource | ID | Purpose |
|---|---|---|---|
| 36 | D1 Database | `mcore-evidence-store` (`b57e050d-70ba-4909-acfd-c19c1ef4c7d3`) | Evidence, policies, audit, providers, evidence_links |
| 37 | KV Namespace | `mcore-tunnel-state` (`87f9cdd65742402593687d116f7ccbf2`) | Health cache, session metadata, screenshots |
| 38 | Queue | `mcore-ingestion` (`7419ddde91d94ec48927de61a4ab5a9f`) | Async document ingestion pipeline |
| 39 | AI Search Namespace | `mcore-fabric` | Knowledge fabric search |
| 40 | AI Search Instance | `mcore-docs` (in `mcore-fabric`) | Hybrid vector + keyword search |

---

## 6. Workers AI Models

| # | Model | ID | Purpose | Status |
|---|---|---|---|---|
| 41 | Llama 3.1 8B Instruct | `@cf/meta/llama-3.1-8b-instruct` | Chat, compliance Q&A, evidence analysis | ✅ Operational |
| 42 | BGE Base EN v1.5 | `@cf/baai/bge-base-en-v1.5` | 768-dim embeddings for semantic search | ✅ Operational |

---

## 7. Zone Security Settings (Both Zones)

| # | Setting | mcoreai.dev | shorbornoai.com | What it does |
|---|---|---|---|---|
| 43 | HTTP/3 (QUIC) | ✅ ON | ✅ ON | Multiplexed streams, 0-RTT, no head-of-line blocking |
| 44 | 0-RTT | ✅ ON | ✅ ON | TLS 1.3 session resumption — skip handshake on revisit |
| 45 | Early Hints (103) | ✅ ON | ✅ ON | Preload resources before full response arrives |
| 46 | HSTS | ✅ 1yr+preload | ✅ 1yr+preload | Force HTTPS in browsers, preload list eligible |
| 47 | Min TLS Version | ✅ 1.2 | ✅ 1.2 | Reject legacy TLS 1.0/1.1 |
| 48 | Always Use HTTPS | ✅ ON | ✅ ON | 301 redirect HTTP → HTTPS at edge |
| 49 | Brotli | ✅ ON | ✅ ON | Better than gzip — smaller payloads |
| 50 | Cache Level | ✅ Aggressive | ✅ Aggressive | CDN caches all static assets |
| 51 | TLS 1.3 | ✅ ON | ✅ ON | Post-quantum key agreement |
| 52 | HTTP/2 | ✅ ON | ✅ ON | Multiplexed connections (fallback from HTTP/3) |
| 53 | SSL/TLS Mode | ✅ Full | ✅ Full | Encrypted edge-to-origin |

---

## 8. D1 Database Schema & Seed Data

### Tables

| Table | Records | Description |
|---|---|---|
| `audit_log` | 5 | Access, tunnel, DNS, AI, security events |
| `documents` | 5 | Evidence from GitHub, Microsoft, Google, local-AI, CI/CD |
| `policies` | 10 | CIA (3), SOC 2 (2), ISO 27001 (2), NIST (3) |
| `providers` | 4 | Microsoft, Google, GitHub, local-AI |
| `evidence_links` | 12 | Documents mapped to policies with confidence scores |

### Seeded Policies

| Framework | Control ID | Name | Description |
|---|---|---|---|
| CIA | C | Confidentiality | Data confidentiality through encryption and access control |
| CIA | I | Integrity | Data integrity through hashing and audit trails |
| CIA | A | Availability | System availability through redundancy and health checks |
| SOC2 | CC6.1 | Access Control | Logical access controls and MFA |
| SOC2 | CC6.7 | Audit Logging | System audit logs and monitoring |
| ISO27001 | A.10.1 | Encryption in Transit | Cryptographic protection in transit |
| ISO27001 | A.14.2 | Secure Development | Secure development practices |
| NIST | AC-2 | Access Control | Account management |
| NIST | AU-2 | Audit and Accountability | Event auditing |
| NIST | SC-8 | System Communications Protection | Transmission confidentiality |

### Seeded Providers

| Provider | Type | Status |
|---|---|---|
| microsoft | oauth | active |
| google | oauth | active |
| github | oauth | active |
| local-ai | api | active |

---

## 9. Cron Triggers

| # | Worker | Schedule | What it does |
|---|---|---|---|
| 54 | mcore-health-monitor | `*/5 * * * *` (every 5 min) | Pings all 11 services, caches results in KV |
| 55 | mcore-compliance-report | `0 0 * * *` (daily midnight UTC) | Generates compliance report, stores in KV |
| 56 | mcore-ai-search | `0 2 * * *` (daily 2am UTC) | Reindexes documents from D1 |

---

## 10. Worker Route Map (10 routes)

| # | Pattern | Worker | Purpose |
|---|---|---|---|
| 1 | `api.mcoreai.dev/*` | mcore-edge-gateway | JWT validation + audit |
| 2 | `docs.mcoreai.dev/*` | mcore-edge-gateway | JWT validation + audit |
| 3 | `ais001.mcoreai.dev/api/*` | mcore-ai-fabric | AI chat + compliance queries |
| 4 | `ais001.mcoreai.dev/data/*` | mcore-d1-api | D1 CRUD operations |
| 5 | `cf-ais001.mcoreai.dev/*` | mcore-ai-fabric | Local AI + AI Fabric |
| 6 | `report.mcoreai.dev/*` | mcore-compliance-report | Compliance reports |
| 7 | `capture.mcoreai.dev/*` | mcore-browser-collector | Screenshots + scraping |
| 8 | `search.mcoreai.dev/*` | mcore-ai-search | Document search |
| 9 | `hooks.mcoreai.dev/*` | mcore-webhook | Provider webhooks |
| 10 | `gateway.mcoreai.dev/*` | mcore-gateway | Master API router |

---

## 11. Home Network Access (WSL2)

| Service | Home LAN URL (inside WiFi) | Tunnel URL (outside home) |
|---|---|---|
| Web (Next.js) | `http://172.23.180.160:3000` | `https://ais001.mcoreai.dev` |
| API (Rust/Axum) | `http://172.23.180.160:8080` | `https://api.mcoreai.dev` |
| Ingest (FastAPI) | `http://172.23.180.160:8000` | `https://ais001.mcoreai.dev` |
| Postgres | `172.23.180.160:5432` | (tunnel only) |
| Qdrant | `http://172.23.180.160:6333` | (tunnel only) |
| SSH | `172.23.180.160:22` | `ssh.mcoreai.dev` (WARP) |
| Ollama | `http://172.23.180.160:11434` | `https://cf-ais001.mcoreai.dev` |

---

## 12. Identity

| Field | Value |
|---|---|
| Entity | Meticulous Core Inc. (MCore) |
| Founder | Aminul Islam Shamim (AIS) |
| Operator ID | MCORE-FDR-AIS-001 |
| Baseline | @AIS-DU |
| Project Domain | shorbornoai.com (DU-PROJECT) |
| Dev Sandbox | ais001.mcoreai.dev |
| Local AI | cf-ais001.mcoreai.dev |
| Contact | shorbornoai@gmail.com |
| Identity | me@aminul-du.com |
| Team Domain | mcore-fdr-ais-001.cloudflareaccess.com |
| GitHub | https://github.com/aminul-du/mcoreai.git |

---

## 13. Pending Actions (Dashboard Only)

| # | Action | Where | Why |
|---|---|---|---|
| 1 | R2 bucket `mcore-evidence-objects` | R2 → Create bucket | Credential lacks R2 write |
| 2 | Access apps for all 11 hostnames | Zero Trust → Access → Applications | Credential is read-only for Access |
| 3 | GCP Cloud Run URL for `shorbornoai.com` | Paste URL → I create CNAME | Need URL from user |
| 4 | Tunnel routes for new hostnames | Tunnels → 78d7fa3b → Public hostnames | Credential is read-only for tunnels |
| 5 | IdP setup (Google/GitHub/OTP) | Zero Trust → Settings → Authentication | Credential is read-only |
| 6 | Clone & push repo to GitHub | `git push` to aminul-du/mcoreai | Repo expires in ~36h |

---

## Summary

| Category | Count |
|---|---|
| Total DNS Records | 25 (12 CNAME + 3 MX + 3 TXT + 5 email) |
| Total Workers | 9 |
| Total Worker Routes | 10 |
| Total Tunnel CNAMEs | 12 |
| Total D1 Records | 36 (5 docs + 10 policies + 4 providers + 12 links + 5 audit) |
| Total Cron Triggers | 3 |
| Total Security Settings | 11 (both zones) |
| Total Pages | 1 |
| Total AI Models | 2 |
| Total AI Search Instances | 1 |
| **Total Live Resources** | **56** |

---

## 3. Zone: `shorborno.ai` (Sovereign Academic Research & Presentation)

**Zone ID:** `4215f8ffab32c865a0def2de7186e314`  
**Status:** Active  
**Nameservers:** `rafe.ns.cloudflare.com`, `uriah.ns.cloudflare.com`  
**Academic Alignment:** `AIS-DU-PMICS-PROJECT-SBOX` (Dhaka University)  

| # | Name | Type | Target Content | Proxied | Destination Architecture | Security & Auth |
|---|---|---|---|---|---|---|
| 22 | `docs.shorborno.ai` | CNAME | `mcore-docs.pages.dev` | 🟠 Yes | Cloudflare Pages (mcore-docs) | Edge CDN + SSL |
| 23 | `research.shorborno.ai` | CNAME | `mcore-docs.pages.dev` | 🟠 Yes | Cloudflare Pages (Bilingual Portal) | Edge CDN + SSL |
| 24 | `sbox.shorborno.ai` | CNAME | `78d7fa3b...cfargotunnel.com` | 🟠 Yes | Cloudflare Tunnel `ais001` -> `:8000` | Zero Trust Access |
| 25 | `drive.shorborno.ai` | CNAME / Rule | Edge 301 Redirect | 🟠 Yes | Google Drive `AIS-DU-PMICS-PROJECT-SBOX` | Google Workspace Auth |
