@echo off
echo ================================================
echo  Preparando projeto para Git
echo ================================================
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERRO] Git não está instalado!
    echo Por favor, instale o Git de: https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Verificar se já é um repositório Git
if exist ".git" (
    echo [INFO] Repositório Git já inicializado.
    echo.
) else (
    echo [INFO] Inicializando repositório Git...
    git init
    echo [OK] Repositório inicializado!
    echo.
)

REM Mostrar status
echo [INFO] Arquivos que serão incluídos no Git:
echo.
git status --short
echo.

echo ================================================
echo  Arquivos IGNORADOS (.gitignore):
echo ================================================
echo - .venv/           (Ambiente virtual Python)
echo - chroma_db/       (Banco de dados local)
echo - __pycache__/     (Cache Python)
echo - .env             (Variáveis de ambiente)
echo.

echo ================================================
echo  Arquivos INCLUÍDOS no Git:
echo ================================================
echo - *.py             (Código Python)
echo - *.bat            (Scripts de execução)
echo - *.md             (Documentação)
echo - requirements.txt (Dependências)
echo - bible_data.json  (Dados bíblicos)
echo - Dados_Json/      (Bíblias importadas)
echo - translations/    (Traduções)
echo.

echo ================================================
echo  Comandos úteis:
echo ================================================
echo.
echo Adicionar todos os arquivos:
echo   git add .
echo.
echo Fazer commit:
echo   git commit -m "Mensagem do commit"
echo.
echo Conectar ao repositório remoto:
echo   git remote add origin https://github.com/usuario/repo.git
echo.
echo Enviar para o GitHub:
echo   git push -u origin main
echo.
echo ================================================
pause
