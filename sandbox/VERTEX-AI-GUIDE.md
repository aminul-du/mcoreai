# ⚠ MCORE-DOCS-001 — Vertex AI Local Integration Guide
## Work Carefully: Security, Cost, and Compliance Warnings

**Document:** MCORE-VERTEX-001
**Author:** Aminul Islam Shamim (MCORE-FDR-AIS-001)
**Date:** 2026-11-06
**Classification:** Internal — Sensitive Configuration

---

## ⚠ CRITICAL WARNINGS — Read Before Proceeding

### 1. Credential Exposure Risk

> **Vertex AI requires Google Cloud service account keys (JSON).**
> If these keys leak, an attacker can:
> - Incur unlimited GCP charges on your billing account
> - Access all Google Cloud resources the service account can see
> - Exfiltrate data from BigQuery, GCS, and other GCP services
> - Create persistent backdoors via new service accounts

**Mitigation:**
- ❌ NEVER commit the service account JSON to git
- ❌ NEVER store it in environment variables visible to `docker inspect`
- ✅ Store in Cloudflare Secrets Store or a sealed file with `chmod 600`
- ✅ Use Workload Identity Federation instead of keys where possible
- ✅ Rotate keys every 90 days maximum
- ✅ Set the service account to minimum-privilege (only `aiplatform.user`)

### 2. Cost Explosion Risk

> **Vertex AI charges per token, per request, per model.**
> Unlike Workers AI (fixed free tier) or Ollama (free local), Vertex AI bills:
> - Gemini 1.5 Pro: ~$7.00 per 1M input tokens, ~$21.00 per 1M output tokens
> - Gemini 1.5 Flash: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
> - Imagen 3: ~$0.03 per image generated
> - Text embeddings: ~$0.025 per 1M tokens

**Mitigation:**
- ✅ Set GCP billing budgets and alerts (Budgets → $10/day hard cap)
- ✅ Use the `gemini-1.5-flash` model for most tasks (100x cheaper than Pro)
- ✅ Implement request caching in Cloudflare KV (avoid duplicate API calls)
- ✅ Set `max_output_tokens` on every request
- ✅ Monitor usage via `gcloud billing` and Cloudflare AI Gateway analytics
- ✅ Use the AI Gateway as a proxy — it logs every request with cost estimates

### 3. Data Privacy & Compliance Risk

> **Vertex AI processes data in Google Cloud regions.**
> Your evidence documents may contain:
> - PII (personally identifiable information)
> - Security control details (CIA, SOC 2, ISO 27001, NIST)
> - Internal architecture details
> - API keys and credentials embedded in documents

**Mitigation:**
- ✅ Enable Vertex AI data residency in your preferred region
- ✅ Do NOT send raw credentials, API keys, or secrets to Vertex AI
- ✅ Redact sensitive data before sending to Vertex AI
- ✅ Use Google's Customer-Managed Encryption Keys (CMEK)
- ✅ Disable Vertex AI data logging: `gcloud ai platforms update --data-logging=false`
- ✅ Review Google's Data Processing Addendum (DPA) for your jurisdiction
- ✅ For GDPR/HIPAA data: use Vertex AI in EU regions only

### 4. Network Exposure Risk

> **Exposing Vertex AI through a public tunnel endpoint means anyone with the URL can call it.**

**Mitigation:**
- ✅ ALWAYS protect the Vertex AI proxy endpoint with Cloudflare Access
- ✅ Use a Service Token for machine-to-machine calls
- ✅ Rate-limit the endpoint via Cloudflare WAF (e.g., 100 req/min)
- ✅ Add request validation in the Worker (reject empty/oversized payloads)
- ✅ Log every request to D1 audit_log with actor + timestamp

---

## Architecture: Vertex AI in Your Stack

```
Your Local Code / Workers
    │
    ├──► Cloudflare AI Gateway (mcore-ai-gateway)
    │       │
    │       ├──► Workers AI (Llama 3.1) — free tier, fast, no data leaves CF
    │       ├──► Local Ollama (llama3.1) — free, private, on your WSL
    │       └──► Vertex AI (Gemini 1.5) — ⚠ paid, powerful, data goes to GCP
    │
    └── When to use which:
         ├── Simple Q&A, compliance lookup → Workers AI (free)
         ├── Private/sensitive data → Local Ollama (stays on your machine)
         └── Complex reasoning, multimodal, large context → Vertex AI (paid)
```

---

## Step-by-Step: Connect Vertex AI Locally

### Step 1: Create a GCP Service Account (Minimum Privilege)

```bash
# Set your GCP project
export GCP_PROJECT="mcore-ai"
export GCP_REGION="us-central1"

# Create a dedicated service account (NOT your main account)
gcloud iam service-accounts create mcore-vertex-ai \
  --display-name="MCORE Vertex AI (minimal access)"

# Grant ONLY Vertex AI user role (nothing else)
gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:mcore-vertex-ai@${GCP_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Generate a key (this is the ONLY time you'll do this)
gcloud iam service-accounts keys create ~/mcore-vertex-key.json \
  --iam-account=mcore-vertex-ai@${GCP_PROJECT}.iam.gserviceaccount.com

# SECURE THE KEY
chmod 600 ~/mcore-vertex-key.json
mv ~/mcore-vertex-key.json ~/.config/mcore/vertex-key.json
```

### Step 2: Store the Key Securely (NOT in .env)

```bash
# Option A: Cloudflare Secrets Store (recommended for Workers)
# Upload via dashboard: Zero Trust → Secrets Store → Add secret
# Name: GCP_VERTEX_KEY
# Value: <contents of vertex-key.json>

# Option B: Sealed file on WSL (for local Python only)
mkdir -p ~/.config/mcore
cp ~/mcore-vertex-key.json ~/.config/mcore/vertex-key.json
chmod 600 ~/.config/mcore/vertex-key.json
# Add to .gitignore: ~/.config/mcore/
```

### Step 3: Create a Vertex AI Proxy Worker

```javascript
// workers/mcore-vertex-proxy/src/index.js
// ⚠ This Worker proxies to Vertex AI — protect with Access!

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === "/__health") {
      return Response.json({ status: "healthy", service: "mcore-vertex-proxy" });
    }

    // ⚠ Require Access JWT
    const jwt = request.headers.get("cf-access-jwt-assertion");
    if (!jwt) {
      return Response.json({ error: "Access JWT required" }, { status: 401 });
    }

    // Chat endpoint — Gemini 1.5 Flash (cheaper)
    if (url.pathname === "/gemini" && request.method === "POST") {
      const { messages, model, max_tokens } = await request.json();

      // ⚠ Validate input
      if (!messages || !Array.isArray(messages)) {
        return Response.json({ error: "messages array required" }, { status: 400 });
      }
      const maxOut = Math.min(max_tokens || 1024, 4096); // Hard cap

      // ⚠ Redact potential secrets from input
      const sanitized = messages.map(m => ({
        ...m,
        content: m.content
          .replace(/sk-[a-zA-Z0-9]{20,}/g, "[REDACTED]")
          .replace(/eyJ[a-zA-Z0-9._-]+/g, "[REDACTED-JWT]")
          .replace(/AKIA[A-Z0-9]{16}/g, "[REDACTED-AWS]")
      }));

      // Call Vertex AI via REST API
      const projectId = env.GCP_PROJECT_ID;
      const region = env.GCP_REGION || "us-central1";
      const modelName = model || "gemini-1.5-flash-002";
      const token = env.GCP_ACCESS_TOKEN; // Short-lived, rotated

      const vertexUrl = `https://${region}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${region}/publishers/google/models/${modelName}:generateContent`;

      try {
        const vertexResp = await fetch(vertexUrl, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            contents: sanitized.map(m => ({
              role: m.role === "assistant" ? "model" : "user",
              parts: [{ text: m.content }]
            })),
            generationConfig: {
              maxOutputTokens: maxOut,
              temperature: 0.7,
            },
            safetySettings: [
              { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_ONLY_HIGH" },
              { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_ONLY_HIGH" },
            ]
          })
        });

        const vertexData = await vertexResp.json();

        // ⚠ Log to D1 audit
        try {
          await env.MCORE_D1.prepare(
            "INSERT INTO audit_log (event_type, actor, action, resource, status, created_at) VALUES (?,?,?,?,?,?)"
          ).bind("vertex-ai", "proxy", "gemini", modelName, "ok", new Date().toISOString()).run();
        } catch (e) {}

        // ⚠ Log token usage for cost tracking
        const usage = vertexData.usageMetadata || {};
        try {
          await env.MCORE_KV.put(
            `vertex-usage:${Date.now()}`,
            JSON.stringify({
              model: modelName,
              input_tokens: usage.promptTokenCount || 0,
              output_tokens: usage.candidatesTokenCount || 0,
              total_tokens: usage.totalTokenCount || 0,
              timestamp: new Date().toISOString()
            }),
            { expirationTtl: 604800 } // 7 days
          );
        } catch (e) {}

        return Response.json({
          response: vertexData.candidates?.[0]?.content?.parts?.[0]?.text || "",
          model: modelName,
          usage: usage,
          source: "vertex-ai"
        });

      } catch (err) {
        return Response.json({ error: err.message, hint: "Check GCP credentials and quota" }, { status: 502 });
      }
    }

    return Response.json({ endpoints: ["/gemini", "/__health"] });
  },
};
```

### Step 4: Vertex AI Proxy wrangler.toml

```toml
name = "mcore-vertex-proxy"
main = "src/index.js"
compatibility_date = "2026-11-01"

[[kv_namespaces]]
binding = "MCORE_KV"
id = "87f9cdd65742402593687d116f7ccbf2"

[[d1_databases]]
binding = "MCORE_D1"
database_name = "mcore-evidence-store"
database_id = "b57e050d-70ba-4909-acfd-c19c1ef4c7d3"

# ⚠ GCP credentials — use Secrets Store, NOT wrangler.toml vars
# Set via: wrangler secret put GCP_PROJECT_ID
# Set via: wrangler secret put GCP_ACCESS_TOKEN
# Set via: wrangler secret put GCP_REGION

# Route: vertex.mcoreai.dev/* → this worker
```

### Step 5: Local Python Client (Safe Usage)

```python
#!/usr/bin/env python3
"""
MCORE Vertex AI Local Client — Safe Usage
Use this instead of calling Vertex AI directly.
"""

import os
import json
import httpx
from pathlib import Path

# ⚠ Load GCP key from secure file, NOT environment variable
KEY_PATH = Path.home() / ".config" / "mcore" / "vertex-key.json"

def get_access_token():
    """Get a short-lived access token from the service account key."""
    if not KEY_PATH.exists():
        raise FileNotFoundError(
            f"Vertex AI key not found at {KEY_PATH}. "
            "Run the setup script first. NEVER commit this key."
        )

    key_data = json.loads(KEY_PATH.read_text())

    # Use Google Auth library (install: pip install google-auth)
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request

    credentials = service_account.Credentials.from_service_account_file(
        str(KEY_PATH),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(Request())
    return credentials.token

def chat_with_gemini(prompt: str, model: str = "gemini-1.5-flash-002"):
    """
    Chat with Gemini via Vertex AI.
    ⚠ This costs money. Monitor your GCP billing.
    ⚠ Your prompt data goes to Google Cloud.
    """
    token = get_access_token()
    project = os.getenv("GCP_PROJECT_ID", "mcore-ai")
    region = "us-central1"

    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project}/locations/{region}/publishers/google/models/{model}:generateContent"

    # ⚠ Redact secrets from prompt
    import re
    safe_prompt = prompt
    safe_prompt = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[REDACTED]', safe_prompt)
    safe_prompt = re.sub(r'eyJ[a-zA-Z0-9._-]+', '[REDACTED-JWT]', safe_prompt)
    safe_prompt = re.sub(r'AKIA[A-Z0-9]{16}', '[REDACTED-AWS]', safe_prompt)

    resp = httpx.post(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }, json={
        "contents": [{"role": "user", "parts": [{"text": safe_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 1024,  # ⚠ Hard cap to control cost
            "temperature": 0.7,
        }
    }, timeout=30.0)

    data = resp.json()
    return {
        "response": data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", ""),
        "usage": data.get("usageMetadata", {}),
        "model": model,
        "cost_warning": "⚠ This request was billed to your GCP account"
    }

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) or "What are NIST 800-53 audit controls?"
    result = chat_with_gemini(prompt)
    print(result["response"])
    print(f"\n{result['cost_warning']}")
    print(f"Tokens: {result['usage']}")
```

### Step 6: Register Vertex AI as AI Gateway Custom Provider

```bash
# In Cloudflare AI Gateway dashboard:
# AI Gateway → mcore-ai-gateway → Custom Providers → Add
#   Name: vertex-ai
#   Base URL: https://vertex.mcoreai.dev (your Worker proxy)
#   Auth: Access Service Token

# Then call via gateway (cached + logged + rate-limited):
curl -X POST \
  "https://gateway.ai.cloudflare.com/v1/41903f4febb2c66dffd4ffcae558e692/mcore-ai-gateway/custom/vertex-ai/v1/gemini" \
  -H "cf-aig-authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Summarize ISO 27001"}]}'
```

---

## ⚠ Pre-Deployment Checklist

Before enabling Vertex AI in production, verify ALL of these:

- [ ] GCP billing budget set to $10/day hard cap
- [ ] GCP billing alerts configured (email + SMS at 50%, 90%, 100%)
- [ ] Service account has ONLY `roles/aiplatform.user` (nothing else)
- [ ] Service account key stored in `~/.config/mcore/vertex-key.json` with `chmod 600`
- [ ] Key file added to `.gitignore`
- [ ] Vertex AI data logging disabled (`--data-logging=false`)
- [ ] Vertex AI proxy Worker deployed with Access protection
- [ ] WAF rate limit rule set on `vertex.mcoreai.dev` (100 req/min max)
- [ ] D1 audit logging enabled for all Vertex AI requests
- [ ] KV usage tracking enabled (token counts stored per request)
- [ ] Secret redaction filter active (sk-, eyJ, AKIA patterns)
- [ ] `maxOutputTokens` hard cap set to 4096 on every request
- [ ] Default model is `gemini-1.5-flash-002` (NOT Pro — 100x cheaper)
- [ ] Data residency region selected (EU for GDPR, US otherwise)
- [ ] Google DPA reviewed and accepted for your jurisdiction

---

## ⚠ When NOT to Use Vertex AI

| Scenario | Use Instead | Why |
|---|---|---|
| Simple compliance Q&A | Workers AI (Llama 3.1) | Free, fast, no data leaves Cloudflare |
| Sensitive/PII data | Local Ollama (llama3.1) | Data stays on your WSL, never leaves |
| Document embeddings | Workers AI (BGE) | Free, 768-dim, works with AI Search |
| Code generation | Workers AI (Llama 3.1) | Free, sufficient for most tasks |
| Testing/development | Local Ollama | Free, unlimited, private |
| Batch processing | Workers AI | Free tier covers most workloads |

## ⚠ When to Use Vertex AI (Carefully)

| Scenario | Model | Estimated Cost |
|---|---|---|
| Multimodal (image + text) | Gemini 1.5 Pro | ~$0.01 per image |
| Very long context (1M+ tokens) | Gemini 1.5 Pro | ~$7 per 1M tokens |
| Complex reasoning (better than Llama 3.1) | Gemini 1.5 Flash | ~$0.075 per 1M tokens |
| Code completion (high quality) | Gemini 1.5 Flash | ~$0.075 per 1M tokens |
| Image generation | Imagen 3 | ~$0.03 per image |

---

## ⚠ Emergency: Disable Vertex AI

If you see unexpected charges or a credential leak:

```bash
# 1. Immediately revoke the service account key
gcloud iam service-accounts keys delete <KEY_ID> \
  --iam-account=mcore-vertex-ai@mcore-ai.iam.gserviceaccount.com

# 2. Disable the Worker route
# Dashboard: Workers Routes → vertex.mcoreai.dev/* → Delete

# 3. Remove the DNS record
# Dashboard: DNS → vertex.mcoreai.dev → Delete

# 4. Check audit logs for unauthorized usage
curl https://mcore-compliance-report.me-419.workers.dev/audit?limit=200 | python3 -m json.tool

# 5. Check GCP billing
gcloud billing projects describe $GCP_PROJECT

# 6. Rotate ALL secrets if key was exposed
# - Cloudflare API token
# - GCP service account
# - Any credentials that were in the same .env file
```

---

## Summary: The Safe Path

```
1. Start with Workers AI (free) for everything
2. Add Local Ollama for sensitive/private data
3. Add Vertex AI ONLY when you need:
   - Multimodal capabilities (images)
   - Very long context (1M+ tokens)
   - Higher quality reasoning than Llama 3.1
4. ALWAYS route Vertex AI through:
   - Cloudflare AI Gateway (logging + caching)
   - Your proxy Worker (Access + redaction + audit)
   - D1 audit log (every request tracked)
5. Monitor GCP billing DAILY for the first month
6. Set a $10/day hard cap on GCP billing
7. Rotate the service account key every 90 days
```

**Remember: Workers AI and Ollama are free. Vertex AI is not. Start free, add paid only when needed.**
