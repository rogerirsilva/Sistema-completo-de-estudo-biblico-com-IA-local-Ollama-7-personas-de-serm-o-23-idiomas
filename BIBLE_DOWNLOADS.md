# 📖 Guia de Download de Bíblias em JSON

Este documento contém links diretos para baixar versões da Bíblia em JSON para os **23 idiomas** suportados pelo sistema.

> **✅ Status:** 28 arquivos em 23 idiomas - 117+ MB de dados bíblicos

**📋 Índice Rápido:**
- [Idiomas Disponíveis](#idiomas-disponíveis)
- [Script Automático](#-script-completo-para-baixar-todos-os-idiomas)
- [Agradecimentos e Créditos](CREDITS.md)

---

## 🌍 Idiomas Disponíveis

| Flag | Idioma | Código | Versões | Fonte |
|------|--------|--------|---------|-------|
| 🇧🇷 | Português | `pt` | 3 | thiagobodruk/bible |
| 🇺🇸 | English | `en` | 2 | thiagobodruk/bible |
| 🇪🇸 | Español | `es` | 1 | thiagobodruk/bible |
| 🇫🇷 | Français | `fr` | 1 | thiagobodruk/bible |
| 🇩🇪 | Deutsch | `de` | 1 | thiagobodruk/bible |
| 🇷🇺 | Русский | `ru` | 1 | thiagobodruk/bible |
| 🇨🇳 | 中文 | `zh` | 2 | thiagobodruk/bible |
| 🇸🇦 | العربية | `ar` | 1 | thiagobodruk/bible |
| 🇬🇷 | Ελληνικά | `el` | 1 | thiagobodruk/bible |
| 🌍 | Esperanto | `eo` | 1 | thiagobodruk/bible |
| 🇫🇮 | Suomi | `fi` | 2 | thiagobodruk/bible |
| 🇰🇷 | 한국어 | `ko` | 1 | thiagobodruk/bible |
| 🇷🇴 | Română | `ro` | 1 | thiagobodruk/bible |
| 🇻🇳 | Tiếng Việt | `vi` | 1 | thiagobodruk/bible |
| 🇮🇹 | Italiano | `it` | 1 ✨ | BibleSuperSearch |
| 🇯🇵 | 日本語 | `ja` | 1 ✨ | BibleSuperSearch |
| 🇮🇩 | Bahasa Indonesia | `id` | 1 ✨ | BibleSuperSearch |
| 🇮🇳 | हिन्दी | `hi` | 1 ✨ | BibleSuperSearch |
| 🇵🇱 | Polski | `pl` | 1 ✨ | BibleSuperSearch |
| 🇮🇷 | فارسی | `fa` | 1 ✨ | BibleSuperSearch |
| 🇹🇿 | Kiswahili | `sw` | 1 ✨ | BibleSuperSearch |
| 🇹🇭 | ไทย | `th` | 1 ✨ | BibleSuperSearch |
| 🇹🇷 | Türkçe | `tr` | 1 ✨ | BibleSuperSearch |

✨ = Novos idiomas adicionados recentemente

---

## 🇧🇷 Português (pt)

### Repositório: thiagobodruk/bible

**Versões Disponíveis:**
- **NVI** (Nova Versão Internacional): [`pt_nvi.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json)
- **ACF** (Almeida Corrigida Fiel): [`pt_acf.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_acf.json)
- **AA** (Almeida Revisada Imprensa Bíblica): [`pt_aa.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_aa.json)

**Como baixar:**
```powershell
# Criar pasta pt se não existir
New-Item -ItemType Directory -Force -Path "Dados_Json\pt"

# Baixar as 3 versões
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json" -OutFile "Dados_Json\pt\nvi.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_acf.json" -OutFile "Dados_Json\pt\acf.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_aa.json" -OutFile "Dados_Json\pt\aa.json"
```

---

## 🇺🇸 English (en)

### Repositório 1: thiagobodruk/bible

**Versões Disponíveis:**
- **KJV** (King James Version): [`en_kjv.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json)
- **BBE** (Basic English Bible): [`en_bbe.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_bbe.json)

### Repositório 2: scrollmapper/bible_databases

Este repositório tem 140 versões em vários idiomas, mas está em formato SQL/CSV/YAML. Você pode baixar:

**Link:** https://github.com/scrollmapper/bible_databases/tree/master/formats

**Versões recomendadas (requerem conversão):**
- KJV, AKJV, ASV, BSB, ESV, NIV, NKJV, etc.

**Como baixar (thiagobodruk):**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\en"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json" -OutFile "Dados_Json\en\kjv.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_bbe.json" -OutFile "Dados_Json\en\bbe.json"
```

---

## 🇪🇸 Español (es)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **RVR** (Reina Valera): [`es_rvr.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/es_rvr.json)

### Alternativa: scrollmapper/bible_databases

Contém mais versões como RV1960, RV1865, RVG em formatos SQL/CSV.

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\es"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/es_rvr.json" -OutFile "Dados_Json\es\rvr.json"
```

---

## 🇫🇷 Français (fr)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **APEE** (Le Bible de I'Épée): [`fr_apee.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fr_apee.json)

### Alternativa: scrollmapper/bible_databases

Versões como Louis Segond (FreCrampon, FreBDM1744, FreJND) em SQL/CSV.

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\fr"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fr_apee.json" -OutFile "Dados_Json\fr\apee.json"
```

---

## 🇩🇪 Deutsch (de)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Schlachter**: [`de_schlachter.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/de_schlachter.json)

### Alternativa: scrollmapper/bible_databases

Versões como Luther (GerLut1545), Elberfelder (GerElb1905), Menge (GerMenge) em SQL/CSV.

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\de"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/de_schlachter.json" -OutFile "Dados_Json\de\schlachter.json"
```

---

## 🇮🇹 Italiano (it)

### Repositório: scrollmapper/bible_databases

**Versões Disponíveis (em SQL/CSV):**
- **NuovaRiveduta** (ItalianRiveduta)
- **Diodati**

⚠️ **Nota:** Não há versões em JSON prontas. Você precisará:
1. Baixar o repositório completo
2. Usar scripts Python para converter
3. Ou procurar outros repositórios

**Link alternativo:**
- Procure por "italian bible json github"
- https://github.com/search?q=italian+bible+json

---

## 🇷🇺 Русский (ru)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Synodal**: [`ru_synodal.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\ru"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json" -OutFile "Dados_Json\ru\synodal.json"
```

---

## 🇨🇳 中文 (zh)

### Repositório: thiagobodruk/bible

**Versões Disponíveis:**
- **CUV** (Chinese Union Version): [`zh_cuv.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_cuv.json)
- **NCV** (New Chinese Version): [`zh_ncv.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_ncv.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\zh"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_cuv.json" -OutFile "Dados_Json\zh\cuv.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_ncv.json" -OutFile "Dados_Json\zh\ncv.json"
```

---

## 🇯🇵 日本語 (ja)

### Repositório: scrollmapper/bible_databases

**Versões Disponíveis (em SQL/CSV):**
- **Kougo-yaku** (口語訳)
- **Bungo** (文語訳)

⚠️ **Nota:** Não há versões JSON prontas. Alternativas:

1. **Converter do scrollmapper**:
   - Baixe: https://github.com/scrollmapper/bible_databases
   - Use o script Python para converter

2. **Procurar repositórios japoneses**:
   ```
   https://github.com/search?q=japanese+bible+json
   ```

---

## 🇸🇦 العربية (ar)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **SVD** (Smith & Van Dyke): [`ar_svd.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ar_svd.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\ar"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ar_svd.json" -OutFile "Dados_Json\ar\svd.json"
```

---

## 🚀 Script Completo para Baixar Todos os Idiomas

Execute este script PowerShell para baixar todas as versões disponíveis em JSON:

```powershell
# Script de Download Automático de Bíblias JSON
Write-Host "Baixando versões da Bíblia em JSON..." -ForegroundColor Cyan

# Criar estrutura de pastas
$idiomas = @("pt", "en", "es", "fr", "de", "ru", "zh", "ar", "el", "eo", "fi", "ko", "ro", "vi")
foreach ($lang in $idiomas) {
    New-Item -ItemType Directory -Force -Path "Dados_Json\$lang" | Out-Null
}

# Português (pt) - 3 versões
Write-Host "Baixando Português (pt)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json" -OutFile "Dados_Json\pt\nvi.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_acf.json" -OutFile "Dados_Json\pt\acf.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_aa.json" -OutFile "Dados_Json\pt\aa.json"

# English (en) - 2 versões
Write-Host "Baixando English (en)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json" -OutFile "Dados_Json\en\kjv.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_bbe.json" -OutFile "Dados_Json\en\bbe.json"

# Español (es) - 1 versão
Write-Host "Baixando Español (es)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/es_rvr.json" -OutFile "Dados_Json\es\rvr.json"

# Français (fr) - 1 versão
Write-Host "Baixando Français (fr)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fr_apee.json" -OutFile "Dados_Json\fr\apee.json"

# Deutsch (de) - 1 versão
Write-Host "Baixando Deutsch (de)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/de_schlachter.json" -OutFile "Dados_Json\de\schlachter.json"

# Русский (ru) - 1 versão
Write-Host "Baixando Русский (ru)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json" -OutFile "Dados_Json\ru\synodal.json"

# 中文 (zh) - 2 versões
Write-Host "Baixando 中文 (zh)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_cuv.json" -OutFile "Dados_Json\zh\cuv.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/zh_ncv.json" -OutFile "Dados_Json\zh\ncv.json"

# العربية (ar) - 1 versão
Write-Host "Baixando العربية (ar)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ar_svd.json" -OutFile "Dados_Json\ar\svd.json"

# Ελληνικά (el) - 1 versão
Write-Host "Baixando Ελληνικά (el)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/el_greek.json" -OutFile "Dados_Json\el\greek.json"

# Esperanto (eo) - 1 versão
Write-Host "Baixando Esperanto (eo)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/eo_esperanto.json" -OutFile "Dados_Json\eo\esperanto.json"

# Suomi (fi) - 2 versões
Write-Host "Baixando Suomi (fi)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_finnish.json" -OutFile "Dados_Json\fi\finnish.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_pr.json" -OutFile "Dados_Json\fi\pr.json"

# 한국어 (ko) - 1 versão
Write-Host "Baixando 한국어 (ko)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ko_ko.json" -OutFile "Dados_Json\ko\korean.json"

# Română (ro) - 1 versão
Write-Host "Baixando Română (ro)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ro_cornilescu.json" -OutFile "Dados_Json\ro\cornilescu.json"

# Tiếng Việt (vi) - 1 versão
Write-Host "Baixando Tiếng Việt (vi)..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/vi_vietnamese.json" -OutFile "Dados_Json\vi\vietnamese.json"

Write-Host "`n✅ Download concluído!" -ForegroundColor Green
Write-Host "`n📊 Resumo:" -ForegroundColor Cyan
Write-Host "  • 14 idiomas baixados" -ForegroundColor White
Write-Host "  • 19 arquivos JSON" -ForegroundColor White
Write-Host "  • ~81 MB de dados bíblicos" -ForegroundColor White
```

---

## 🇬🇷 Grego (el)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Modern Greek**: [`el_greek.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/el_greek.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\el"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/el_greek.json" -OutFile "Dados_Json\el\greek.json"
```

---

## 🌍 Esperanto (eo)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Esperanto**: [`eo_esperanto.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/eo_esperanto.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\eo"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/eo_esperanto.json" -OutFile "Dados_Json\eo\esperanto.json"
```

---

## 🇫🇮 Suomi (fi)

### Repositório: thiagobodruk/bible

**Versões Disponíveis:**
- **Finnish Bible**: [`fi_finnish.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_finnish.json)
- **Pyhä Raamattu**: [`fi_pr.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_pr.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\fi"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_finnish.json" -OutFile "Dados_Json\fi\finnish.json"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/fi_pr.json" -OutFile "Dados_Json\fi\pr.json"
```

---

## 🇰🇷 한국어 (ko)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Korean Version**: [`ko_ko.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ko_ko.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\ko"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ko_ko.json" -OutFile "Dados_Json\ko\korean.json"
```

---

## 🇷🇴 Română (ro)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Dumitru Cornilescu**: [`ro_cornilescu.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ro_cornilescu.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\ro"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ro_cornilescu.json" -OutFile "Dados_Json\ro\cornilescu.json"
```

---

## 🇻🇳 Tiếng Việt (vi)

### Repositório: thiagobodruk/bible

**Versão Disponível:**
- **Vietnamese Bible**: [`vi_vietnamese.json`](https://raw.githubusercontent.com/thiagobodruk/bible/master/json/vi_vietnamese.json)

**Como baixar:**
```powershell
New-Item -ItemType Directory -Force -Path "Dados_Json\vi"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/vi_vietnamese.json" -OutFile "Dados_Json\vi\vietnamese.json"
```

---

---

## 🆕 Idiomas Adicionados do BibleSuperSearch

### 🇮🇹 Italiano (it)

**Versão:** Diodati (1649)  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/it/diodati.json`

---

### 🇯🇵 日本語 (ja)

**Versão:** Kougo-yaku (1954/1955) 口語訳  
**Formato:** Convertido de TXT para JSON  
**Status:** ⚠️ Em processamento (nomes de livros em japonês)

---

### 🇮🇩 Bahasa Indonesia (id)

**Versão:** Terjemahan Lama  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/id/indo_tm.json`

---

### 🇮🇳 हिन्दी (hi)

**Versão:** Indian Revised Version (IRV) 2017/2018  
**Formato:** Convertido de TXT para JSON  
**Status:** ⚠️ Em processamento

---

### 🇵🇱 Polski (pl)

**Versão:** Uwspółcześniona Biblia Gdańska (UBG) 2017  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/pl/pol_ubg.json`

---

### 🇮🇷 فارسی (fa)

**Versão:** Old Persian Translation (OPT) 1895  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/fa/opt.json`

---

### 🇹🇿 Kiswahili (sw)

**Versão:** Swahili NT (Novo Testamento)  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/sw/swahili.json`

---

### 🇹🇭 ไทย (th)

**Versão:** Thai KJV  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/th/thaikjv.json`

---

### 🇹🇷 Türkçe (tr)

**Versão:** Turkish Bible  
**Formato:** Convertido de TXT para JSON  
**Como baixar:** Já convertido e disponível em `Dados_Json/tr/turkish.json`

---

## ⚠️ Idiomas sem JSON Pronto

### Italiano (it) e Japonês (ja)

Estes idiomas não têm versões JSON prontas no repositório thiagobodruk/bible. Você tem 3 opções:

#### Opção 1: Converter do scrollmapper/bible_databases

1. Clone o repositório:
   ```powershell
   git clone https://github.com/scrollmapper/bible_databases.git
   ```

2. Navegue até a pasta formats/json/

3. Use os scripts Python incluídos para converter

#### Opção 2: Procurar outros repositórios

- **Italiano**: https://github.com/search?q=italian+bible+json
- **Japonês**: https://github.com/search?q=japanese+bible+json

#### Opção 3: Solicitar conversão manual

Entre em contato com a comunidade ou use ferramentas de conversão SQL→JSON.

---

## 📚 Formato Esperado

O sistema espera arquivos JSON no seguinte formato:

```json
[
  {
    "abbrev": "gn",
    "book": "Gênesis",
    "chapters": [
      [
        "No princípio Deus criou os céus e a terra.",
        "Era a terra sem forma e vazia..."
      ],
      [
        "Assim foram concluídos os céus e a terra..."
      ]
    ]
  }
]
```

Se você baixar versões de outras fontes, verifique se o formato é compatível!

---

## 🔗 Links Úteis

- **thiagobodruk/bible**: https://github.com/thiagobodruk/bible
- **scrollmapper/bible_databases**: https://github.com/scrollmapper/bible_databases
- **API.Bible** (requer chave): https://scripture.api.bible/
- **Bible.com API**: https://www.bible.com/

---

## 📝 Licença

Cada versão da Bíblia possui sua própria licença. Verifique os direitos autorais antes de distribuir:

- **Domínio Público**: KJV, ASV, BBE, RVR, etc.
- **Creative Commons**: NVI (uso não comercial)
- **Protegidas**: ESV, NIV, NKJV (requerem permissão)

---

**Última Atualização:** 12 de dezembro de 2025
