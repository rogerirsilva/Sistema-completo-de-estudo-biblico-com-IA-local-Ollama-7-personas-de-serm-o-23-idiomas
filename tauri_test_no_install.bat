@echo off
setlocal

set "ROOT=%~dp0"

echo.
echo ================================================
echo Tauri test mode (without installer)
echo ================================================

call "%ROOT%prepare_tauri_resources.bat"
if errorlevel 1 goto :prep_error

cd /d "%ROOT%tauri-launcher"

where npm >nul 2>&1
if errorlevel 1 goto :npm_missing

where cargo >nul 2>&1
if errorlevel 1 goto :cargo_missing

echo [INFO] Installing Node dependencies...
call npm install
if errorlevel 1 goto :npm_install_error

if not exist "src-tauri\icons\icon.ico" (
  echo [INFO] Generating Tauri icons...
  call npx tauri icon icon.png
  if errorlevel 1 goto :icon_error
)

echo [INFO] Launching Tauri in dev mode...
call npm run tauri:dev
exit /b %errorlevel%

:prep_error
echo [ERROR] Failed to prepare resources.
exit /b 1

:npm_missing
echo [ERROR] npm not found. Install Node.js LTS: https://nodejs.org/
exit /b 1

:cargo_missing
echo [ERROR] cargo not found. Install Rust: https://rustup.rs/
exit /b 1

:npm_install_error
echo [ERROR] npm install failed.
exit /b 1

:icon_error
echo [ERROR] Failed to generate Tauri icons.
exit /b 1
