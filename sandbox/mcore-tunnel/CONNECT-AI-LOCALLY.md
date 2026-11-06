# =============================================================================
# MCORE-DOCS-001 — Connect Cloudflare AI to Your Local Environment
# 4 methods, from simplest to most advanced
# =============================================================================

## Method 1: Workers AI REST API (Simplest — works right now)

Call Cloudflare AI models directly from your local Python/JS code.
No Workers needed — just your API token.

```bash
# From your Debian/WSL terminal:
export CLOUDFLARE_API_TOKEN="your-token"
export CLOUDFLARE_ACCOUNT_ID="41903f4febb2c66dffd4ffcae558e692"

# Chat with Llama 3.1
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/meta/llama-3.1-8b-instruct" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are MCORE-DOCS-001 AI assistant."},
      {"role": "user", "content": "Explain CIA triad controls"}
    ]
  }'

# Generate embeddings
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/baai/bge-base-en-v1.5" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": ["MCORE evidence framework"]}'
```

## Method 2: AI Gateway (Recommended — caching + logging + rate limits)

AI Gateway sits between your local code and the AI models, adding:
- Request caching (save money on repeated queries)
- Logging (see every AI request)
- Rate limiting (prevent abuse)
- Analytics (tokens used, latency, cost)

### Create an AI Gateway (dashboard — 1 min)
1. Go to: https://dash.cloudflare.com/41903f4febb2c66dffd4ffcae558e692/ai/ai-gateway
2. Click "Create Gateway"
3. Name: `mcore-ai-gateway`
4. Create

### Use the gateway from local code
```bash
# The "default" gateway is auto-created on first request — no setup needed:
curl -X POST \
  "https://gateway.ai.cloudflare.com/v1/$CLOUDFLARE_ACCOUNT_ID/default/compat/chat/completions" \
  -H "cf-aig-authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "workers-ai/@cf/meta/llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "What are NIST 800-53 audit controls?"}]
  }'
```

## Method 3: Your mcore-ai-fabric Worker (Already deployed!)

You already have a Worker that wraps Workers AI + D1 + compliance queries.
Call it from your local code:

```bash
# Chat with the compliance AI
curl -X POST https://mcore-ai-fabric.me-419.workers.dev/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Summarize ISO 27001 access controls"}]}'

# Query compliance policies from D1
curl https://mcore-ai-fabric.me-419.workers.dev/compliance?framework=NIST

# Generate embeddings for local use
curl -X POST https://mcore-ai-fabric.me-419.workers.dev/embed \
  -H "Content-Type: application/json" \
  -d '{"texts":["evidence document text"]}'
```

## Method 4: Connect Local AI (Ollama) through Cloudflare Tunnel

Run AI models locally on your Debian/WSL box and expose them through the tunnel.

### Step 1: Install Ollama on WSL
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
ollama serve  # runs on localhost:11434
```

### Step 2: Add to tunnel config
In your Cloudflare Tunnel dashboard, add a public hostname:
- Subdomain: `ai`
- Domain: `mcoreai.dev`
- Service: `http://localhost:11434`

Or in cloudflared config:
```yaml
ingress:
  - hostname: ai.mcoreai.dev
    service: http://localhost:11434
  - service: http_status:404
```

### Step 3: Create DNS record (I can do this!)
The CNAME `ai.mcoreai.dev` → tunnel 78d7fa3b

### Step 4: Protect with Access
Create an Access app for `ai.mcoreai.dev` so only you can use it.

### Step 5: Call your local AI from anywhere
```bash
# From any device, through Cloudflare:
curl -X POST https://ai.mcoreai.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.1","messages":[{"role":"user","content":"Hello from Cloudflare!"}]}'
```

### Step 6: Register as AI Gateway Custom Provider
In AI Gateway → Custom Providers, add:
- Name: `local-ollama`
- Base URL: `https://ai.mcoreai.dev`
- Auth: Access service token

Then route through the gateway:
```bash
curl -X POST \
  "https://gateway.ai.cloudflare.com/v1/$CLOUDFLARE_ACCOUNT_ID/mcore-ai-gateway/custom/local-ollama/v1/chat/completions" \
  -H "cf-aig-authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"model":"llama3.1","messages":[{"role":"user","content":"Hi"}]}'
```

## Architecture: All AI paths

```
Your Local Code (Python/JS/CLI)
    │
    ├──► Method 1: Direct REST API ──────► Workers AI (Llama 3.1, BGE)
    │                                     (no gateway, no caching)
    │
    ├──► Method 2: AI Gateway ───────────► Workers AI (cached, logged)
    │     gateway.ai.cloudflare.com        (rate limited, analytics)
    │
    ├──► Method 3: Your Worker ──────────► mcore-ai-fabric Worker
    │     mcore-ai-fabric.workers.dev       (D1 + compliance + AI)
    │
    └──► Method 4: Local AI (Ollama) ────► ai.mcoreai.dev (tunnel)
          localhost:11434                   (your own model, private)
                │
                └──► AI Gateway Custom Provider (optional, for logging)
```
