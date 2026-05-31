#!/usr/bin/env python3
"""Script para adicionar traduções faltantes."""

import json
from pathlib import Path

# Traduções adicionais
ADDITIONAL_TRANSLATIONS = {
    "pt": {
        "reading_page": "Página de leitura",
        "no_verses_in_chapter": "Nenhum versículo encontrado neste capítulo.",
        "set_default_version": "Definir como versão padrão ao iniciar",
        "no_local_versions": "Nenhuma versão local encontrada. Use Importar Dados para carregar conteúdo.",
        "importing_versions": "⏳ Importando versões...",
        "context_label": "Contexto:",
        "explanation_label": "Explicação:",
        "timestamp_format": "%d/%m/%Y às %H:%M"
    },
    "en": {
        "reading_page": "Reading page",
        "no_verses_in_chapter": "No verses found in this chapter.",
        "set_default_version": "Set as default version on startup",
        "no_local_versions": "No local versions found. Use Import Data to load content.",
        "importing_versions": "⏳ Importing versions...",
        "context_label": "Context:",
        "explanation_label": "Explanation:",
        "timestamp_format": "%m/%d/%Y at %I:%M %p"
    },
    "es": {
        "reading_page": "Página de lectura",
        "no_verses_in_chapter": "No se encontraron versículos en este capítulo.",
        "set_default_version": "Establecer como versión predeterminada al iniciar",
        "no_local_versions": "No se encontraron versiones locales. Use Importar Datos para cargar contenido.",
        "importing_versions": "⏳ Importando versiones...",
        "context_label": "Contexto:",
        "explanation_label": "Explicación:",
        "timestamp_format": "%d/%m/%Y a las %H:%M"
    },
    "fr": {
        "reading_page": "Page de lecture",
        "no_verses_in_chapter": "Aucun verset trouvé dans ce chapitre.",
        "set_default_version": "Définir comme version par défaut au démarrage",
        "no_local_versions": "Aucune version locale trouvée. Utilisez Importer des données pour charger du contenu.",
        "importing_versions": "⏳ Importation des versions...",
        "context_label": "Contexte:",
        "explanation_label": "Explication:",
        "timestamp_format": "%d/%m/%Y à %H:%M"
    },
    "de": {
        "reading_page": "Leseabschnitt",
        "no_verses_in_chapter": "Keine Verse in diesem Kapitel gefunden.",
        "set_default_version": "Als Standardversion beim Start festlegen",
        "no_local_versions": "Keine lokalen Versionen gefunden. Verwenden Sie Daten importieren, um Inhalte zu laden.",
        "importing_versions": "⏳ Versionen werden importiert...",
        "context_label": "Kontext:",
        "explanation_label": "Erklärung:",
        "timestamp_format": "%d.%m.%Y um %H:%M"
    },
    "ar": {
        "reading_page": "صفحة القراءة",
        "no_verses_in_chapter": "لم يتم العثور على آيات في هذا الفصل.",
        "set_default_version": "تعيين كإصدار افتراضي عند البدء",
        "no_local_versions": "لم يتم العثور على إصدارات محلية. استخدم استيراد البيانات لتحميل المحتوى.",
        "importing_versions": "⏳ جاري استيراد الإصدارات...",
        "context_label": "السياق:",
        "explanation_label": "التفسير:",
        "timestamp_format": "%d/%m/%Y في %H:%M"
    },
    "hi": {
        "reading_page": "पढ़ने का पृष्ठ",
        "no_verses_in_chapter": "इस अध्याय में कोई पद नहीं मिला।",
        "set_default_version": "प्रारंभ पर डिफ़ॉल्ट संस्करण के रूप में सेट करें",
        "no_local_versions": "कोई स्थानीय संस्करण नहीं मिला। सामग्री लोड करने के लिए डेटा आयात का उपयोग करें।",
        "importing_versions": "⏳ संस्करण आयात किए जा रहे हैं...",
        "context_label": "संदर्भ:",
        "explanation_label": "व्याख्या:",
        "timestamp_format": "%d/%m/%Y को %H:%M"
    },
    "ja": {
        "reading_page": "読書ページ",
        "no_verses_in_chapter": "この章には節が見つかりませんでした。",
        "set_default_version": "起動時のデフォルトバージョンとして設定",
        "no_local_versions": "ローカルバージョンが見つかりません。データインポートを使用してコンテンツをロードしてください。",
        "importing_versions": "⏳ バージョンをインポート中...",
        "context_label": "コンテキスト:",
        "explanation_label": "説明:",
        "timestamp_format": "%Y/%m/%d %H:%M"
    },
    "ru": {
        "reading_page": "Страница чтения",
        "no_verses_in_chapter": "В этой главе не найдено стихов.",
        "set_default_version": "Установить как версию по умолчанию при запуске",
        "no_local_versions": "Локальные версии не найдены. Используйте Импорт данных для загрузки содержимого.",
        "importing_versions": "⏳ Импорт версий...",
        "context_label": "Контекст:",
        "explanation_label": "Объяснение:",
        "timestamp_format": "%d.%m.%Y в %H:%M"
    },
    "zh": {
        "reading_page": "阅读页面",
        "no_verses_in_chapter": "在此章节中未找到经文。",
        "set_default_version": "设置为启动时的默认版本",
        "no_local_versions": "未找到本地版本。使用导入数据加载内容。",
        "importing_versions": "⏳ 正在导入版本...",
        "context_label": "上下文:",
        "explanation_label": "说明:",
        "timestamp_format": "%Y/%m/%d %H:%M"
    },
    "it": {
        "reading_page": "Pagina di lettura",
        "no_verses_in_chapter": "Nessun versetto trovato in questo capitolo.",
        "set_default_version": "Imposta come versione predefinita all'avvio",
        "no_local_versions": "Nessuna versione locale trovata. Usa Importa dati per caricare il contenuto.",
        "importing_versions": "⏳ Importazione versioni...",
        "context_label": "Contesto:",
        "explanation_label": "Spiegazione:",
        "timestamp_format": "%d/%m/%Y alle %H:%M"
    }
}

def add_additional_translations():
    translations_dir = Path("translations")
    
    for lang_code, translations in ADDITIONAL_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            # Adicionar em messages
            if "messages" not in data:
                data["messages"] = {}
                changed = True
            
            for key in ["no_verses_in_chapter", "no_local_versions", "importing_versions"]:
                if key in translations:
                    if key not in data["messages"] or data["messages"][key] != translations[key]:
                        data["messages"][key] = translations[key]
                        changed = True
                        print(f"  ✅ {lang_code}.json messages.{key}")
            
            # Adicionar em labels
            if "labels" not in data:
                data["labels"] = {}
                changed = True
            
            for key in ["reading_page", "set_default_version"]:
                if key in translations:
                    if key not in data["labels"] or data["labels"][key] != translations[key]:
                        data["labels"][key] = translations[key]
                        changed = True
                        print(f"  ✅ {lang_code}.json labels.{key}")
            
            # Adicionar em formatting
            if "formatting" not in data:
                data["formatting"] = {}
                changed = True
            
            for key in ["context_label", "explanation_label", "timestamp_format"]:
                if key in translations:
                    if key not in data["formatting"] or data["formatting"][key] != translations[key]:
                        data["formatting"][key] = translations[key]
                        changed = True
                        print(f"  ✅ {lang_code}.json formatting.{key}")
            
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Arquivo {lang_code}.json atualizado!\n")
            else:
                print(f"⏭️ {lang_code}.json já está atualizado\n")
        
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")

if __name__ == "__main__":
    print("🔧 Adicionando traduções adicionais...\n")
    add_additional_translations()
    print("\n✨ Concluído!")
