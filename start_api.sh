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
  echo "[ERROR] venv python not found: $VENV_PY"
  exit 1
fi

echo "[INFO] Installing dependencies..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt

echo "[INFO] Starting API at http://localhost:8000"
echo "[INFO] Docs: http://localhost:8000/docs"
exec "$VENV_PY" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
