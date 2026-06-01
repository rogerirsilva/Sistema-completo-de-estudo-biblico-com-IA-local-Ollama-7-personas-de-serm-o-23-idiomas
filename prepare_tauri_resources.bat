@echo off
setlocal

set "ROOT=%~dp0"
set "TARGET=%ROOT%tauri-launcher\python_app"
set "BUNDLED_CACHE=%TEMP%\biblical_study_bundled_cache"

echo.
echo [INFO] Preparing python_app resources for Tauri...

REM Preserve existing bundled_packages and start scripts to avoid re-download / overwrite
if exist "%TARGET%\bundled_packages" (
  echo [INFO] Preserving bundled_packages cache...
  if exist "%BUNDLED_CACHE%" rmdir /s /q "%BUNDLED_CACHE%"
  move "%TARGET%\bundled_packages" "%BUNDLED_CACHE%" >nul
)
REM Preserve start_api.bat and start_api.sh (these have correct paths for python_app/)
if exist "%TARGET%\start_api.bat" (
  copy /Y "%TARGET%\start_api.bat" "%TEMP%\biblical_study_start_api.bat" >nul
)
if exist "%TARGET%\start_api.sh" (
  copy /Y "%TARGET%\start_api.sh" "%TEMP%\biblical_study_start_api.sh" >nul
)

if exist "%TARGET%" rmdir /s /q "%TARGET%"
mkdir "%TARGET%"

for %%F in (
  book_names_mapping.py
  requirements.txt
  app_config.json
  bible_data.json
) do (
  if exist "%ROOT%%%F" (
    copy /Y "%ROOT%%%F" "%TARGET%\" >nul
  )
)

REM Restore start_api.bat and start_api.sh (python_app/ versions with correct relative paths)
if exist "%TEMP%\biblical_study_start_api.bat" (
  copy /Y "%TEMP%\biblical_study_start_api.bat" "%TARGET%\start_api.bat" >nul
  del "%TEMP%\biblical_study_start_api.bat" >nul 2>&1
) else if exist "%ROOT%tauri-launcher\python_app\start_api.bat" (
  copy /Y "%ROOT%tauri-launcher\python_app\start_api.bat" "%TARGET%\start_api.bat" >nul
)
if exist "%TEMP%\biblical_study_start_api.sh" (
  copy /Y "%TEMP%\biblical_study_start_api.sh" "%TARGET%\start_api.sh" >nul
  del "%TEMP%\biblical_study_start_api.sh" >nul 2>&1
) else if exist "%ROOT%tauri-launcher\python_app\start_api.sh" (
  copy /Y "%ROOT%tauri-launcher\python_app\start_api.sh" "%TARGET%\start_api.sh" >nul
)

if exist "%ROOT%backend" (
  robocopy "%ROOT%backend" "%TARGET%\backend" /E /NFL /NDL /NJH /NJS /NC /NS >nul
)

if exist "%ROOT%translations" (
  robocopy "%ROOT%translations" "%TARGET%\translations" /E /NFL /NDL /NJH /NJS /NC /NS >nul
)

if exist "%ROOT%Dados_Json" (
  robocopy "%ROOT%Dados_Json" "%TARGET%\Dados_Json" /E /NFL /NDL /NJH /NJS /NC /NS >nul
)

REM Restore bundled_packages from cache
if exist "%BUNDLED_CACHE%" (
  echo [INFO] Restoring bundled_packages from cache...
  move "%BUNDLED_CACHE%" "%TARGET%\bundled_packages" >nul
)

REM Build bundled_packages if still missing (first-time / clean checkout)
if exist "%TARGET%\bundled_packages" goto :after_build
echo [INFO] Building bundled_packages (first time)...
where python >nul 2>&1
if errorlevel 1 (
  echo [WARN] Python not found. Skipping bundled_packages build.
  goto :after_build
)
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r "%TARGET%\requirements.txt" --target "%TARGET%\bundled_packages" >nul 2>&1
if errorlevel 1 (
  echo [WARN] pip install failed. App will use system Python packages.
) else (
  echo [OK] bundled_packages created.
)
:after_build

echo [OK] Resources ready at %TARGET%
exit /b 0
