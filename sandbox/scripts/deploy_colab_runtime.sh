#!/usr/bin/env bash
# =============================================================================
# MCORE Sovereign AI - Python 3.14 Native Colab Runtime Deployment
# Endpoint: https://colab.mcoreai.dev
# Local Port: 127.0.0.1:8899
# =============================================================================
set -euo pipefail

echo "=========================================================="
echo "🚀 DEPLOYING NATIVE 3.14 COLAB RUNTIME & TRANSFERRING OWNERSHIP"
echo "=========================================================="

TARGET_DIR="/srv/aiseye"
PYTHON_BIN=""

if [ -f "/root/.pyenv/versions/3.14.0/bin/python3" ]; then
    PYTHON_BIN="/root/.pyenv/versions/3.14.0/bin/python3"
    chmod o+x /root /root/.pyenv /root/.pyenv/versions /root/.pyenv/versions/3.14.0 /root/.pyenv/versions/3.14.0/lib || true
elif command -v python3.14 &> /dev/null; then
    PYTHON_BIN="/usr/bin/python3.14"
else
    PYTHON_BIN="/usr/bin/python3"
fi

echo "📦 Using Python binary: ${PYTHON_BIN}"

# 1. Provision target directory
echo "📁 Provisioning ${TARGET_DIR}..."
mkdir -p "${TARGET_DIR}"
cd "${TARGET_DIR}"

# 2. Build isolated virtual environment
echo "📦 Initializing Python 3.14 kernel in aisdu-env..."
"${PYTHON_BIN}" -m venv aisdu-env
source aisdu-env/bin/activate

# 3. Install core dependencies
echo "🐍 Deploying Data Science stack and Colab WebSocket bridge..."
pip install --upgrade pip setuptools wheel
pip install numpy pandas scikit-learn jupyter jupyter_http_over_ws "notebook<7"

# 4. Configure Jupyter extensions
echo "🔌 Activating Jupyter Colab extension..."
jupyter serverextension enable --py jupyter_http_over_ws
jupyter serverextension disable --sys-prefix --py jupyterlab 2>/dev/null || true

# 5. Generate launch script
echo "📝 Generating Colab Bridge launcher..."
cat << "LAUNCHER" > "${TARGET_DIR}/launch_colab_backend.sh"
#!/usr/bin/env bash
source /srv/aiseye/aisdu-env/bin/activate
echo "🔥 Starting Sovereign Jupyter Colab Bridge on Port 8899..."
exec jupyter notebook \
  --NotebookApp.allow_origin="https://colab.research.google.com" \
  --NotebookApp.allow_remote_access=True \
  --NotebookApp.port_retries=0 \
  --NotebookApp.token="mcoreai" \
  --ip=127.0.0.1 \
  --port=8899 \
  --no-browser
LAUNCHER

chmod +x "${TARGET_DIR}/launch_colab_backend.sh"

# 6. Configure systemd persistent service
echo "⚙️ Configuring systemd service colab-backend.service..."
cat << "SERVICE" > /etc/systemd/system/colab-backend.service
[Unit]
Description=Sovereign Jupyter Colab Bridge (Python 3.14)
After=network.target

[Service]
Type=simple
User=mcoreai
Group=mcoreai
WorkingDirectory=/srv/aiseye
ExecStart=/srv/aiseye/launch_colab_backend.sh
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable --now colab-backend.service

# 7. Secure permissions
echo "🔒 Transferring ownership entirely to mcoreai user..."
chown -R mcoreai:mcoreai "${TARGET_DIR}"

echo "=========================================================="
echo "✅ DEPLOYMENT SUCCESSFUL. Python 3.14 Runtime is Ready."
echo "🔗 Access URL: https://colab.mcoreai.dev/?token=mcoreai"
echo "=========================================================="
