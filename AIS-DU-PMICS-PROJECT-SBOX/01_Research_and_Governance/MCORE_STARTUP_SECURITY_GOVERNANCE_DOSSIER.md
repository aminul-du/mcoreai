# 🛡️ MCore Executive Startup Security & Governance Dossier
## End-to-End Enterprise Compliance, Cloud IAM Identity Architecture, Runtime Boundaries & Policy Engine Guardrails
**Document Reference:** `MCORE-DOSSIER-SEC-001`  
**Classification:** Venture-Ready / Confidential Academic & Startup Record  
**Founder & Final Authority:** Aminul Islam Shamim (AIS) | ID: `MCORE-FDR-AIS-001`  
**Host Target:** `mcorebd` (Debian 13 Trixie / Sovereign Bare-Metal Architecture)  
**Academic Anchor:** `AIS-DU-PMICS-PROJECT-SBOX` (Dhaka University PMICS)  
**Primary Venture Initiative:** MCore Agent Platform & ShorbornoAI Knowledge Engine  
**Last Audited:** November 9, 2026 (UTC)  

---

## 1. Executive Prologue: Startup Program & Enterprise Audit Readiness

To compete successfully in premier startup accelerators (Y Combinator, Techstars, Google for Startups) and pass institutional vendor risk assessments (SOC2 Type II, ISO/IEC 27001, CIS Cloud Benchmarks), an AI startup cannot treat security as an afterthought.

Most early-stage AI ventures stumble on three predictable failure modes:
1. **Uncontained Blast Radius:** Code running as `root` in production, allowing a single prompt injection or dependency vulnerability to escalate into total host takeover.
2. **Static Cloud Credential Leakage:** Hardcoded Google Cloud Service Account `.json` keys committed to Git or embedded in container images.
3. **Agentic Over-Privilege:** AI coding agents executing unconstrained shell commands, creating unintended cloud bills, or modifying production infrastructure without cryptographic oversight.

This dossier establishes the official, audit-ready operational standard for **MCore**, defining the exact technical boundaries between root and unprivileged runtimes, auditing Google Cloud Identity & Access Management (IAM), and enforcing strict policy-engine guardrails for AI development agents.

---

## 2. Google Cloud Service Accounts & IAM: End-to-End Gap Analysis

### 2.1 What Information We Already Have (Empirical System Audit)

A live query of the active Google Cloud environment on host `mcorebd` yielded the following verified baseline:

* **Active GCP Project:** `project-12884862-2ba9-4048-b03`
* **Primary Developer Identity:** `aminulcse7@gmail.com` (Role: `roles/owner`)
* **Local Authentication Protocol:** Application Default Credentials (`ADC`) anchored via `authorized_user` OAuth 2.0 refresh tokens in `~/.config/gcloud/application_default_credentials.json`.
* **Static Key Audit:** **100% Zero-Static Key State.** An exhaustive scan of `/home/mcoreai` and `/srv` confirmed **zero** `.json` service account private keys stored on disk.
* **Registered Service Accounts:**
  1. `469173990872-compute@developer.gserviceaccount.com` (Default Compute Service Account)
     - Keys: `d095ab2edfa1...` (`SYSTEM_MANAGED`, auto-rotated by Google).
     - IAM Bindings:
       - `roles/artifactregistry.writer` (Container push privileges)
       - `roles/run.sourceDeveloper` (Cloud Run deployment privileges)
       - `roles/secretmanager.secretAccessor` (Secret retrieval)
       - `roles/storage.objectAdmin` (Full GCS bucket lifecycle access)
  2. `ais-gemini-key-f5f770c17f9c41a@469173990872.iam.gserviceaccount.com`
     - Keys: `c743b9049f...` & `eaaf08c77c...` (Both `SYSTEM_MANAGED`).
     - Role Bindings: No project-level IAM roles bound directly (scoped to specific resource level or unassigned).
* **Live Serverless Ingress:** `https://shorbornoai-launch-469173990872.us-central1.run.app/` (Google Cloud Run).

---

### 2.2 What the Actual Core Gaps Are (Vulnerability Scope)

While having zero user-managed JSON keys is a major security asset, an enterprise-level audit identifies **four critical gaps**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              IDENTIFIED GCP SECURITY GAPS                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP A: Over-Scoped Default Compute Service Account                                     │
│ • 469173990872-compute holds storage.objectAdmin + secretAccessor simultaneously.      │
│ • If Cloud Run runs as this account, a container escape exposes all buckets & secrets. │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP B: Unassigned / Orphaned Service Account (ais-gemini-key)                          │
│ • Account exists with two active keys but no documented project-level IAM roles.       │
│ • Lacks explicit Principle of Least Privilege (PoLP) scoping for Gemini/Vertex API.    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP C: Absence of Workload Identity Federation (WIF) for CI/CD                         │
│ • GitHub Actions (.github/workflows/) currently lacks OIDC Workload Identity pools.    │
│ • Risks engineers creating static JSON keys in the future to enable CI/CD pipelines.  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GAP D: Lack of Organization Policy Constraints                                         │
│ • constraints/iam.disableServiceAccountKeyCreation is not enforced.                   │
│ • Any team member with IAM admin could accidentally generate an unrotated key.         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.3 What You Need to Share Next (Founder Decision Points)

To complete the hardening of your Google Cloud IAM posture, please review and provide:

1. **Intended Role of `ais-gemini-key`:**  
   Is `ais-gemini-key-f5f770c17f9c41a` intended solely for the Gemini Developer API / Vertex AI inference in `terminal-ai`, or is it linked to ShorbornoAI Cloud Run?
2. **Cloud Run Runtime Identity:**  
   Confirm which service account is attached to `shorbornoai-launch`:
   ```bash
   gcloud run services describe shorbornoai-launch --region=us-central1 --format="value(spec.template.spec.serviceAccountName)"
   ```
3. **CI/CD Deployment Strategy:**  
   Do you want GitHub Actions to deploy directly to Google Cloud Run and Cloudflare Workers, or will deployments remain orchestrated locally from `mcorebd` via `setup_master_devops_deploy.sh`?

---

### 2.4 Quick "What To Do" Roadmap (Immediate Action Items)

| Timeline | Action Item | Target & Command |
| :--- | :--- | :--- |
| **Immediate** | **Scope a Dedicated Runtime Service Account for Cloud Run** | Create `mcore-cloudrun-sa@...` with only `roles/aiplatform.user` and necessary Secret Accessor permissions instead of using the Default Compute SA. |
| **Week 1** | **Lock Down Secret Manager Access** | Bind `roles/secretmanager.secretAccessor` strictly to specific secrets rather than project-wide. |
| **Week 2** | **Implement Workload Identity Federation** | Bind GitHub repo `aminul-du/mcoreai` to a GCP WIF pool, eliminating any future need for static keys in GitHub Secrets. |
| **Week 3** | **Enforce Organization Key Creation Ban** | Apply `constraints/iam.disableServiceAccountKeyCreation` at the project level. |

---

## 3. Architectural Demarcation: Root vs. Normal Development Environment

A non-negotiable requirement for both system reliability and startup compliance is establishing a **hard structural boundary** between the root-controlled sovereign system layer and the unprivileged developer space.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                 SOVEREIGN LAYERED RUNTIME TOPOLOGY ON HOST: mcorebd                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: ROOT HOST OS & INFRASTRUCTURE (/etc, /usr, /dev, systemd)                    │
│  • Authority: root (UID 0) strictly via explicit, audited sudo                         │
│  • Scope: Kernel, apt-get, /etc/systemd/system/*.service, volatile /dev/MCore link    │
│  • RULE: NO AI AGENT OR DEV SCRIPT EVER WRITES DIRECTLY TO THIS LAYER.                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: SOVEREIGN PRODUCTION RUNTIME (/srv/mcore/mcore365 & /srv/aiseye)             │
│  • Authority: mcoreai (UID 1000)                                                       │
│  • Daemons: mcoresec-api (:8000), mcoresec-mte (:8100), terminal-ai (:8200), Colab    │
│  • RULE: Zero ad-hoc file edits. Only receives verified, tagged DevOps promotions.     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: UNPRIVILEGED DEV & WORKSPACE SANDBOX (/home/mcoreai)                         │
│  • Authority: mcoreai (UID 1000)                                                       │
│  • Tools: pnpm 9, Turborepo, Wrangler Edge Workers, Git, Python testing venvs         │
│  • RULE: All day-to-day coding, feature branches, and AI agent experimentation.        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 The Principle of Least Privilege (PoLP) Matrix

| Operation Category | Permitted User | Privilege Level | Rationale |
| :--- | :--- | :--- | :--- |
| **Editing Application Code / Tests** | `mcoreai` | Unprivileged (`UID 1000`) | Code edits should never have system partition access. |
| **Running LLM Inference / Notebooks** | `mcoreai` | Unprivileged (`UID 1000`) | Prompt injection RCE cannot escape into root. |
| **Git Operations (`commit`, `push`)** | `mcoreai` | Unprivileged (`UID 1000`) | SSH keys (`id_ed25519`) owned by `mcoreai`. |
| **Systemd Daemon Restarts** | `mcoreai` | `sudo systemctl reload-or-restart` | Controlled system lifecycle operations only. |
| **OS Package Upgrades (`apt`)** | `root` | Explicit `sudo` by AIS | System integrity protection. |
| **Modifying `/etc/systemd/system/`** | `root` | Explicit `sudo` by AIS | Service definition changes require founder sign-off. |

### 3.2 Production Container Parity (Cloud Run & Kubernetes Readiness)
To ensure seamless migration from local bare-metal to cloud container environments:
* Every Dockerfile in `sandbox/` and `mcoresec/` must declare:
  ```dockerfile
  RUN adduser --disabled-password --gecos "" --uid 1000 mcoreai
  USER 1000:1000
  ```
* Running as unprivileged `UID 1000` satisfies Google Cloud Run, AWS Fargate, and Kubernetes Pod Security Standards (`PSS: Restricted`) out of the box.

---

## 4. Gemini CLI Security Controls, Folder Trust & Policy Engine

*Based on official specifications: [Gemini CLI Policy Engine](https://geminicli.com/docs/reference/policy-engine/) • [Trusted Folders](https://geminicli.com/docs/cli/trusted-folders/) • [Commands Reference](https://geminicli.com/docs/reference/commands/)*

The Gemini CLI includes an enterprise-grade security policy engine supporting 5 hierarchical tiers:
* **Tier 1 (Default):** Built-in read-only defaults.
* **Tier 2 (Extension):** Extension-level rules.
* **Tier 3 (Workspace):** `.gemini/policies/` *(currently disabled upstream)*.
* **Tier 4 (User):** `~/.gemini/policies/*.toml` (Enforced across all sessions).
* **Tier 5 (Admin):** System-wide root-owned policies (`/etc/gemini-cli/policies`).

### 4.1 Folder Trust Governance (`~/.gemini/trustedFolders.json`)

Folder trust prevents malicious repositories from automatically executing custom hooks, loading `.env` credentials, or connecting unverified MCP servers.

**Policy Directive for MCore:**
* `/srv/mcore/mcore365` $\rightarrow$ `TRUST_FOLDER` (Verified sovereign production core).
* `/home/mcoreai` $\rightarrow$ `TRUST_FOLDER` (Verified developer workspace).
* Any newly cloned, external, or third-party repository must initially remain `DO_NOT_TRUST` until audited via `/permissions trust`.

---

### 4.2 The "Allow for all future sessions" Golden Rule

Gemini CLI allows persistent tool approval (`security.enablePermanentToolApproval`), which automatically adds rules to `~/.gemini/policies/`.

**The MCore Sovereign Rule:**
> **"Allow for all future sessions" is strictly restricted to narrowly scoped, routine, read-only actions you completely understand (e.g. `git status`, `git log`, read tools).**  
> **Destructive commands, deployments, credential changes, paid cloud provisioning, and external side effects MUST remain subject to explicit manual approval every single time.**

#### What May Be Auto-Approved:
- Read-only filesystem operations (`read_file`, `grep_search`, `glob`, `list_directory`).
- Safe local inspection commands (`git status`, `git log`, `git branch`, `node -v`, `python3 --version`).

#### What MUST Require Explicit Human Approval:
- **Destructive File/DB Commands:** `rm`, `rm -rf`, `git reset --hard`, `git clean -fd`, `dropdb`, `truncate`.
- **Deployments & Infrastructure:** `terraform apply`, `wrangler deploy`, `gcloud run deploy`, `docker push`.
- **Credential & Secret Access:** `gcloud auth`, `passwd`, `ssh-keygen`, reading `.env` files or API keys.
- **Paid Cloud Resources:** Cloud Run scaling mutations, Vertex AI model endpoint creation, Cloudflare paid add-ons.

---

### 4.3 Recommended Settings File (`~/.gemini/settings.json`)

To apply these principles directly to your Gemini CLI environment:

```json
{
  "$schema": "https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json",
  "general": {
    "defaultApprovalMode": "default"
  },
  "security": {
    "auth": {
      "selectedType": "vertex-ai"
    },
    "folderTrust": {
      "enabled": true
    },
    "disableYoloMode": true,
    "disableAlwaysAllow": false,
    "enablePermanentToolApproval": true,
    "autoAddToPolicyByDefault": false,
    "environmentVariableRedaction": {
      "enabled": true,
      "blocked": [
        "CLOUDFLARE_API_TOKEN",
        "GITHUB_TOKEN",
        "GEMINI_API_KEY",
        "DATABASE_URL",
        "POSTGRES_PASSWORD"
      ]
    }
  },
  "tools": {
    "confirmationRequired": [
      "write_file",
      "replace"
    ]
  }
}
```

---

### 4.4 User Guardrail Policy Definition (`~/.gemini/policies/mcore-guardrails.toml`)

This Tier 4 User Policy file enforces persistent safety rules across all modes:

```toml
# ==============================================================================
# MCORE SOVEREIGN SECURITY GUARDRAILS POLICY (TIER 4 USER POLICY)
# Location: ~/.gemini/policies/mcore-guardrails.toml
# ==============================================================================

# 1. READ-ONLY ROUTINE ACTIONS: AUTO-ALLOWED
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["git status", "git log", "git branch", "git diff", "uname", "uptime", "free", "df"]
decision = "allow"
priority = 200
modes = ["default", "autoEdit", "plan", "yolo"]

# 2. FILE WRITE OPERATIONS: REQUIRE USER CONFIRMATION
[[rule]]
toolName = ["write_file", "replace"]
decision = "ask_user"
priority = 300

# 3. HIGH-RISK DESTRUCTIVE COMMANDS: REQUIRE EXPLICIT APPROVAL
[[rule]]
toolName = "run_shell_command"
commandPrefix = [
  "rm", 
  "rmdir", 
  "git reset", 
  "git clean", 
  "dropdb", 
  "psql -c DROP", 
  "mkfs", 
  "dd"
]
decision = "ask_user"
priority = 600

# 4. CATASTROPHIC COMMANDS: UNCONDITIONALLY BLOCKED
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["rm -rf /", "rm -rf /srv", "rm -rf /home"]
decision = "deny"
priority = 999
denyMessage = "Catastrophic recursive deletion of sovereign root paths is forbidden."

# 5. CLOUD INFRASTRUCTURE & DEPLOYMENTS: REQUIRE FOUNDER CONFIRMATION
[[rule]]
toolName = "run_shell_command"
commandPrefix = [
  "gcloud", 
  "terraform", 
  "wrangler deploy", 
  "docker push", 
  "systemctl stop", 
  "systemctl disable"
]
decision = "ask_user"
priority = 500

# 6. CREDENTIAL ACCESS & PRIVILEGE ESCALATION: REQUIRE EXPLICIT APPROVAL
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["sudo", "su", "passwd", "ssh-keygen", "gcloud auth login"]
decision = "ask_user"
priority = 700

# 7. REDIRECTION SAFETY
# By default, shell redirection operators (>, >>) trigger manual approval 
# to protect existing files from accidental overwrites.
```

---

## 5. Collaborative DevOps & Research Operating Protocol

As Founder & Lead Architect (@AIS) collaborating with the MCore Architecture Engine:

1. **Strategic Intent Precedence:**  
   Every major architectural mutation is proposed, validated against non-destructive doctrines, and documented prior to execution.
2. **Double-Sided Verification:**  
   No feature or security fix is deemed complete without empirical socket verification (`ss -tuln`), service status checks (`systemctl status`), and regression tests.
3. **Audit Evidence Persistence:**  
   All validation logs and experiment outputs are recorded with SHA-256 hashes under `AIS-DU-PMICS-PROJECT-SBOX/05_Evidence_and_Validation/` to maintain a tamper-proof record for Dhaka University faculty supervisors and future startup due-diligence auditors.

---

**Authored and Certified by MCore Architecture Engine on behalf of Founder Aminul Islam Shamim (AIS).**
