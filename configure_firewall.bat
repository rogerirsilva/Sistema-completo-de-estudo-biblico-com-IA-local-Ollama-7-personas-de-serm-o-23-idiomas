@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Verificar privilégios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ═══════════════════════════════════════════════════════
    echo   ERRO: Este script precisa ser executado como
    echo         ADMINISTRADOR
    echo ═══════════════════════════════════════════════════════
    echo.
    echo Clique com botão direito no arquivo e selecione:
    echo "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo ═══════════════════════════════════════════════════════
echo   Configuração de Firewall - Sistema Bíblico
echo ═══════════════════════════════════════════════════════
echo.

:: Remover regra antiga se existir
echo [INFO] Removendo regras antigas (se existirem)...
netsh advfirewall firewall delete rule name="Streamlit Bible Study" >nul 2>&1
netsh advfirewall firewall delete rule name="Streamlit Bible Study - TCP" >nul 2>&1

:: Adicionar regra de entrada TCP
echo [INFO] Adicionando regra de entrada (TCP)...
netsh advfirewall firewall add rule name="Streamlit Bible Study - TCP" dir=in action=allow protocol=TCP localport=8501 description="Permite acesso ao sistema de estudo bíblico pela rede local" >nul 2>&1

if %errorLevel% equ 0 (
    echo [OK] Regra de firewall criada com sucesso!
) else (
    echo [ERRO] Falha ao criar regra de firewall.
    pause
    exit /b 1
)

:: Obter IP da máquina
echo.
echo [INFO] Detectando endereço IP da máquina...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :ip_found
)
:ip_found
set IP=%IP:~1%

echo.
echo ═══════════════════════════════════════════════════════
echo   ✅ CONFIGURAÇÃO CONCLUÍDA
echo ═══════════════════════════════════════════════════════
echo.
echo Porta 8501 liberada no Firewall do Windows!
echo.
echo PRÓXIMOS PASSOS:
echo.
echo 1. Execute: start_app.bat
echo.
echo 2. Em outros dispositivos da rede, acesse:
echo    http://%IP%:8501
echo.
echo 3. Certifique-se de que os dispositivos estão na mesma
echo    rede Wi-Fi ou conectados ao mesmo roteador.
echo.
echo ═══════════════════════════════════════════════════════
echo.

pause
