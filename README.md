<div align="center">

# 📖 Estudo Bíblico com IA

### *Sua Ferramenta Completa para Estudo Bíblico Assistido por Inteligência Artificial*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tauri](https://img.shields.io/badge/Tauri-Desktop-24C8DB?logo=tauri&logoColor=white)](https://tauri.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ai&logoColor=white)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**🌍 Idiomas / Languages / Idiomas:** [🇧🇷 Português](README.md) • [🇺🇸 English](README.en.md) • [🇪🇸 Español](README.es.md)

[✨ Funcionalidades](#-funcionalidades) • [🚀 Instalação](#-instalação) • [📚 Como Usar](#-como-usar) • [🎭 Personas](#-personas-de-sermão) • [💝 Apoiar](#-apoie-o-projeto)

**Clone o projeto:**
```bash
git clone https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama.git
cd Biblia-em-23-Idiomas-Local-Com-IA-Ollama
```

---

</div>

## 🌟 Sobre o Projeto

Uma aplicação completa e **100% offline** para estudo bíblico profundo, utilizando modelos de linguagem local (Ollama) para análise teológica, geração de sermões, devocionais e muito mais. Ideal para pastores, estudantes de teologia, professores de escola bíblica e todos que desejam aprofundar seu conhecimento das Escrituras.

### Atualização da interface

- Interface principal migrada para desktop com Tauri.
- Backend local em FastAPI na porta 8000.
- Integração Ollama local com listagem de modelos, geração e fallback robusto.
- Tradução da interface em múltiplos idiomas (incluindo rótulos, botões e históricos).

### 🎯 Por que usar este sistema?

- ✅ **100% Offline**: Seus dados bíblicos nunca saem do seu computador
- ✅ **Inteligência Artificial Avançada**: Análise teológica profunda usando LLMs locais
- ✅ **7 Personas de Sermão**: Estilos únicos de pregação (Analítico, Narrativo, Profético, etc.)
- ✅ **Multilíngue**: Suporte a Português, Inglês, Espanhol e outros idiomas
- ✅ **Histórico Completo**: Todas as suas análises, sermões e devocionais salvos automaticamente
- ✅ **Gerador de Perguntas**: Crie quizzes bíblicos com até 50 perguntas
- ✅ **Exportação PDF**: Gere PDFs profissionais de sermões e estudos
- ✅ **Multi-Versão**: Trabalhe com NVI, ACF, AA, KJV e outras traduções

---

## ✨ Funcionalidades

### 📚 Leitura & Exegese
- 🔍 Seleção interativa de livros, capítulos e **múltiplos versículos** (ex: "1-5, 10, 15-20")
- 🧠 Geração automática de **explicações teológicas profundas**
- 📜 Análise contextual, histórica e linguística (Grego/Hebraico)
- 📖 **Histórico de Estudos** com busca inteligente e filtros
- 📄 Exportação para PDF com formatação profissional

### 🗣️ Gerador de Sermões (7 Personas)
Crie sermões em **7 estilos diferentes** de pregação:

- **🔍 Analítico-Essência** (O Investigador): Psicologia espiritual, motivações ocultas
- **📚 Expositivo-Teológico** (O Professor): Contexto histórico, exegese, doutrina
- **🎬 Narrativo-Imersivo** (O Storyteller): Atmosfera, emoção, tensão dramática
- **💡 Devocional-Prático** (O Mentor): Vida diária, consolo, passos práticos
- **✝️ Cristocêntrico-Tipológico** (O Revelador): Jesus em todo texto, tipos e sombras
- **🔥 Profético-Confrontador** (O Atalaia): Arrependimento, santidade, urgência
- **🛡️ Apologético-Filosófico** (O Defensor): Lógica, razão, defesa da fé

**Recursos:**
- ✅ Personalização por tema, público-alvo e notas do pregador
- ✅ Escopos flexíveis: livro específico, múltiplos livros, testamento ou bíblia toda
- ✅ Seleção de múltiplos versículos (ex: "João 3:1-16, 19, 25-30")
- ✅ Timeout dinâmico (até 10 minutos) para sermões complexos
- ✅ Auto-continuação inteligente (até 5 continuações automáticas)
- ✅ Histórico completo com busca e exportação PDF

### 🧘 Devocional & Meditação
- 🙏 Devocionais personalizados por sentimento/tema (Gratidão, Paz, Força, etc.)
- 💭 Reflexões profundas sobre passagens escolhidas
- 🌅 Meditações para momentos específicos do dia
- 📚 Suporte a múltiplos livros e versículos
- 🗂️ **Histórico de Devocionais** com busca e filtros
- 📄 Exportação para PDF

### 💬 Chat Teológico Inteligente
- ❓ Perguntas e respostas baseadas em versículos específicos
- 📖 Análise interpretativa e doutrinária profunda
- 🌍 Contexto histórico, cultural e linguístico
- 📚 Escopos variados: versículo, múltiplos livros, testamento ou bíblia toda
- 💾 **Histórico de Conversas** para consultas anteriores
- 📄 Exportação para PDF

### ❓ Gerador de Perguntas Bíblicas
- 🎯 Gere de 1 a **50 perguntas** sobre qualquer livro ou escopo
- ✅ Modo **Com Respostas** ou **Só Perguntas** (para quizzes)
- 📚 Escopos: livro específico, múltiplos livros ou bíblia toda
- 🧠 Respostas curtas e diretas (1-2 frases) com linguagem teológica equilibrada
- 💾 Histórico completo com filtros por modo
- 📄 Exportação para PDF formatado

### 📥 Importar Dados Bíblicos
- 🌐 Organização por idioma (pt/, en/, es/, etc.)
- 📦 Importação automática de múltiplas versões bíblicas
- ✅ Suporte a NVI, ACF, AA, KJV, NIV, RV1960 e outras
- 🔄 Mesclagem inteligente com versões existentes
- 📁 Sistema de pastas organizado: `Dados_Json/{idioma}/`

---

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8 ou superior** instalado
2. **Ollama** instalado e rodando localmente
   - Download: [https://ollama.ai/](https://ollama.ai/)
   - Baixe ao menos um modelo: `ollama pull llama3.2` ou `ollama pull mistral`
3. **Windows 10/11** para uso do instalador desktop atual

### Windows - Instalação Desktop (Recomendado)

```bash
# Gerar instalador localmente (mantenedor)
tauri_build_installers.bat

# Executar app já instalado (usuário final)
start_app.bat
```

No fluxo desktop:
- ✅ A interface Tauri inicia o backend FastAPI embutido automaticamente
- ✅ A comunicação com IA local ocorre via Ollama em localhost
- ✅ Não depende mais de abrir Streamlit no navegador como fluxo principal

### API local para diagnóstico

```bash
http://localhost:8000/health
```

> Observação: o launcher desktop é a interface principal. A API FastAPI permanece disponível para integração/diagnóstico.

👉 **[Guia Completo de Instalação](INSTALL.md)**

---

## 📦 Publicação do instalador no GitHub

Sim, você pode disponibilizar o instalador no GitHub sem problema, desde que publique como asset de Release (não dentro do histórico Git).

Boas práticas:

- Publique instaladores em GitHub Releases.
- Não versione binários grandes no repositório (evite commits de arquivos .exe/.msi).
- Limite de arquivo em Release é alto (até 2 GiB por asset), então instaladores desktop comuns funcionam bem.
- Se o instalador crescer demais, use compactação e divida por plataforma/arquitetura.

Fluxo sugerido:

1. Gere o instalador com `tauri_build_installers.bat`.
2. Abra uma nova Release no GitHub.
3. Anexe os arquivos de `tauri-launcher/src-tauri/target/release/bundle/`.
4. Informe requisitos: Ollama instalado e modelo recomendado.
5. Mantenha changelog por versão.

## 🛠️ Tecnologias

- **Python 3.11+**
- **Tauri + HTML/CSS/JS** - Interface desktop
- **FastAPI** - Backend local HTTP
- **Ollama** - LLM local para IA offline
- **ChromaDB** - Banco de dados vetorial para persistência
- **Modelo padrão**: `llama3.2:1b`

## 💾 Persistência de Dados

**NOVIDADE!** Todos os seus estudos, sermões, devocionais e conversas são automaticamente salvos em um banco de dados local.

- ✅ **Salvamento automático** - Não perca mais seus estudos ao fechar a aplicação
- 🔄 **Carregamento instantâneo** - Todos os dados são restaurados ao iniciar
- 🔍 **Busca eficiente** - Históricos organizados e pesquisáveis
- 💾 **Backup simples** - Copie a pasta `chroma_db/` para fazer backup

### Instalar ChromaDB

```bash
# Opção 1: Script automático (Windows)

### Instalar ChromaDB

```bash
# Opção 1: Script automático (Windows)
install_chromadb.bat

# Opção 2: Manual
pip install chromadb
```

---

## 📚 Como Usar

### 1️⃣ Primeira Execução

1. Execute `setup.bat` como administrador
2. Aguarde a instalação de todas as dependências
3. O Ollama iniciará automaticamente (se instalado)
4. Execute `start_app.bat` para abrir a aplicação

### 2️⃣ Importar Versões Bíblicas

1. Acesse a aba **"📥 Importar Dados"**
2. Coloque arquivos `.json` em `Dados_Json/{idioma}/`
   - Exemplo: `Dados_Json/pt/nvi.json`
3. Clique em **"🔄 Importar Versões da Pasta"**

**Fontes de Bíblias JSON:**
- **Português**: [github.com/thiagobodruk/bible](https://github.com/thiagobodruk/bible)
- **English**: [github.com/scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)
- **Español**: [github.com/thiagobodruk/bible (branch es)](https://github.com/thiagobodruk/bible)

### 3️⃣ Começar a Estudar

**📖 Leitura & Exegese:**
```
1. Selecione livro, capítulo e versículos (ex: "1-5, 10, 15-20")
2. Clique em "✨ Gerar Explicação"
3. Veja análise contextual, histórica e teológica
4. Acesse "📚 Histórico" para revisar estudos anteriores
```

**🗣️ Gerador de Sermões:**
```
1. Escolha escopo (livro, múltiplos livros, testamento ou bíblia)
2. Selecione versículos específicos
3. Escolha uma das 7 PERSONAS de pregação
4. Tema: "Bem-aventuranças" | Público: "Jovens adultos"
5. Gere e exporte para PDF
```

**❓ Gerador de Perguntas:**
```
1. Selecione escopo (livro, múltiplos ou bíblia toda)
2. Quantidade: 1-50 perguntas
3. Modo: Com Respostas ou Só Perguntas
4. Perfeito para escolas bíblicas e grupos de estudo!
```

---

## 🎭 Personas de Sermão

Cada persona tem **tom, método e estrutura únicos**:

| Persona | Foco | Ideal Para |
|---------|------|-----------|
| 🔍 **Analítico-Essência** | Psicologia espiritual, motivações ocultas | Estudos profundos, grupos de crescimento |
| 📚 **Expositivo-Teológico** | Contexto histórico, exegese, doutrina | Escolas bíblicas, seminários |
| 🎬 **Narrativo-Imersivo** | Atmosfera, emoção, tensão dramática | Cultos de avivamento, evangelísticos |
| 💡 **Devocional-Prático** | Vida diária, consolo, passos práticos | Grupos pequenos, devocionais |
| ✝️ **Cristocêntrico-Tipológico** | Jesus em todo texto, tipos e sombras | Cultos de Santa Ceia, Páscoa |
| 🔥 **Profético-Confrontador** | Arrependimento, santidade, urgência | Campanhas, retiros espirituais |
| 🛡️ **Apologético-Filosófico** | Lógica, razão, defesa da fé | Debates, evangelismo intelectual |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|--------|
| ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white) | 3.8+ | Linguagem principal |
| ![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white) | 1.32+ | Interface web interativa |
| ![Ollama](https://img.shields.io/badge/Ollama-Latest-000000?logo=ai&logoColor=white) | Latest | LLM local (offline) |
| ![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4+-FF6B6B?logo=database&logoColor=white) | 0.4+ | Banco vetorial para históricos |
| ![ReportLab](https://img.shields.io/badge/ReportLab-4.0+-green?logo=adobe-acrobat-reader&logoColor=white) | 4.0+ | Geração de PDFs |

**Modelos LLM suportados:** `llama3.2:1b`, `llama3.2:3b`, `mistral`, `llama3.1:8b`, `qwen2.5` e qualquer modelo Ollama compatível.

---

## 📁 Estrutura do Projeto

```
Biblia/
├── 📄 app.py                          # Aplicação principal Streamlit
├── 📄 bible_data_importer.py          # Importador de dados bíblicos
├── 📄 requirements.txt                # Dependências Python
├── 📄 .env                            # Configurações (Ollama, Streamlit)
├── 🚀 setup.bat                       # Instalação automática (Windows)
├── 🚀 start_app.bat                   # Iniciar aplicação
├── 📂 Dados_Json/                     # Versões bíblicas por idioma
│   ├── pt/                            # Português (NVI, ACF, AA)
│   ├── en/                            # English (KJV, NIV, ESV)
│   └── es/                            # Español (RV1960, RV1995)
├── 📂 chroma_db/                      # Banco de dados (históricos)
│   ├── study_history/                 # Histórico de estudos
│   ├── sermon_history/                # Histórico de sermões
│   ├── devotional_history/            # Histórico de devocionais
│   ├── chat_history/                  # Histórico de conversas
│   └── questions_history/             # Histórico de perguntas
├── 📂 locales/                        # Traduções (pt, en, es)
│   ├── pt.json                        # Português
│   ├── en.json                        # English
│   └── es.json                        # Español
└── 📂 .venv/                          # Ambiente virtual Python
```

---

## 🔧 Solução de Problemas

### ❌ Ollama não conecta

```bash
# Verificar status
curl http://localhost:11434/api/version

# Iniciar manualmente
ollama serve

# Windows: verificar se está rodando
tasklist | findstr ollama
```

### ❌ Modelo não encontrado

```bash
# Listar modelos instalados
ollama list

# Baixar modelo recomendado
ollama pull llama3.2:1b

# Testar modelo
ollama run llama3.2:1b "Olá"
```

### ❌ Erro ao importar versões

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar estrutura de pastas
dir Dados_Json\pt
```

### ❌ ChromaDB não salva dados

```bash
# Verificar permissões da pasta chroma_db
icacls chroma_db

# Recriar banco de dados
rmdir /s /q chroma_db
python -c "import chromadb; chromadb.Client()"
```

### ❌ Timeout ao gerar sermão

✅ **Solução implementada!** O sistema agora usa **timeout dinâmico**:
- Sermões simples: 4 minutos
- Sermões complexos: até **10 minutos**
- Auto-continuação: até 5 continuações automáticas

---

## 🤝 Contribuindo

Contribuições são **muito bem-vindas**! Siga os passos:

1. **Fork** o repositório
2. Crie uma **branch** para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um **Pull Request**

### 📝 Diretrizes

- Use **PEP 8** para código Python
- Documente novas funcionalidades
- Teste antes de enviar PR
- Mantenha compatibilidade com Python 3.8+

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🐛 Reportar Bugs

Encontrou um bug? Abra uma [Issue](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/issues) com:

- ✅ Descrição clara do problema
- ✅ Passos para reproduzir
- ✅ Comportamento esperado vs atual
- ✅ Screenshots (se aplicável)
- ✅ Informações do sistema (Windows, Python, Ollama)

---

## 🗺️ Roadmap

### ✅ Já Implementado
- [x] 6 abas funcionais (Leitura, Sermão, Devocional, Chat, Perguntas, Importar)
- [x] 7 personas de sermão (Analítico, Narrativo, Profético, etc.)
- [x] Seleção de múltiplos versículos (ex: "1-5, 10, 15-20")
- [x] Históricos persistentes com ChromaDB
- [x] Gerador de perguntas (1-50 questões)
- [x] Exportação para PDF
- [x] Suporte multilíngue (pt, en, es)
- [x] Timeout dinâmico (até 10 min)
- [x] Auto-continuação inteligente

### 🚧 Em Desenvolvimento
- [ ] Comparação de versões lado a lado
- [ ] Mapa bíblico interativo
- [ ] Timeline de eventos bíblicos
- [ ] Concordância bíblica integrada
- [ ] Modo de estudo em grupo (colaborativo)

### 💡 Futuras Ideias
- [ ] App mobile (React Native)
- [ ] API REST para integração
- [ ] Plugin para WordPress
- [ ] Integração com apps de sermões
- [ ] Sistema de anotações e marcações

---

<div align="center">

## 💝 Apoie o Projeto

Este projeto é **gratuito e open-source**, mantido com dedicação para ajudar pastores, estudantes de teologia e cristãos no estudo da Palavra de Deus.

Se este sistema tem sido útil para você, considere apoiar o desenvolvimento com uma contribuição:

### ☕ **[Doar via PayPal](https://www.paypal.com/donate/?business=9SNHLWN6MUJAQ&no_recurring=0&item_name=Feito+com+dedicação.+Se+puder,+apoie+o+tempo+e+os+custos+de+criação+deste+projeto.&currency_code=BRL)**

<div align="center">

[![Donate with PayPal](https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=9SNHLWN6MUJAQ&no_recurring=0&item_name=Feito+com+dedicação.+Se+puder,+apoie+o+tempo+e+os+custos+de+criação+deste+projeto.&currency_code=BRL)

</div>

*Sua doação ajuda a:*
- ⚡ Manter o projeto ativo e atualizado
- 🚀 Desenvolver novas funcionalidades
- 📚 Adicionar mais recursos teológicos
- 🌍 Expandir suporte a mais idiomas
- 💻 Melhorar a infraestrutura e hospedagem

---

**Toda contribuição é muito apreciada! 🙏**

---

### 📧 Contato

Dúvidas ou sugestões? Entre em contato:

- � Issues: [GitHub Issues](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/issues)
- 🌐 Repositório: [GitHub](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama)

---

### ⭐ Gostou do Projeto?

Se este sistema foi útil para você:
- ⭐ Dê uma **estrela** no GitHub
- 🔄 **Compartilhe** com outros pastores e estudantes
- 🐛 **Reporte bugs** para melhorarmos
- 💝 **Contribua** com código ou ideias

---

**Feito com ❤️ e dedicação para a glória de Deus**

*"Lâmpada para os meus pés é a tua palavra e luz, para o meu caminho." - Salmos 119:105*

---

[![GitHub Stars](https://img.shields.io/github/stars/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama?style=social)](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama?style=social)](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama)](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/issues)

</div>
Biblia/
├── app.py                    # Aplicação principal Streamlit
├── bible_data_importer.py    # Importador de versões bíblicas
├── requirements.txt          # Dependências Python
├── .env                      # Configurações (criar após setup)
├── setup.bat                 # Instalador automático Windows
├── start_app.bat             # Inicializador da aplicação
├── INSTALL.md               # Guia detalhado de instalação
├── README.md                # Este arquivo
├── bible_data.json          # Dados bíblicos (gerado após importar)
└── .venv/                   # Ambiente virtual Python
```

## 🌟 Destaques

### 🔒 Totalmente Offline
- Todos os dados bíblicos armazenados localmente
- IA roda completamente no seu computador
- Nenhum dado enviado para servidores externos

### ⚡ Rápido e Leve
- Modelo `llama3.2:1b` otimizado para velocidade
- Interface responsiva e moderna
- Baixo consumo de recursos

### 📚 Completo
- 6 abas funcionais
- 4 históricos independentes
- Suporte a múltiplas versões bíblicas
- Interface em português

## 🎨 Interface

A aplicação possui modo escuro automático que se adapta ao tema do sistema, com:

- 🎯 Design limpo e intuitivo
- 📱 Layout responsivo
- 🔍 Busca integrada em todos os históricos
- 🎭 Ícones descritivos para fácil navegação

## 📈 Roadmap

- [ ] Persistência de históricos em banco de dados
- [ ] Exportação de estudos em PDF/Word
- [ ] Comparação lado a lado de versões
- [ ] Mapas e cronologias interativas
- [ ] Sistema de favoritos e tags
- [ ] Planos de leitura personalizados

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Enviar pull requests
4. Melhorar a documentação

## 📄 Licença

Este projeto é de código aberto para fins educacionais e de estudo bíblico.

## 🙏 Agradecimentos

- Comunidade **Ollama** pelo framework de IA local
- Projeto **Streamlit** pela interface web
- Repositórios de dados bíblicos em português(thiagobodruk)
com o projeto: https://github.com/thiagobodruk/biblia/commits?author=thiagobodruk(Foi usado o arquivo Json com a biblia nas 3 traduções.)
- Todos que contribuem para ferramentas de estudo bíblico

---

**Desenvolvido com ❤️ para o estudo da Palavra de Deus**

*"Lâmpada para os meus pés é a tua palavra e luz, para o meu caminho." - Salmos 119:105*
