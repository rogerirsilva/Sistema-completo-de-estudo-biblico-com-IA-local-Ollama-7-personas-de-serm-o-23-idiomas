# 🚀 Guia Rápido: Subir Projeto para o Git

## ✅ O que está incluído no Git

Seguindo o `.gitignore` configurado, os seguintes arquivos **SERÃO** enviados ao Git:

### 📁 Código Fonte
- ✅ `app.py` - Aplicação principal
- ✅ `*.py` - Todos os scripts Python
- ✅ `requirements.txt` - Dependências do projeto

### 📄 Documentação
- ✅ `README.md` - Documentação principal
- ✅ `DOCUMENTATION.md` - Documentação técnica
- ✅ `INSTALL.md` - Guia de instalação
- ✅ `PERSISTENCIA.md` - Guia de persistência
- ✅ `GIT_GUIDE.md` - Este guia
- ✅ Todos os arquivos `.md`

### 🔧 Scripts de Execução
- ✅ `setup.bat` - Script de configuração
- ✅ `start_app.bat` - Iniciar aplicação
- ✅ `install_chromadb.bat` - Instalar banco de dados
- ✅ `git_setup.bat` - Preparar Git
- ✅ Todos os arquivos `.bat`

### 📚 Dados Bíblicos
- ✅ `bible_data.json` - Dados bíblicos principais
- ✅ `Dados_Json/` - Pasta com todas as bíblias importadas
- ✅ `translations/` - Arquivos de tradução

## ❌ O que está IGNORADO

Os seguintes arquivos/pastas **NÃO** serão enviados ao Git:

### 🔒 Ignorados pelo .gitignore
- ❌ `.venv/` - Ambiente virtual Python (cada usuário cria o seu)
- ❌ `chroma_db/` - Banco de dados local (dados pessoais de estudos)
- ❌ `__pycache__/` - Cache Python (gerado automaticamente)
- ❌ `.env` - Variáveis de ambiente (configurações locais)
- ❌ `.vscode/` - Configurações da IDE
- ❌ `.idea/` - Configurações do PyCharm
- ❌ `.DS_Store` - Arquivos do macOS
- ❌ `Thumbs.db` - Arquivos do Windows

## 🎯 Passo a Passo para Subir no GitHub

### 1️⃣ Preparar o Projeto

```bash
# Execute o script de preparação
git_setup.bat
```

Ou manualmente:

```bash
# Inicializar repositório (só primeira vez)
git init

# Verificar status
git status
```

### 2️⃣ Adicionar Arquivos

```bash
# Adicionar todos os arquivos (respeitando .gitignore)
git add .

# Verificar o que será commitado
git status
```

### 3️⃣ Fazer Primeiro Commit

```bash
git commit -m "Initial commit: Sistema de Estudo Bíblico com IA"
```

### 4️⃣ Criar Repositório no GitHub

1. Acesse https://github.com
2. Clique em **"New repository"**
3. Nome: `estudo-biblico-ia` (ou outro nome)
4. Descrição: `Sistema de Estudo Bíblico com IA usando Ollama`
5. Escolha: **Público** ou **Privado**
6. **NÃO** marque "Initialize with README" (já temos um)
7. Clique em **"Create repository"**

### 5️⃣ Conectar ao GitHub

```bash
# Adicionar repositório remoto (use SEU URL do GitHub)
git remote add origin https://github.com/SEU_USUARIO/estudo-biblico-ia.git

# Verificar conexão
git remote -v
```

### 6️⃣ Enviar Código

```bash
# Renomear branch para main (se necessário)
git branch -M main

# Enviar para o GitHub
git push -u origin main
```

## 🔄 Atualizações Futuras

Após o primeiro push, para enviar novas mudanças:

```bash
# 1. Adicionar arquivos modificados
git add .

# 2. Fazer commit
git commit -m "Descrição da mudança"

# 3. Enviar para GitHub
git push
```

## 📦 Clonar em Outra Máquina

Para usar o projeto em outro computador:

```bash
# 1. Clonar repositório
git clone https://github.com/SEU_USUARIO/estudo-biblico-ia.git
cd estudo-biblico-ia

# 2. Executar setup (cria .venv e instala dependências)
start_app.bat
```

O `start_app.bat` vai:
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências (incluindo ChromaDB)
- ✅ Criar diretório `chroma_db/`
- ✅ Configurar `.env`
- ✅ Iniciar Ollama
- ✅ Abrir a aplicação

## 🎁 Vantagens desta Configuração

### ✅ Bíblias Incluídas
- As bíblias já importadas vão junto com o projeto
- Quem clonar já terá os dados bíblicos prontos
- Não precisa reimportar

### ✅ Setup Automático
- Ambiente virtual é criado automaticamente
- ChromaDB é instalado automaticamente
- Tudo pronto com um comando: `start_app.bat`

### ✅ Dados Pessoais Protegidos
- Seus estudos (`chroma_db/`) ficam locais
- Não sobem para o GitHub
- Cada usuário tem seus próprios dados

### ✅ Portabilidade
- Funciona em qualquer Windows
- Não precisa configuração manual
- Um comando e está rodando

## 🔍 Comandos Úteis

```bash
# Ver histórico de commits
git log --oneline

# Ver diferenças não commitadas
git diff

# Ver status
git status

# Desfazer mudanças não commitadas
git checkout -- arquivo.py

# Criar nova branch
git checkout -b nova-feature

# Trocar de branch
git checkout main

# Merge de branch
git merge nova-feature

# Ver branches
git branch -a

# Atualizar do GitHub
git pull
```

## 🆘 Problemas Comuns

### Erro: "Git não reconhecido"
```bash
# Instale o Git: https://git-scm.com/downloads
```

### Erro: "Permission denied"
```bash
# Configure suas credenciais do GitHub
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Erro: "Repository not found"
```bash
# Verifique se o URL está correto
git remote -v

# Corrigir URL
git remote set-url origin https://github.com/USUARIO_CORRETO/REPO_CORRETO.git
```

### Arquivos demais sendo adicionados
```bash
# Limpar cache do Git
git rm -r --cached .
git add .
git commit -m "Aplicar .gitignore corretamente"
```

## 📚 Recursos

- [GitHub Docs](https://docs.github.com/)
- [Git Book](https://git-scm.com/book/pt-br/v2)
- [GitHub Desktop](https://desktop.github.com/) - Interface gráfica

## ✨ Pronto!

Seu projeto está configurado para Git e pronto para ser compartilhado! 🚀

Os dados bíblicos vão junto, mas seus estudos pessoais ficam protegidos localmente.
