@echo off
setlocal

set "ROOT=%~dp0"

echo.
echo ================================================
echo Build installers with Tauri
echo ================================================

REM Kill locking processes
echo [INFO] Closing potentially locking processes...
taskkill /F /IM "Biblical Study AI.exe" /T >nul 2>&1
taskkill /F /IM "python.exe" /T >nul 2>&1
taskkill /F /IM "msiexec.exe" /T >nul 2>&1
timeout /t 2 /nobreak >nul

set "BUNDLE_MSI=%ROOT%tauri-launcher\src-tauri\target\release\bundle\msi"
if exist "%BUNDLE_MSI%" (
    echo [INFO] Cleaning old MSI bundle folder to prevent Access Denied...
    rmdir /s /q "%BUNDLE_MSI%" 2>nul
    mkdir "%BUNDLE_MSI%" 2>nul
)

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

echo [INFO] Building installers for current OS...
call npm run tauri:build
if errorlevel 1 goto :build_error

set "BUNDLE_DIR=%ROOT%tauri-launcher\src-tauri\target\release\bundle"
if not exist "%BUNDLE_DIR%" goto :artifact_error

dir /b "%BUNDLE_DIR%\msi\*.msi" >nul 2>&1
if errorlevel 1 (
  dir /b "%BUNDLE_DIR%\nsis\*.exe" >nul 2>&1
  if errorlevel 1 goto :artifact_error
)

echo [OK] Build finished. Check output in tauri-launcher\src-tauri\target\release\bundle
pause
exit /b 0

:prep_error
echo [ERROR] Failed to prepare resources.
pause
exit /b 1

:npm_missing
echo [ERROR] npm not found. Install Node.js LTS: https://nodejs.org/
pause
exit /b 1

:cargo_missing
echo [ERROR] cargo not found. Install Rust: https://rustup.rs/
pause
exit /b 1

:npm_install_error
echo [ERROR] npm install failed.
pause
exit /b 1

:icon_error
echo [ERROR] Failed to generate Tauri icons.
pause
exit /b 1

:build_error
echo [ERROR] Build failed.
pause
exit /b 1

:artifact_error
echo [ERROR] Build command finished but installer artifact was not found.
echo [ERROR] Expected .msi in bundle\msi or .exe in bundle\nsis.
pause
exit /b 1
