@echo off
setlocal

cd /d "%~dp0"
set "VENV_PY=.venv\Scripts\python.exe"

echo.
echo ================================================
echo Starting Biblical Study API (FastAPI)
echo ================================================

python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found.
  exit /b 1
)

if not exist ".venv\Scripts\activate.bat" (
  echo [INFO] Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv
    exit /b 1
  )
)

if not exist "%VENV_PY%" (
  echo [ERROR] Venv python not found: %VENV_PY%
  exit /b 1
)

echo [INFO] Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency install failed.
  exit /b 1
)

echo [INFO] Starting API at http://localhost:8000
echo [INFO] Docs: http://localhost:8000/docs
"%VENV_PY%" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
exit /b %errorlevel%
