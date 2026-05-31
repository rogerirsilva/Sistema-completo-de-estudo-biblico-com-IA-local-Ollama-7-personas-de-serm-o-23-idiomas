#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 not found. Install Python 3.11+."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[INFO] Creating virtual environment..."
  python3 -m venv .venv
fi

VENV_PY=".venv/bin/python"
if [ ! -x "$VENV_PY" ]; then
  echo "[ERROR] Virtual environment python not found: $VENV_PY"
  exit 1
fi

"$VENV_PY" -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  "$VENV_PY" -m pip install -r requirements.txt
else
  "$VENV_PY" -m pip install streamlit requests python-dotenv chromadb
fi

mkdir -p chroma_db

if [ ! -f ".env" ]; then
  cat > .env <<'EOF'
# Ollama config
OLLAMA_BASE=http://127.0.0.1:11434
OLLAMA_GENERATE_PATHS=api/generate,api/v1/generate,v1/generate,generate
OLLAMA_MODEL_DEFAULT=llama3.2:1b

# App config
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
EOF
fi

if command -v curl >/dev/null 2>&1; then
  if curl -s --max-time 2 http://127.0.0.1:11434/api/version >/dev/null; then
    echo "[OK] Ollama is running."
  else
    echo "[WARN] Ollama is not running. Start it with: ollama serve"
  fi
else
  echo "[WARN] curl not found, skipping Ollama health check."
fi

echo "[INFO] Starting Streamlit on http://localhost:8501"
exec "$VENV_PY" -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --browser.serverAddress localhost
