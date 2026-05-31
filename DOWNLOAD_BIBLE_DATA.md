# Como Baixar Dados Bíblicos para Hindi e Japonês

## Problema
Os arquivos `Dados_Json/hi/irv.json` e `Dados_Json/ja/kougo.json` existem mas estão vazios (`[]`).

## Soluções

### Opção 1: Download Automático (Recomendado)
1. Execute o aplicativo: `streamlit run app.py`
2. Selecione o idioma desejado (हिन्दी ou 日本語)
3. Vá para a aba "📥 Importar Dados"
4. Use os botões de importação para baixar os dados

### Opção 2: Download Manual

#### Para Hindi (हिन्दी):
```bash
# Baixar do GitHub - BibleSuperSearch
curl -o Dados_Json/hi/irv.json https://raw.githubusercontent.com/BibleSuperSearch/bibles/master/JSON/hi_irv.json
```

#### Para Japonês (日本語):
```bash
# Baixar do GitHub - thiagobodruk/bible
curl -o Dados_Json/ja/kougo.json https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ja_kougo.json
```

### Opção 3: Usar Outros Idiomas
Os seguintes idiomas têm dados completos:
- ✅ Português (pt) - ACF, NVI
- ✅ English (en)
- ✅ Español (es)
- ✅ Français (fr)
- ✅ Deutsch (de)
- ✅ Türkçe (tr)
- ✅ العربية (ar)
- ✅ Русский (ru)
- ✅ 中文 (zh)

## Estrutura do Arquivo JSON Esperada

Os arquivos devem ter esta estrutura:
```json
[
  {
    "abbrev": "gn",
    "name": "उत्पत्ति",  // Nome traduzido
    "chapters": [
      ["versículo 1", "versículo 2", ...],  // Capítulo 1
      ["versículo 1", "versículo 2", ...]   // Capítulo 2
    ]
  },
  {
    "abbrev": "ex",
    "name": "निर्गमन",
    "chapters": [...]
  }
]
```

## Verificar se Funcionou

Execute o teste:
```bash
python test_hindi_japanese.py
```

Deve mostrar o número de livros carregados (66 livros completos para Bíblia inteira).

## Fontes de Dados Bíblicos

1. **BibleSuperSearch**: https://github.com/BibleSuperSearch/bibles
   - Muitos idiomas disponíveis
   - Formato JSON compatível

2. **thiagobodruk/bible**: https://github.com/thiagobodruk/bible
   - Idiomas principais
   - Formato JSON compatível

3. **API.Bible**: https://scripture.api.bible/
   - Requer API key gratuita
   - Muitas traduções disponíveis
