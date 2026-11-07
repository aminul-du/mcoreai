#!/usr/bin/env bash
# =============================================================================
# MCORE Sovereign AI - Python 3.14 Baseline & Pyenv Migration Script
# Target: Debian 13 (Trixie) / WSL2
# =============================================================================
set -euo pipefail

echo "=========================================================="
echo "🚀 MCORE DRIFT RESOLUTION: UPGRADING TO PYTHON 3.14"
echo "=========================================================="

# 1. Install Secure Build Dependencies for Debian 13
echo "🛠️ Installing native build dependencies..."
sudo apt update -y
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev git

# 2. Install Pyenv (Zero-Gap Version Manager)
echo "📦 Installing Pyenv..."
if [ ! -d "${HOME}/.pyenv" ]; then
    curl https://pyenv.run | bash
fi

export PYENV_ROOT="${HOME}/.pyenv"
export PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
eval "$(pyenv init -)"

if ! grep -q "pyenv init" "${HOME}/.bashrc"; then
    echo "export PYENV_ROOT="${HOME}/.pyenv"" >> "${HOME}/.bashrc"
    echo "[[ -d \$PYENV_ROOT/bin ]] && export PATH="\$PYENV_ROOT/bin:\$PATH"" >> "${HOME}/.bashrc"
    echo "eval "\$(pyenv init -)"" >> "${HOME}/.bashrc"
fi

# 3. Compile and Install Python 3.14
echo "🐍 Compiling Python 3.14..."
pyenv install -s 3.14.0
pyenv global 3.14.0
pyenv rehash

echo "✅ Global Baseline set to: $(python3 --version)"

# 4. Safely Migrate Terminal AI Virtual Environment
TARGET_DIR="/srv/mcore/mcore365/mcoresec/apps/terminal-ai"
if [ -d "${TARGET_DIR}" ]; then
    echo "🔄 Rebuilding Terminal AI Virtual Environment with 3.14..."
    cd "${TARGET_DIR}"
    if [ -d ".venv" ]; then
        mv .venv ".venv_backup_$(date +%Y%m%d%H%M%S)"
    fi
    python3 -m venv .venv
    source .venv/bin/activate
    if [ -f "requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
    fi
    echo "✅ Terminal AI successfully migrated to: $(python --version)"
fi

echo "=========================================================="
echo "✅ DRIFT RESOLVED. SYSTEM IS NOW ANCHORED TO PYTHON 3.14."
echo "=========================================================="
