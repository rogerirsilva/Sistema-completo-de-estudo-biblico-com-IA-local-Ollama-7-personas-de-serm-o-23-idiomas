@echo off
chcp 65001 >nul
:: =====================================================
:: Script de Commit e Push para GitHub
:: =====================================================
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     Upload para GitHub - Biblia-Local-Com-IA    ║
echo ╚══════════════════════════════════════════════════╝
echo.

:: Verificar se Git está instalado
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERRO] Git não está instalado!
    echo.
    echo Por favor, instale o Git primeiro:
    echo 1. Baixe: https://git-scm.com/download/win
    echo 2. Instale com as opções padrão
    echo 3. Reinicie este prompt de comando
    echo 4. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [✓] Git está instalado
git --version
echo.

:: Verificar se o repositório Git existe
if not exist ".git" (
    echo [INFO] Inicializando repositório Git...
    git init
    
    echo [INFO] Configurando remote...
    echo Por favor, informe a URL do repositório:
    set /p REPO_URL="URL (ex: https://github.com/usuario/Biblia-Local-Com-IA.git): "
    
    if not defined REPO_URL (
        echo [ERRO] URL não fornecida!
        pause
        exit /b 1
    )
    
    git remote add origin %REPO_URL%
    echo [✓] Remote configurado
) else (
    echo [✓] Repositório Git já inicializado
)

:: Verificar configuração do Git
git config user.name >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Configurando Git...
    set /p GIT_NAME="Seu nome: "
    set /p GIT_EMAIL="Seu email: "
    git config user.name "%GIT_NAME%"
    git config user.email "%GIT_EMAIL%"
    echo [✓] Git configurado
)

:: Criar .gitignore se não existir
if not exist ".gitignore" (
    echo [INFO] Criando .gitignore...
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo build/
        echo develop-eggs/
        echo dist/
        echo downloads/
        echo eggs/
        echo .eggs/
        echo lib/
        echo lib64/
        echo parts/
        echo sdist/
        echo var/
        echo wheels/
        echo *.egg-info/
        echo .installed.cfg
        echo *.egg
        echo.
        echo # Virtual Environment
        echo .venv/
        echo venv/
        echo ENV/
        echo env/
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo *~
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # Project specific
        echo bible_data.json
        echo *.log
    ) > .gitignore
    echo [✓] .gitignore criado
)

echo.
echo ════════════════════════════════════════════════════
echo Arquivos que serão enviados:
echo ════════════════════════════════════════════════════
git status --short

echo.
echo ════════════════════════════════════════════════════
set /p COMMIT_MSG="Mensagem do commit (Enter para usar padrão): "

if not defined COMMIT_MSG (
    set COMMIT_MSG=Adiciona históricos de Sermões, Devocionais e Chat + Sistema de instalação automática
)

echo.
echo [INFO] Adicionando arquivos...
git add .

echo [INFO] Criando commit...
git commit -m "%COMMIT_MSG%"

if %errorLevel% neq 0 (
    echo [AVISO] Nenhuma alteração para commitar ou erro no commit
    echo.
    git status
    pause
    exit /b 0
)

echo.
echo [INFO] Enviando para GitHub...
git push -u origin main

if %errorLevel% neq 0 (
    echo.
    echo [AVISO] Falha no push. Tentando branch 'master'...
    git push -u origin master
    
    if %errorLevel% neq 0 (
        echo.
        echo [ERRO] Falha ao fazer push!
        echo.
        echo Possíveis soluções:
        echo 1. Verifique sua conexão com a internet
        echo 2. Verifique se o repositório existe no GitHub
        echo 3. Verifique suas credenciais
        echo 4. Execute manualmente: git push -u origin main
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║           Upload Concluído com Sucesso!         ║
echo ╚══════════════════════════════════════════════════╝
echo.
echo [✓] Código enviado para o GitHub
echo [✓] Repositório: Biblia-Local-Com-IA
echo.
pause
