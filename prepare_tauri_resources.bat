@echo off
setlocal

set "ROOT=%~dp0"
set "TARGET=%ROOT%tauri-launcher\python_app"

echo.
echo [INFO] Preparing python_app resources for Tauri...

if exist "%TARGET%" rmdir /s /q "%TARGET%"
mkdir "%TARGET%"

for %%F in (
  book_names_mapping.py
  requirements.txt
  start_api.bat
  start_api.sh
  app_config.json
  bible_data.json
) do (
  if exist "%ROOT%%%F" (
    copy /Y "%ROOT%%%F" "%TARGET%\" >nul
  )
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

echo [OK] Resources ready at %TARGET%
exit /b 0
