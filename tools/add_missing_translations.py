import json

# Todas as traduções que faltam
new_translations = {
    "pt": {
        "labels.no_theme": "Sem tema",
        "labels.generic": "Genérico",
        "labels.indefinido": "Indefinido",
        "prompts.sermon_request": "Escreva um esboco completo de sermao com titulo, introducao, topicos expositivos, ilustracoes e conclusao.",
        "prompts.sermon_theme": "Tema:",
        "prompts.sermon_audience": "Publico:",
        "prompts.sermon_scope_info": "O sermão deve abranger textos de:",
        "prompts.devotional_request": "Crie uma leitura calma, uma breve reflexao e uma oracao final que conecte o sentimento selecionado ao texto biblico.",
        "prompts.devotional_feeling": "Sentimento:",
        "prompts.devotional_scope_info": "O devocional deve considerar textos de:",
        "labels.order_sort": "📅 Ordenar",
        "labels.import_placeholder_versions": "Ex: nvi,kjv,acf"
    },
    "en": {
        "labels.no_theme": "No theme",
        "labels.generic": "Generic",
        "labels.indefinido": "Undefined",
        "prompts.sermon_request": "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.",
        "prompts.sermon_theme": "Theme:",
        "prompts.sermon_audience": "Audience:",
        "prompts.sermon_scope_info": "The sermon should cover texts from:",
        "prompts.devotional_request": "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.",
        "prompts.devotional_feeling": "Feeling:",
        "prompts.devotional_scope_info": "The devotional should consider texts from:",
        "labels.order_sort": "📅 Sort",
        "labels.import_placeholder_versions": "Ex: nvi,kjv,acf"
    },
    "hi": {
        "labels.no_theme": "कोई विषय नहीं",
        "labels.generic": "सामान्य",
        "labels.indefinido": "अपरिभाषित",
        "prompts.sermon_request": "शीर्षक, परिचय, व्याख्यात्मक विषय, उदाहरण और निष्कर्ष के साथ एक पूर्ण उपदेश रूपरेखा लिखें।",
        "prompts.sermon_theme": "विषय:",
        "prompts.sermon_audience": "दर्शक:",
        "prompts.sermon_scope_info": "उपदेश में इनके पाठ शामिल होने चाहिए:",
        "prompts.devotional_request": "एक शांत पाठ, एक संक्षिप्त चिंतन और एक अंतिम प्रार्थना बनाएं जो चयनित भावना को बाइबिल पाठ से जोड़े।",
        "prompts.devotional_feeling": "भावना:",
        "prompts.devotional_scope_info": "भक्ति में इनके पाठ पर विचार करना चाहिए:",
        "labels.order_sort": "📅 क्रमबद्ध करें",
        "labels.import_placeholder_versions": "उदाहरण: nvi,kjv,acf"
    },
    "ja": {
        "labels.no_theme": "テーマなし",
        "labels.generic": "一般的",
        "labels.indefinido": "未定義",
        "prompts.sermon_request": "タイトル、序論、解説的トピック、例示、結論を含む完全な説教の概要を書いてください。",
        "prompts.sermon_theme": "テーマ:",
        "prompts.sermon_audience": "対象者:",
        "prompts.sermon_scope_info": "説教には次のテキストを含める必要があります:",
        "prompts.devotional_request": "穏やかな読み物、簡単な考察、選択した感情を聖書のテキストに結び付ける最後の祈りを作成してください。",
        "prompts.devotional_feeling": "感情:",
        "prompts.devotional_scope_info": "黙想には次のテキストを考慮する必要があります:",
        "labels.order_sort": "📅 並べ替え",
        "labels.import_placeholder_versions": "例: nvi,kjv,acf"
    }
}

# Atualizar cada arquivo
for lang in ["pt", "en", "hi", "ja"]:
    file_path = f"translations/{lang}.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
    
    updated = 0
    for key, value in new_translations[lang].items():
        section, key_name = key.split(".", 1)
        if section not in translations:
            translations[section] = {}
        if key_name not in translations[section]:
            translations[section][key_name] = value
            updated += 1
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {lang.upper()}: {updated} novas traduções adicionadas")

print("\n✨ Traduções adicionadas com sucesso!")
