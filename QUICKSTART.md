# Quick Start Guide

## Início Rápido - Getting Started

### 1. Instalação Rápida / Quick Install

```bash
# Clone o repositório / Clone the repository
git clone https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama.git
cd Biblia-em-23-Idiomas-Local-Com-IA-Ollama

# Instale as dependências / Install dependencies
pip install -r requirements.txt

# Execute a aplicação / Run the application
python app.py
```

Abra seu navegador em / Open your browser at: **http://localhost:5000**

### 2. Recursos Principais / Main Features

#### 🌍 23 Idiomas Suportados / 23 Supported Languages
Leia a Bíblia em 23 idiomas diferentes / Read the Bible in 23 different languages

#### 📖 Navegação Fácil / Easy Navigation
- Selecione livro, capítulo e versículo
- Select book, chapter and verse
- Visualize versículos individuais ou capítulos completos
- View individual verses or complete chapters

#### 🤖 Assistência por IA / AI Assistance
- Análise profunda de versículos / Deep verse analysis
- Perguntas e respostas / Question answering
- Contexto histórico e teológico / Historical and theological context

#### 🔒 Privacidade / Privacy
- Roda localmente / Runs locally
- Nenhum dado enviado para a nuvem / No data sent to the cloud
- IA executada na sua máquina / AI runs on your machine

### 3. Configuração da IA (Opcional) / AI Setup (Optional)

Para usar os recursos de IA, instale o Ollama:
To use AI features, install Ollama:

1. Visite / Visit: https://ollama.ai
2. Baixe e instale para seu sistema operacional
   Download and install for your operating system
3. Execute / Run:
   ```bash
   ollama pull llama2
   ollama serve
   ```

**Nota / Note**: A aplicação funciona mesmo sem IA, apenas os recursos de análise
ficam indisponíveis. / The application works without AI, only analysis features
will be unavailable.

### 4. Estrutura / Structure

```
├── app.py              # Aplicação principal / Main application
├── bible_data.py       # Dados bíblicos / Bible data
├── ollama_integration.py  # Integração IA / AI integration
├── templates/
│   └── index.html      # Interface web / Web interface
└── requirements.txt    # Dependências / Dependencies
```

### 5. Exemplos de Uso / Usage Examples

#### Ler um Versículo / Read a Verse
1. Selecione "Genesis" / Select "Genesis"
2. Digite capítulo "1" / Enter chapter "1"
3. Digite versículo "1" / Enter verse "1"
4. Escolha o idioma / Choose language
5. Clique "Carregar Versículo" / Click "Load Verse"

#### Analisar com IA / Analyze with AI
1. Carregue um versículo primeiro / Load a verse first
2. Clique "Analisar Versículo com IA" / Click "Analyze with AI"
3. Aguarde a análise / Wait for analysis

#### Fazer uma Pergunta / Ask a Question
1. Digite sua pergunta / Type your question
2. Clique "Fazer Pergunta" / Click "Ask Question"
3. Receba a resposta / Receive the answer

### 6. Solução de Problemas / Troubleshooting

**Problema / Problem**: "Ollama AI não disponível"
**Solução / Solution**: Instale e execute o Ollama seguindo a seção 3

**Problema / Problem**: "Versículo não encontrado"
**Solução / Solution**: Atualmente temos versículos de exemplo. Para versões completas,
consulte o README.md / Currently we have sample verses. For full versions, see README.md

**Problema / Problem**: Erro ao instalar dependências
**Solução / Solution**: 
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Desenvolvimento / Development

Execute os testes / Run tests:
```bash
python test_app.py
```

Modo debug / Debug mode:
```bash
FLASK_DEBUG=True python app.py
```

### 8. Contribuir / Contributing

Contribuições são bem-vindas! / Contributions are welcome!
- Reporte bugs / Report bugs
- Sugira recursos / Suggest features
- Envie pull requests / Submit pull requests

### 9. Suporte / Support

Para questões ou problemas, abra uma issue no GitHub.
For questions or issues, open an issue on GitHub.

---

**Desenvolvido com ❤️ para o estudo bíblico**
**Developed with ❤️ for Bible study**
