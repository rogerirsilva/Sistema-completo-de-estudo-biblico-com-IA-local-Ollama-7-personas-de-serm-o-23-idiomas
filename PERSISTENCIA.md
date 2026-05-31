# 📦 Persistência de Dados com ChromaDB

## O que foi implementado?

A aplicação agora salva automaticamente todos os históricos em um banco de dados local (ChromaDB), garantindo que seus estudos, sermões, devocionais e conversas não sejam perdidos ao reiniciar a aplicação.

## Instalação

### 1. Instalar ChromaDB

```bash
pip install chromadb
```

Ou instalar todas as dependências atualizadas:

```bash
pip install -r requirements.txt
```

### 2. Primeira execução

Na primeira vez que você executar a aplicação após instalar o ChromaDB, ela irá:

1. Criar uma pasta `chroma_db/` no diretório do projeto
2. Carregar quaisquer históricos salvos anteriormente
3. A partir desse momento, todos os dados serão automaticamente salvos

## Funcionalidades

### ✅ Salvamento Automático

Todos os dados são salvos automaticamente quando você:
- 🔍 Gera uma explicação bíblica
- 🔍 Compara versões de traduções
- 🎤 Cria um sermão
- 🧘 Gera um devocional
- 💬 Faz uma pergunta no chat teológico

### ✅ Carregamento Automático

Ao iniciar a aplicação, todos os seus dados anteriores são carregados automaticamente:
- 📚 Histórico de Estudos Bíblicos
- 📋 Histórico de Sermões
- 🕊️ Histórico de Devocionais
- 💭 Histórico de Conversas

### ✅ Sincronização em Tempo Real

Qualquer ação que você realizar é imediatamente salva:
- Adicionar novo estudo ✅
- Deletar um item ✅
- Limpar todo o histórico ✅

## Estrutura dos Dados

```
chroma_db/
├── chroma.sqlite3          # Banco de dados SQLite
└── [arquivos internos]     # Arquivos de índice do ChromaDB
```

## Backup Manual

Para fazer backup dos seus dados, simplesmente copie a pasta `chroma_db/` para outro local seguro.

```bash
# Windows
xcopy chroma_db backup_chroma_db /E /I

# Linux/Mac
cp -r chroma_db backup_chroma_db
```

## Restaurar Backup

Para restaurar um backup, substitua a pasta `chroma_db/` pela cópia de backup:

```bash
# Windows
rmdir /s /q chroma_db
xcopy backup_chroma_db chroma_db /E /I

# Linux/Mac
rm -rf chroma_db
cp -r backup_chroma_db chroma_db
```

## Limpar Todos os Dados

Se desejar começar do zero, você pode deletar a pasta `chroma_db/`:

```bash
# Windows
rmdir /s /q chroma_db

# Linux/Mac
rm -rf chroma_db
```

A aplicação criará uma nova pasta vazia na próxima execução.

## Busca Semântica (Futuro)

O ChromaDB permite busca semântica nos seus estudos. Em versões futuras, você poderá:
- 🔍 Buscar estudos por similaridade de conteúdo
- 🤖 Encontrar sermões relacionados a um tema
- 💡 Descobrir devocionais com sentimentos similares
- 📊 Analisar padrões nos seus estudos

## Troubleshooting

### Erro: "ChromaDB não está instalado"

Execute:
```bash
pip install chromadb
```

### Erro: "Erro ao inicializar ChromaDB"

1. Verifique se a pasta `chroma_db/` tem permissões de escrita
2. Tente deletar a pasta `chroma_db/` e reiniciar a aplicação
3. Verifique se não há outro processo usando o banco de dados

### Os dados não estão sendo salvos

1. Verifique se o ChromaDB foi instalado corretamente
2. Procure por mensagens de erro na interface do Streamlit
3. Verifique as permissões da pasta `chroma_db/`

## Performance

O ChromaDB é otimizado para:
- ⚡ Salvamento rápido (< 100ms)
- 📦 Armazenamento eficiente
- 🔍 Busca instantânea
- 💾 Baixo uso de memória

## Segurança

- 🔒 Todos os dados ficam armazenados localmente
- 🔐 Nenhuma informação é enviada para servidores externos
- 🛡️ Você tem controle total sobre seus dados
