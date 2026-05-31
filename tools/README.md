# 🛠️ Scripts de Ferramentas e Utilitários

Esta pasta contém scripts auxiliares usados para desenvolvimento, manutenção e processamento de dados do sistema de Estudo Bíblico.

## 📂 Categorias de Scripts

### 🌍 Traduções
Scripts para adicionar/verificar traduções da interface:
- `add_*_translations.py` - Adicionar traduções específicas
- `check_*_translations.py` - Verificar traduções faltantes
- `apply_proper_translations.py` - Aplicar traduções corretas

### 📚 Processamento de Dados Bíblicos
- `convert_txt_to_json.py` - Converter bíblias TXT para JSON
- `convert_txt_bibles.py` - Processar múltiplas bíblias
- `import_github_data.py` - Importar dados do GitHub
- `inspect_zip.py` - Inspecionar arquivos ZIP de bíblias

### 🔧 Completar Dados
- `complete_all_translations.py` - Completar todas as traduções
- `complete_arabic.py` - Completar tradução árabe
- `complete_12_languages.py` - Completar 12 idiomas

### ⚙️ Configuração
- `setup_database.py` - Configurar banco de dados
- `test_ollama_integration.py` - Testar integração com Ollama

## 🚀 Como Usar

### Executar um script:
```bash
# Ativar ambiente virtual primeiro
.venv\Scripts\activate

# Executar script
python tools/nome_do_script.py
```

### Exemplo - Adicionar Traduções:
```bash
python tools/add_missing_translations.py
```

### Exemplo - Converter Bíblias:
```bash
python tools/convert_txt_to_json.py
```

## ⚠️ Importante

- Estes scripts são para **uso interno/desenvolvimento**
- **NÃO** são necessários para executar a aplicação principal
- Execute apenas se souber o que está fazendo
- Sempre faça backup antes de executar scripts de conversão

## 📋 Scripts do Sistema Principal

Os seguintes arquivos **permanecem na raiz** pois são essenciais:
- `app.py` - Aplicação principal Streamlit
- `bible_data_importer.py` - Módulo importado pelo app.py
- `book_names_mapping.py` - Módulo importado pelo app.py

## 🗑️ Limpeza

Se não precisar mais fazer desenvolvimento/manutenção, você pode:
- Manter esta pasta (não ocupa muito espaço)
- Ou deletar completamente (não afeta o funcionamento do app)

```bash
# Deletar pasta tools (se não precisar)
Remove-Item -Recurse -Force tools
```

## 📚 Documentação

Para usar a aplicação principal, consulte:
- [README.md](../README.md) - Documentação geral
- [INSTALL.md](../INSTALL.md) - Guia de instalação
- [DOCUMENTATION.md](../DOCUMENTATION.md) - Documentação técnica
