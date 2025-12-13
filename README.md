# 📖 Bíblia em 23 Idiomas - Local Com IA Ollama

**Sua Ferramenta Completa para Estudo Bíblico Assistido por Inteligência Artificial**

Uma aplicação web moderna que combina textos bíblicos em 23 idiomas com análise assistida por IA usando Ollama para aprofundar seu estudo bíblico.

## ✨ Características

- 📚 **23 Idiomas Suportados**: Leia a Bíblia em português, inglês, espanhol, francês, alemão, italiano, russo, chinês, japonês, coreano, árabe, hebraico, hindi, holandês, polonês, sueco, norueguês, dinamarquês, finlandês, tcheco, romeno, turco e vietnamita
- 🤖 **Assistência por IA**: Análise profunda de versículos bíblicos usando Ollama AI
- 💬 **Perguntas e Respostas**: Faça perguntas sobre tópicos bíblicos e receba respostas fundamentadas
- 🌐 **Interface Web Moderna**: Design responsivo e intuitivo
- 🔒 **Privacidade Local**: Toda a IA roda localmente, seus dados permanecem privados

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+**
2. **Ollama** (para funcionalidade de IA)

### Passo 1: Instalar Ollama

Visite [https://ollama.ai](https://ollama.ai) e siga as instruções para sua plataforma.

Depois de instalar, baixe um modelo (recomendado: llama2):

```bash
ollama pull llama2
```

Inicie o servidor Ollama:

```bash
ollama serve
```

### Passo 2: Instalar a Aplicação

1. Clone o repositório:
```bash
git clone https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama.git
cd Biblia-em-23-Idiomas-Local-Com-IA-Ollama
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (opcional):
```bash
cp .env.example .env
# Edite .env se necessário
```

### Passo 3: Execute a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: [http://localhost:5000](http://localhost:5000)

## 📖 Como Usar

### Leitura Bíblica

1. Selecione o livro, capítulo e versículo desejados
2. Escolha o idioma de sua preferência
3. Clique em "Carregar Versículo" para ver um versículo específico
4. Ou clique em "Carregar Capítulo Completo" para ver todos os versículos do capítulo

### Análise com IA

1. Primeiro, carregue um versículo
2. Opcionalmente, adicione contexto adicional
3. Clique em "Analisar Versículo com IA"
4. Aguarde enquanto a IA processa e fornece insights sobre:
   - Explicação do significado
   - Contexto histórico e cultural
   - Temas teológicos
   - Aplicação prática

### Perguntas à IA

1. Digite sua pergunta na caixa de texto
2. A pergunta pode ser sobre qualquer tópico bíblico
3. Clique em "Fazer Pergunta"
4. Receba uma resposta fundamentada biblicamente

## 🛠️ Configuração

### Variáveis de Ambiente (.env)

```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
FLASK_SECRET_KEY=your-secret-key-here
PORT=5000
FLASK_DEBUG=True
```

### Modelos Ollama Suportados

Você pode usar diferentes modelos do Ollama alterando `OLLAMA_MODEL` no arquivo `.env`:

- `llama2` (padrão, recomendado)
- `mistral`
- `mixtral`
- `neural-chat`
- E outros disponíveis em [https://ollama.ai/library](https://ollama.ai/library)

## 📊 Estrutura do Projeto

```
Biblia-em-23-Idiomas-Local-Com-IA-Ollama/
├── app.py                 # Aplicação Flask principal
├── bible_data.py          # Dados e estrutura da Bíblia
├── ollama_integration.py  # Integração com Ollama AI
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore            # Arquivos ignorados pelo Git
├── templates/
│   └── index.html        # Interface web
└── README.md             # Este arquivo
```

## 🌍 Idiomas Suportados

1. Português (pt)
2. English (en)
3. Español (es)
4. Français (fr)
5. Deutsch (de)
6. Italiano (it)
7. Русский (ru)
8. 中文 (zh)
9. 日本語 (ja)
10. 한국어 (ko)
11. العربية (ar)
12. עברית (he)
13. हिन्दी (hi)
14. Nederlands (nl)
15. Polski (pl)
16. Svenska (sv)
17. Norsk (no)
18. Dansk (da)
19. Suomi (fi)
20. Čeština (cs)
21. Română (ro)
22. Türkçe (tr)
23. Tiếng Việt (vi)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novos recursos
- Adicionar mais livros e versículos bíblicos
- Melhorar traduções
- Aprimorar a interface

## 📝 Licença

Este projeto é fornecido como está para fins educacionais e de estudo bíblico.

## 🙏 Agradecimentos

- Textos bíblicos de várias fontes de domínio público
- [Ollama](https://ollama.ai) pela plataforma de IA local
- Comunidade open source

## ⚠️ Notas Importantes

- A aplicação funciona mesmo sem Ollama instalado (modo demonstração)
- A qualidade das respostas da IA depende do modelo Ollama escolhido
- Os textos bíblicos incluídos são apenas amostrais (Genesis 1:1-3 e João 3:16)
- Para uma versão completa, você precisaria adicionar todos os livros e versículos

## 📞 Suporte

Para questões ou suporte, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ para auxiliar no estudo bíblico**
