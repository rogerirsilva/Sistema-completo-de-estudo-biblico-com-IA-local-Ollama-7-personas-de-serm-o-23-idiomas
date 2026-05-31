import json

# Traduções que faltam
new_translations = {
    "pt": {
        "labels.guided_reading": "Leitura Guiada",
        "labels.selected_colon": "Selecionado:",
        "labels.import_folder": "Pasta de importação:",
        "labels.files_found": "arquivo(s) encontrado(s)",
        "labels.filter_versions": "Filtrar versões (opcional)",
        "expanders.how_to_add_versions": "ℹ️ Como Adicionar Versões Bíblicas"
    },
    "en": {
        "labels.guided_reading": "Guided Reading",
        "labels.selected_colon": "Selected:",
        "labels.import_folder": "Import folder:",
        "labels.files_found": "file(s) found",
        "labels.filter_versions": "Filter versions (optional)",
        "expanders.how_to_add_versions": "ℹ️ How to Add Bible Versions"
    },
    "hi": {
        "labels.guided_reading": "निर्देशित पठन",
        "labels.selected_colon": "चयनित:",
        "labels.import_folder": "आयात फ़ोल्डर:",
        "labels.files_found": "फ़ाइल(ें) मिली",
        "labels.filter_versions": "संस्करण फ़िल्टर करें (वैकल्पिक)",
        "expanders.how_to_add_versions": "ℹ️ बाइबिल संस्करण कैसे जोड़ें"
    },
    "ja": {
        "labels.guided_reading": "ガイド付き読書",
        "labels.selected_colon": "選択済み:",
        "labels.import_folder": "インポートフォルダ:",
        "labels.files_found": "ファイルが見つかりました",
        "labels.filter_versions": "バージョンをフィルタ (オプション)",
        "expanders.how_to_add_versions": "ℹ️ 聖書版の追加方法"
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
    
    print(f"✅ {lang.upper()}: {updated} traduções finais adicionadas")

print("\n✨ Traduções finais concluídas!")
