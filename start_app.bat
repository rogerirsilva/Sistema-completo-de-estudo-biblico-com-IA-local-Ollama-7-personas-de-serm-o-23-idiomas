@echo off
setlocal

rem =====================================================
rem Startup script - Bible Study App
rem ASCII-only to avoid cmd encoding parsing issues
rem =====================================================

echo.
echo ====================================================
echo Starting Bible Study with AI
echo ====================================================
echo.

rem Ensure we run from this script folder
cd /d "%~dp0"
set "VENV_PY=.venv\Scripts\python.exe"

rem Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install Python 3.11+ and enable "Add Python to PATH".
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

rem Create venv if missing
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Creating .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )

    echo [INFO] Installing dependencies...
    "%VENV_PY%" -m pip install --upgrade pip
    if exist "requirements.txt" (
        "%VENV_PY%" -m pip install -r requirements.txt
    ) else (
        "%VENV_PY%" -m pip install streamlit requests python-dotenv chromadb
    )

    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        pause
        exit /b 1
    )
)

rem Validate venv python
if not exist "%VENV_PY%" (
    echo [ERROR] Virtual environment Python not found: %VENV_PY%
    pause
    exit /b 1
)

rem Ensure Streamlit is installed in this venv
"%VENV_PY%" -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Streamlit not found in .venv. Installing...
    "%VENV_PY%" -m pip install streamlit
    if errorlevel 1 (
        echo [ERROR] Failed to install Streamlit in .venv.
        pause
        exit /b 1
    )
)

rem Ensure app folders/files
if not exist "chroma_db" mkdir chroma_db

if not exist ".env" (
    > .env echo # Ollama config
    >> .env echo OLLAMA_BASE=http://127.0.0.1:11434
    >> .env echo OLLAMA_GENERATE_PATHS=api/generate,api/v1/generate,v1/generate,generate
    >> .env echo OLLAMA_MODEL_DEFAULT=llama3.2:1b
    >> .env echo.
    >> .env echo # App config
    >> .env echo STREAMLIT_SERVER_PORT=8501
    >> .env echo STREAMLIT_SERVER_ADDRESS=localhost
)

rem Check Ollama API
echo [INFO] Checking Ollama service...
powershell -NoProfile -Command "try { Invoke-RestMethod -Uri 'http://localhost:11434/api/version' -TimeoutSec 2 ^| Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama is not running.
    echo [WARN] Start it manually in another window with: ollama serve
) else (
    echo [OK] Ollama is running.
)

echo.
echo [INFO] Starting Streamlit...
echo Local URL: http://localhost:8501
echo Press CTRL+C to stop.
echo.

"%VENV_PY%" -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --browser.serverAddress localhost
set "APP_EXIT=%ERRORLEVEL%"

echo.
echo [INFO] Application closed. Exit code: %APP_EXIT%
pause
exit /b %APP_EXIT%
