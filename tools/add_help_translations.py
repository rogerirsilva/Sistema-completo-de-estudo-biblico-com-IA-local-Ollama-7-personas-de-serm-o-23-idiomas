import json

# Tradução para o help text
new_translations = {
    "pt": {
        "help.filter_versions": "Deixe vazio para importar todas as versões disponíveis na pasta"
    },
    "en": {
        "help.filter_versions": "Leave empty to import all available versions from the folder"
    },
    "hi": {
        "help.filter_versions": "फ़ोल्डर से सभी उपलब्ध संस्करण आयात करने के लिए खाली छोड़ें"
    },
    "ja": {
        "help.filter_versions": "フォルダから利用可能なすべてのバージョンをインポートするには空のままにします"
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
    
    print(f"✅ {lang.upper()}: {updated} help texts adicionados")

print("\n✨ Help texts traduzidos!")
