#!/bin/sh
# =============================================================================
# Universal non-root entrypoint — runs as UID 1001
# Validates required environment variables before starting the service.
# Works for Python (uvicorn), Rust binaries, and Node.js.
# =============================================================================

set -e

# ---- Environment variable isolation: fail fast if critical vars are missing ----
REQUIRED_VARS_FILE="/app/.required-env"

if [ -f "$REQUIRED_VARS_FILE" ]; then
    while IFS= read -r var; do
        # Skip comments and blank lines
        case "$var" in
            \#*|"") continue ;;
        esac
        eval "val=\${$var:-}"
        if [ -z "$val" ]; then
            echo "FATAL: Required environment variable '$var' is not set. Refusing to start." >&2
            exit 1
        fi
    done < "$REQUIRED_VARS_FILE"
fi

echo "[entrypoint] Running as UID $(id -u), GID $(id -g)"
echo "[entrypoint] Starting: $@"

exec "$@"
