# 🚀 Guia de Upload para GitHub

## ⚠️ Pré-requisito: Instalar Git

### Windows

1. **Baixe o Git**:
   - Acesse: https://git-scm.com/download/win
   - Baixe o instalador (64-bit recomendado)

2. **Instale o Git**:
   - Execute o instalador baixado
   - Use as opções padrão (Next em tudo)
   - **IMPORTANTE**: Marque "Git from the command line and also from 3rd-party software"

3. **Verifique a instalação**:
   ```bash
   # Abra um NOVO prompt de comando e digite:
   git --version
   ```

---

## 📤 Opção 1: Upload Automático (Recomendado)

### Passo a Passo

1. **Execute o script de upload**:
   ```bash
   git_push.bat
   ```

2. **Primeira vez? Configure**:
   - Informe a URL do seu repositório:
     ```
     https://github.com/SEU-USUARIO/Biblia-Local-Com-IA.git
     ```
   - Informe seu nome e email (se solicitado)

3. **Customize a mensagem de commit** (opcional):
   - Ou pressione Enter para usar a mensagem padrão

4. **Aguarde o upload completar**

---

## 📤 Opção 2: Upload Manual

### 1. Criar Repositório no GitHub

1. Acesse https://github.com
2. Clique em **"New repository"**
3. Nome: `Biblia-Local-Com-IA`
4. Descrição: `Aplicação de estudo bíblico com IA offline usando Ollama`
5. Escolha: **Public** ou **Private**
6. **NÃO** marque "Initialize with README"
7. Clique em **"Create repository"**

### 2. Configurar Git Local

```bash
# Navegar até a pasta do projeto
cd C:\Users\rogerio.rodrigues\Documents\Biblia

# Inicializar repositório (se ainda não foi)
git init

# Configurar seu nome e email
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"

# Adicionar o remote
git remote add origin https://github.com/SEU-USUARIO/Biblia-Local-Com-IA.git
```

### 3. Criar .gitignore

```bash
# Criar arquivo .gitignore
notepad .gitignore
```

Cole este conteúdo:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
bible_data.json
*.log
```

### 4. Fazer Commit e Push

```bash
# Adicionar todos os arquivos
git add .

# Criar commit
git commit -m "Adiciona históricos de Sermões, Devocionais e Chat + Sistema de instalação automática"

# Enviar para GitHub
git push -u origin main
```

Se o comando acima falhar, tente:
```bash
git push -u origin master
```

---

## 🔐 Autenticação no GitHub

### Token de Acesso Pessoal (Recomendado)

Desde 2021, o GitHub não aceita mais senha. Use um token:

1. **Gerar Token**:
   - Acesse: https://github.com/settings/tokens
   - Clique em **"Generate new token"** → **"Generate new token (classic)"**
   - Nome: `Biblia-Local-Token`
   - Marque: `repo` (acesso completo aos repositórios)
   - Clique em **"Generate token"**
   - **COPIE O TOKEN** (não será mostrado novamente!)

2. **Usar o Token**:
   ```bash
   # Quando pedir senha, use o TOKEN gerado
   Username: SEU-USUARIO
   Password: ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

### GitHub Desktop (Alternativa Fácil)

1. Baixe: https://desktop.github.com
2. Faça login com sua conta GitHub
3. File → Add Local Repository
4. Selecione a pasta do projeto
5. Clique em "Publish repository"

---

## 📋 Arquivos que Serão Enviados

```
✅ app.py                      # Aplicação principal
✅ bible_data_importer.py      # Importador
✅ requirements.txt            # Dependências
✅ setup.bat                   # Instalador automático
✅ start_app.bat               # Inicializador
✅ git_push.bat                # Este script de upload
✅ check_environment.bat       # Verificador de ambiente
✅ README.md                   # Documentação principal
✅ INSTALL.md                  # Guia de instalação
✅ CHANGELOG.md                # Registro de alterações
✅ GIT_GUIDE.md                # Este guia

❌ .venv/                      # Ambiente virtual (ignorado)
❌ __pycache__/                # Cache Python (ignorado)
❌ bible_data.json             # Dados bíblicos (ignorado - muito grande)
```

---

## 🔄 Atualizações Futuras

Após o primeiro upload, para enviar novas alterações:

```bash
# Opção 1: Usar o script
git_push.bat

# Opção 2: Comandos manuais
git add .
git commit -m "Descrição das alterações"
git push
```

---

## 🐛 Solução de Problemas

### Erro: "fatal: not a git repository"

```bash
git init
git remote add origin https://github.com/SEU-USUARIO/Biblia-Local-Com-IA.git
```

### Erro: "failed to push some refs"

```bash
# Atualizar repositório local primeiro
git pull origin main --rebase
git push origin main
```

### Erro: "Support for password authentication was removed"

Use um **Token de Acesso Pessoal** (veja seção Autenticação acima)

### Erro: "Permission denied (publickey)"

Use HTTPS ao invés de SSH:
```bash
git remote set-url origin https://github.com/SEU-USUARIO/Biblia-Local-Com-IA.git
```

---

## 📝 Dicas

1. **Commits frequentes**: Faça commits pequenos e frequentes
2. **Mensagens claras**: Use mensagens descritivas
3. **Branches**: Para features grandes, use branches:
   ```bash
   git checkout -b nova-feature
   # ... fazer alterações ...
   git push origin nova-feature
   ```

4. **Ver histórico**:
   ```bash
   git log --oneline
   ```

5. **Desfazer alterações**:
   ```bash
   git checkout -- arquivo.py  # Desfaz alterações não commitadas
   ```

---

## 🌟 Pronto!

Após seguir este guia, seu projeto estará no GitHub e poderá ser:
- ✅ Compartilhado com outros
- ✅ Clonado em outros computadores
- ✅ Versionado e rastreado
- ✅ Colaborado por múltiplas pessoas

**URL do projeto**: `https://github.com/SEU-USUARIO/Biblia-Local-Com-IA`

---

**Bom upload! 🚀**
