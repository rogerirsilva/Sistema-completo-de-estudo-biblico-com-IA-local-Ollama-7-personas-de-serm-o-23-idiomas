@echo off
setlocal

cd /d "%~dp0"

set "LOG=%TEMP%\biblical_study_api.log"

echo ================================================ >> "%LOG%"
echo Starting Biblical Study API (FastAPI) >> "%LOG%"
echo WorkingDir: %CD% >> "%LOG%"
echo Time: %DATE% %TIME% >> "%LOG%"
echo ================================================ >> "%LOG%"

set "PY="

REM --- 1. Check bundled packages (production: python_app/bundled_packages/) ---
set "BUNDLED=%~dp0tauri-launcher\python_app\bundled_packages"
if exist "%BUNDLED%" (
  echo [INFO] Bundled packages found at %BUNDLED% >> "%LOG%"
  set "PYTHONPATH=%BUNDLED%;%PYTHONPATH%"
)

REM --- 2. Find a Python interpreter ---

REM Check local .venv (dev: .venv at project root)
if exist "%~dp0.venv\Scripts\python.exe" set "PY=%~dp0.venv\Scripts\python.exe"

REM Fallback: tauri bundle venv
if not defined PY if exist "%~dp0tauri-launcher\python_app\.venv\Scripts\python.exe" set "PY=%~dp0tauri-launcher\python_app\.venv\Scripts\python.exe"

REM System Python
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)

if not defined PY (
  echo [ERROR] Python not found. Install Python 3.10+ from https://python.org >> "%LOG%"
  pause
  exit /b 1
)

echo [INFO] Using Python: %PY% >> "%LOG%"
echo [INFO] PYTHONPATH: %PYTHONPATH% >> "%LOG%"

REM --- 3. Ensure dependencies are available ---
if not exist "%BUNDLED%" (
  "%PY%" -c "import fastapi, uvicorn, dotenv, fpdf, cryptography" >nul 2>&1
  if errorlevel 1 (
    echo [INFO] Installing dependencies into %BUNDLED%... >> "%LOG%"
    "%PY%" -m pip install --upgrade pip >nul 2>&1
    "%PY%" -m pip install -r "%~dp0requirements.txt" --target "%BUNDLED%" >> "%LOG%" 2>&1
    if errorlevel 1 (
      echo [ERROR] pip install failed. Check %LOG% >> "%LOG%"
      pause
      exit /b 1
    )
    set "PYTHONPATH=%BUNDLED%;%PYTHONPATH%"
  )
)

echo [INFO] Starting API at http://127.0.0.1:8000 >> "%LOG%"
echo [INFO] Docs at http://127.0.0.1:8000/docs >> "%LOG%"
echo [INFO] Log file: %LOG%

REM Use --reload only if TURBO_DEV is set (dev mode)
if defined TURBO_DEV (
  "%PY%" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload >> "%LOG%" 2>&1
) else (
  "%PY%" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 >> "%LOG%" 2>&1
)
exit /b %errorlevel%
