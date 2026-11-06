#!/usr/bin/env python3
"""
MCORE-DOCS-001 — Local AI Connector
Connects your local Python environment to Cloudflare AI (4 methods).

Usage:
    python mcore_local_ai.py chat "Explain CIA triad controls"
    python mcore_local_ai.py embed "evidence document text"
    python mcore_local_ai.py compliance NIST
    python mcore_local_ai.py compliance
    python mcore_local_ai.py providers
    python mcore_local_ai.py stats
    python mcore_local_ai.py local "Hello from Ollama"  # via tunnel
"""
import os
import sys
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "41903f4febb2c66dffd4ffcae558e692")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
FABRIC_URL = "https://mcore-ai-fabric.me-419.workers.dev"
GATEWAY_URL = f"https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/default"
LOCAL_AI_URL = os.getenv("LOCAL_AI_URL", "https://cf-ais001.mcoreai.dev")  # via tunnel


def method1_direct(prompt: str):
    """Method 1: Direct Workers AI REST API"""
    print("[Method 1] Direct Workers AI REST API")
    resp = httpx.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct",
        headers={"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"},
        json={"messages": [
            {"role": "system", "content": "You are MCORE-DOCS-001 AI assistant for evidence and compliance."},
            {"role": "user", "content": prompt}
        ], "max_tokens": 500},
        timeout=30.0
    )
    data = resp.json()
    if data.get("success"):
        print(data["result"]["response"])
    else:
        print(f"Error: {data.get('errors')}")


def method2_gateway(prompt: str):
    """Method 2: AI Gateway (cached, logged)"""
    print("[Method 2] AI Gateway (cached + logged)")
    resp = httpx.post(
        f"{GATEWAY_URL}/compat/chat/completions",
        headers={
            "cf-aig-authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "model": "workers-ai/@cf/meta/llama-3.1-8b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30.0
    )
    data = resp.json()
    if "choices" in data:
        print(data["choices"][0]["message"]["content"])
    else:
        print(f"Response: {json.dumps(data, indent=2)}")


def method3_fabric(prompt: str):
    """Method 3: Your deployed mcore-ai-fabric Worker"""
    print("[Method 3] mcore-ai-fabric Worker (D1 + compliance)")
    resp = httpx.post(
        f"{FABRIC_URL}/chat",
        headers={"Content-Type": "application/json"},
        json={"messages": [{"role": "user", "content": prompt}]},
        timeout=30.0
    )
    data = resp.json()
    print(data.get("response", json.dumps(data, indent=2)))


def method4_local(prompt: str):
    """Method 4: Local AI (Ollama) via Cloudflare Tunnel"""
    print(f"[Method 4] Local AI (Ollama) via tunnel at {LOCAL_AI_URL}")
    try:
        resp = httpx.post(
            f"{LOCAL_AI_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama3.1",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60.0
        )
        data = resp.json()
        print(data.get("message", {}).get("content", json.dumps(data, indent=2)))
    except Exception as e:
        print(f"Error (is Ollama running + tunnel configured?): {e}")


def embed(text: str):
    """Generate embeddings via Workers AI"""
    print(f"[Embeddings] BGE base-en-v1.5")
    resp = httpx.post(
        f"{FABRIC_URL}/embed",
        headers={"Content-Type": "application/json"},
        json={"texts": [text]},
        timeout=30.0
    )
    data = resp.json()
    if "embeddings" in data:
        print(f"Dimensions: {data.get('dimensions', '?')}")
        print(f"First 5 values: {data['embeddings'][0][:5]}")
    else:
        print(json.dumps(data, indent=2))


def compliance(framework: str = ""):
    """Query compliance policies from D1"""
    url = f"{FABRIC_URL}/compliance"
    if framework:
        url += f"?framework={framework}"
    print(f"[Compliance] Querying D1 policies{f' for {framework}' if framework else ' (all)'}")
    resp = httpx.get(url, timeout=15.0)
    data = resp.json()
    for p in data.get("policies", []):
        print(f"  [{p['framework']}] {p['control_id']}: {p['name']} — {p['description'][:60]}")
    print(f"\nTotal: {data.get('count', 0)} policies")


def providers():
    """List AI providers from D1"""
    print("[Providers] From D1:")
    resp = httpx.get(f"{FABRIC_URL}/providers", timeout=15.0)
    data = resp.json()
    for p in data.get("providers", []):
        print(f"  {p['name']} ({p['type']}) — {p['status']}")


def stats():
    """D1 database stats"""
    print("[Stats] D1 Evidence Store:")
    resp = httpx.get("https://mcore-d1-api.me-419.workers.dev/stats", timeout=15.0)
    data = resp.json()
    for k, v in data.items():
        print(f"  {k}: {v}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    arg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    if cmd == "chat":
        method1_direct(arg)
    elif cmd == "gateway":
        method2_gateway(arg)
    elif cmd == "fabric":
        method3_fabric(arg)
    elif cmd == "local":
        method4_local(arg)
    elif cmd == "embed":
        embed(arg)
    elif cmd == "compliance":
        compliance(arg.upper() if arg else "")
    elif cmd == "providers":
        providers()
    elif cmd == "stats":
        stats()
    elif cmd == "all":
        # Run all methods to show they work
        print("=" * 60)
        method1_direct(arg or "What is CIA triad?")
        print("\n" + "=" * 60)
        method3_fabric(arg or "What is CIA triad?")
        print("\n" + "=" * 60)
        compliance()
        print("\n" + "=" * 60)
        providers()
        print("\n" + "=" * 60)
        stats()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
