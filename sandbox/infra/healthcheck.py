#!/usr/bin/env python3
"""
Universal HTTP health check for all Python services.
Exits 0 if the service responds 200 on /health, exits 1 otherwise.
Configured via env vars: HEALTH_HOST (default 127.0.0.1), HEALTH_PORT (default 8000).
"""
import os
import sys
import urllib.request

host = os.environ.get("HEALTH_HOST", "127.0.0.1")
port = os.environ.get("HEALTH_PORT", os.environ.get("PORT", "8000"))
path = os.environ.get("HEALTH_PATH", "/health")
url = f"http://{host}:{port}{path}"

try:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=5) as resp:
        if resp.status == 200:
            print(f"HEALTHY: {url} → {resp.status}")
            sys.exit(0)
        else:
            print(f"UNHEALTHY: {url} → {resp.status}", file=sys.stderr)
            sys.exit(1)
except Exception as e:
    print(f"UNHEALTHY: {url} → {e}", file=sys.stderr)
    sys.exit(1)
