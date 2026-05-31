@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ═══════════════════════════════════════════════════════
echo   Verificação de ChromaDB
echo ═══════════════════════════════════════════════════════
echo.

:: Verificar se venv existe
if not exist .venv (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Execute: start_app.bat
    pause
    exit /b 1
)

:: Ativar venv
call .venv\Scripts\activate.bat

echo [INFO] Verificando instalação do ChromaDB...
echo.

:: Verificar ChromaDB
python -c "import chromadb; print('✅ ChromaDB:', chromadb.__version__); from chromadb.config import Settings; print('✅ Settings OK'); import chromadb.api; print('✅ API OK')" 2>nul

if %errorLevel% neq 0 (
    echo ❌ ChromaDB NÃO está instalado corretamente!
    echo.
    echo [INFO] Instalando ChromaDB...
    pip install chromadb --quiet
    
    if %errorLevel% equ 0 (
        echo [OK] ChromaDB instalado com sucesso!
        python -c "import chromadb; print('✅ Versão:', chromadb.__version__)"
    ) else (
        echo [ERRO] Falha na instalação!
    )
) else (
    echo.
    echo [OK] ChromaDB está instalado e funcionando corretamente!
)

echo.
echo [INFO] Verificando diretório do banco de dados...
if exist chroma_db (
    echo [OK] Diretório chroma_db/ existe
    dir chroma_db /s
) else (
    echo [INFO] Criando diretório chroma_db/...
    mkdir chroma_db
    echo [OK] Diretório criado!
)

echo.
echo ═══════════════════════════════════════════════════════
pause
