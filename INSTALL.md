# Guia de Instalacao - Interface Desktop (Tauri + FastAPI)

## Visao geral

Este projeto usa:

- Frontend desktop com Tauri
- Backend local com FastAPI em http://localhost:8000
- IA local via Ollama

Fluxo principal atual: aplicativo desktop. O uso de Streamlit nao e o caminho principal desta versao.

---

## Requisitos

- Windows 10 ou 11
- Python 3.11+
- Ollama instalado
- Pelo menos 1 modelo Ollama baixado

Comandos uteis do Ollama:

```bash
ollama serve
ollama pull llama3.2:3b
ollama list
```

---

## Instalacao para uso local (desenvolvimento)

1. Crie/ative ambiente virtual Python:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale dependencias Python:

```bash
pip install -r requirements.txt
```

3. Inicie o backend local (opcional em modo manual):

```bash
start_api.bat
```

4. Teste o backend:

```bash
http://localhost:8000/health
```

5. Execute o launcher desktop:

```bash
start_app.bat
```

---

## Gerar instalador (Windows)

Use o script do projeto:

```bash
tauri_build_installers.bat
```

O bundle sera gerado em:

- tauri-launcher/src-tauri/target/release/bundle/

Tipos comuns de artefato:

- .msi
- .exe

---

## Publicar instalador no GitHub

Recomendacao:

- Publique instaladores em GitHub Releases.
- Nao faça commit de binarios grandes dentro do repositorio.

Limites relevantes:

- Releases suportam assets grandes (ate 2 GiB por arquivo).
- Arquivos grandes no historico Git degradam o repositorio.

Passo a passo:

1. Gere o instalador com tauri_build_installers.bat.
2. Crie uma tag de versao (exemplo: v2.1.0).
3. Abra uma Release no GitHub.
4. Anexe os instaladores gerados.
5. Inclua notas de versao com mudancas da interface e requisitos.

---

## Solucao de problemas

### O app abre e fecha

- Verifique se o Ollama esta ativo.
- Verifique se a porta 8000 responde: http://localhost:8000/health.
- Execute start_app.bat pelo terminal para ver logs.

### Nao lista modelos Ollama

- Teste ollama list no terminal.
- Confirme OLLAMA_BASE no .env (padrao: http://127.0.0.1:11434).

### Erro de idioma/traducao na interface

- Garanta que os arquivos em translations/ estao presentes.
- Troque idioma e recarregue dados pelo botao de atualizar.

### Erro de dependencias Tauri

- Reinstale dependencias do launcher:

```bash
cd tauri-launcher
npm install
```

---

## Estrutura principal

- backend/main.py: API FastAPI principal
- backend/services/ollama_service.py: Integracao Ollama
- tauri-launcher/src/app.js: Interface desktop e logica cliente
- tauri-launcher/python_app/backend/main.py: Backend embutido no launcher
- translations/: Dicionarios de traducao da interface

---

## Checklist de release

- Build do instalador concluido
- Teste local do instalador
- Verificacao de idioma e troca de modelos
- Changelog atualizado
- Upload dos assets na Release
