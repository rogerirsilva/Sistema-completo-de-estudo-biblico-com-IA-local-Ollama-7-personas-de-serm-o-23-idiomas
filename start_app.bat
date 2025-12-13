@echo off
chcp 65001 >nul
:: =====================================================
:: Script de Inicialização - Aplicação Bíblia
:: =====================================================
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║      Iniciando Estudo Bíblico com IA            ║
echo ╚══════════════════════════════════════════════════╝
echo.

:: Garantir que estamos no diretório correto (onde está o script)
cd /d "%~dp0"

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.11 ou superior de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    pause
    exit /b 1
)

:: Verificar se o ambiente virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtual não encontrado. Criando...
    python -m venv .venv
    if %errorLevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual!
        echo Verifique se o Python está instalado corretamente.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado com sucesso!
    
    :: Ativar e instalar dependências
    call .venv\Scripts\activate.bat
    echo [INFO] Instalando dependências...
    python -m pip install --upgrade pip >nul 2>&1
    
    if exist "requirements.txt" (
        pip install -r requirements.txt
        if %errorLevel% neq 0 (
            echo [ERRO] Falha ao instalar dependências!
            pause
            exit /b 1
        )
    ) else (
        pip install streamlit requests python-dotenv chromadb
    )
    echo [OK] Dependências instaladas!
) else (
    echo [OK] Ambiente virtual encontrado.
    
    :: Ativar ambiente virtual
    call .venv\Scripts\activate.bat
    
    :: Verificar dependências críticas
    echo [INFO] Verificando dependências...
    
    :: Verificar Streamlit
    python -c "import streamlit" >nul 2>&1
    if %errorLevel% neq 0 (
        echo [INFO] Instalando Streamlit...
        pip install streamlit --quiet
    )
    
    :: Verificar ChromaDB
    python -c "import chromadb" >nul 2>&1
    if %errorLevel% neq 0 (
        echo [INFO] ChromaDB não encontrado. Instalando...
        pip install chromadb --quiet
        if %errorLevel% equ 0 (
            echo [OK] ChromaDB instalado com sucesso!
        ) else (
            echo [AVISO] Falha ao instalar ChromaDB. Continuando sem persistência.
        )
    ) else (
        echo [OK] ChromaDB já está instalado.
    )
    
    echo [OK] Dependências verificadas!
)

:: Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorLevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

:: Criar diretório para ChromaDB se não existir
if not exist "chroma_db" (
    echo [INFO] Criando diretório para banco de dados...
    mkdir chroma_db
    echo [OK] Diretório chroma_db criado!
)

:: Criar arquivo .env se não existir
if not exist ".env" (
    echo [INFO] Criando arquivo .env...
    (
        echo # Configuração Ollama
        echo OLLAMA_BASE=http://127.0.0.1:11434
        echo OLLAMA_GENERATE_PATHS=api/generate,api/v1/generate,v1/generate,generate
        echo OLLAMA_MODEL_DEFAULT=llama3.2:1b
        echo.
        echo # Configuração do App
        echo STREAMLIT_SERVER_PORT=8501
        echo STREAMLIT_SERVER_ADDRESS=localhost
    ) > .env
    echo [OK] Arquivo .env criado!
)

:: Verificar se Ollama está rodando
echo [INFO] Verificando serviço Ollama...
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:11434/api/version' -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Iniciando Ollama...
    start "Ollama Server" cmd /c "ollama serve"
    timeout /t 5 /nobreak >nul
    echo [OK] Ollama iniciado.
) else (
    echo [OK] Ollama já está rodando.
)

:: Obter IP da máquina
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP:~1%

:: Iniciar Streamlit
echo.
echo [INFO] Iniciando aplicação Streamlit...
echo ════════════════════════════════════════════════════
echo A aplicação será aberta no navegador automaticamente
echo.
echo ACESSO LOCAL:
echo   http://localhost:8501
echo.
echo ACESSO NA REDE:
echo   http://%IP%:8501
echo.
echo Compartilhe o endereço acima para acessar de outros dispositivos
echo na mesma rede (celular, tablet, outro computador)
echo.
echo Para encerrar: Pressione CTRL+C nesta janela
echo ════════════════════════════════════════════════════
echo.

streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --browser.serverAddress localhost

:: Se o usuário fechar o Streamlit
echo.
echo [INFO] Aplicação encerrada.
pause
