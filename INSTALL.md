# 📖 Estudo Bíblico com IA - Guia de Instalação

## 🚀 Instalação Automática (Recomendado)

### Windows

1. **Execute o instalador com privilégios de administrador:**
   - Clique com o botão direito em `setup.bat`
   - Selecione "Executar como administrador"
   - Aguarde a conclusão da instalação

2. **Inicie a aplicação:**
   - Dê um duplo clique em `start_app.bat`
   - A aplicação abrirá automaticamente no navegador

### O que o `setup.bat` faz?

✅ Verifica e instala Python 3.11.9  
✅ Verifica e instala Git  
✅ Cria ambiente virtual Python  
✅ Instala todas as dependências do `requirements.txt`  
✅ Verifica e instala Ollama  
✅ Baixa o modelo `llama3.2:1b`  
✅ Configura arquivo `.env` com variáveis padrão  

---

## 🛠️ Instalação Manual

### Pré-requisitos

- **Python 3.11+**: [Download](https://www.python.org/downloads/)
- **Git** (opcional): [Download](https://git-scm.com/downloads)
- **Ollama**: [Download](https://ollama.com/download)

### Passo a Passo

1. **Clone ou baixe o projeto**
   ```bash
   git clone <seu-repositorio>
   cd Biblia
   ```

2. **Crie o ambiente virtual**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure o Ollama**
   ```bash
   # Inicie o servidor
   ollama serve
   
   # Em outro terminal, baixe o modelo
   ollama pull llama3.2:1b
   ```

6. **Configure o arquivo .env**
   ```env
   OLLAMA_BASE=http://127.0.0.1:11434
   OLLAMA_GENERATE_PATHS=/api/generate
   OLLAMA_MODEL_DEFAULT=llama3.2:1b
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=localhost
   ```

7. **Inicie a aplicação**
   ```bash
   streamlit run app.py
   ```

---

## 🎯 Usando a Aplicação

### 1️⃣ Importar Dados Bíblicos

- Acesse a aba **"📥 Importar Dados"**
- Configure o repositório GitHub (padrão já fornecido)
- Clique em **"Baixar e converter do GitHub"**
- Aguarde o download e conversão

### 2️⃣ Leitura & Exegese

- Selecione a versão da Bíblia
- Escolha livro, capítulo e versículos
- Clique em **"✨ Gerar Explicação"**
- O estudo será salvo automaticamente no histórico

### 3️⃣ Gerador de Sermões

- Selecione a passagem bíblica
- Preencha tema e tipo de público
- Adicione notas adicionais (opcional)
- Clique em **"✨ Gerar Esboço de Sermão"**
- Acesse **"📋 Histórico Sermões"** para revisar

### 4️⃣ Devocional & Meditação

- Selecione um versículo
- Escolha o sentimento/tema (ex: "Gratidão", "Paz")
- Clique em **"✨ Gerar Devocional"**
- Acesse **"🕊️ Histórico Devocionais"** para revisar

### 5️⃣ Chat Teológico

- Selecione um versículo base
- Digite sua pergunta teológica
- Clique em **"✨ Enviar Pergunta"**
- Acesse **"💭 Histórico Chat"** para revisar conversas

---

## 🔧 Solução de Problemas

### Ollama Offline

```bash
# Verifique se Ollama está rodando
curl http://localhost:11434/api/version

# Se não estiver, inicie manualmente
ollama serve
```

### Modelo não encontrado

```bash
# Liste modelos instalados
ollama list

# Baixe o modelo padrão
ollama pull llama3.2:1b
```

### Erro de importação Python

```bash
# Certifique-se que o ambiente virtual está ativo
.venv\Scripts\activate

# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Port 8501 já em uso

- Modifique a porta no arquivo `.env`:
  ```env
  STREAMLIT_SERVER_PORT=8502
  ```
- Ou force outra porta:
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## 📦 Estrutura do Projeto

```
Biblia/
├── app.py                    # Aplicação principal
├── bible_data_importer.py    # Importador de dados bíblicos
├── requirements.txt          # Dependências Python
├── .env                      # Variáveis de ambiente
├── setup.bat                 # Instalador automático
├── start_app.bat             # Inicializador da aplicação
├── bible_data.json           # Dados bíblicos (após importar)
├── .venv/                    # Ambiente virtual Python
└── INSTALL.md                # Este arquivo
```

---

## 🌐 Recursos Adicionais

- **Ollama**: https://ollama.com
- **Streamlit**: https://streamlit.io
- **Python**: https://www.python.org
- **Modelos Ollama**: https://ollama.com/library

---

## 📝 Notas

- A primeira execução pode demorar devido ao download do modelo LLM (~1.3GB)
- O Ollama precisa estar rodando sempre que usar a aplicação
- Todos os históricos são salvos na sessão atual (em memória)
- Para persistência permanente, será necessário adicionar salvamento em arquivo/banco

---

## 💡 Dicas

1. **Modelos alternativos**: Você pode usar outros modelos modificando o `.env`:
   ```env
   OLLAMA_MODEL_DEFAULT=llama3.2:3b
   OLLAMA_MODEL_DEFAULT=mistral
   ```

2. **Melhorar respostas**: Modelos maiores geram respostas melhores, mas são mais lentos:
   - `llama3.2:1b` - Rápido, respostas básicas
   - `llama3.2:3b` - Balanceado
   - `llama3.1:8b` - Melhor qualidade

3. **Performance**: Se estiver lento, reduza o `max_tokens` no código

---

## 🤝 Suporte

Para problemas ou dúvidas:
1. Verifique a seção "Solução de Problemas"
2. Consulte os logs do terminal
3. Teste a conectividade do Ollama com `curl http://localhost:11434/api/tags`

**Feito com ❤️ para o estudo da Palavra**
