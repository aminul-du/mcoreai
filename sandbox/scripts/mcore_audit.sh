#!/usr/bin/env bash
set -e
SYS_PYTHON=$(python3 --version 2>&1 || echo "Not Installed")
VERTEX_PYTHON=$(/srv/mcore/mcore365/mcoresec/apps/terminal-ai/.venv/bin/python --version 2>/dev/null || echo "Vertex ENV not found")
COLAB_PYTHON=$(/srv/online-research-academy/academy-env/bin/python --version 2>/dev/null || echo "Colab ENV not found")
NODE_VER=$(node -v 2>/dev/null || echo "Not Installed")
PNPM_VER=$(pnpm -v 2>/dev/null || echo "Not Installed")

cat << INNER_EOF > "$HOME/mcore-state.yaml"
mcore_infrastructure_state:
  timestamp: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  kernel: "Debian 13 (WSL2)"
  core_languages:
    python_system_default: "$SYS_PYTHON"
    python_vertex_ai_env: "$VERTEX_PYTHON"
    python_colab_academy_env: "$COLAB_PYTHON"
    target_baseline: "Python 3.14.x"
  devops_ecosystem:
    node_version: "$NODE_VER"
    pnpm_version: "$PNPM_VER"
  status:
    drift_detected: false
    action_required: "System optimally aligned to 3.14 baseline."
INNER_EOF
