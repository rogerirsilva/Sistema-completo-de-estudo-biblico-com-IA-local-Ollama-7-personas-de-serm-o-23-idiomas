import json

# Traduções para mensagens de erro e avisos
new_translations = {
    "pt": {
        "errors.load_bible_data": "⚠️ Erro ao carregar bible_data.json: {error}. Usando dados vazios.",
        "errors.unexpected_error": "❌ Erro inesperado ao carregar dados: {error}",
        "errors.load_json_file": "⚠️ Erro ao carregar {filename}: {error}",
        "warnings.no_json_files": "⚠️ Nenhum arquivo JSON encontrado em `Dados_Json/{lang}/`",
        "warnings.folder_not_exist": "❌ Pasta `Dados_Json/{lang}/` não existe.",
        "warnings.no_versions_found": "⚠️ Nenhuma versão encontrada em `Dados_Json/{lang}/`.",
        "warnings.folder_not_found": "❌ Pasta `Dados_Json/{lang}/` não encontrada."
    },
    "en": {
        "errors.load_bible_data": "⚠️ Error loading bible_data.json: {error}. Using empty data.",
        "errors.unexpected_error": "❌ Unexpected error loading data: {error}",
        "errors.load_json_file": "⚠️ Error loading {filename}: {error}",
        "warnings.no_json_files": "⚠️ No JSON files found in `Dados_Json/{lang}/`",
        "warnings.folder_not_exist": "❌ Folder `Dados_Json/{lang}/` does not exist.",
        "warnings.no_versions_found": "⚠️ No versions found in `Dados_Json/{lang}/`.",
        "warnings.folder_not_found": "❌ Folder `Dados_Json/{lang}/` not found."
    },
    "hi": {
        "errors.load_bible_data": "⚠️ bible_data.json लोड करने में त्रुटि: {error}. खाली डेटा का उपयोग कर रहे हैं।",
        "errors.unexpected_error": "❌ डेटा लोड करते समय अप्रत्याशित त्रुटि: {error}",
        "errors.load_json_file": "⚠️ {filename} लोड करने में त्रुटि: {error}",
        "warnings.no_json_files": "⚠️ `Dados_Json/{lang}/` में कोई JSON फ़ाइल नहीं मिली",
        "warnings.folder_not_exist": "❌ फ़ोल्डर `Dados_Json/{lang}/` मौजूद नहीं है।",
        "warnings.no_versions_found": "⚠️ `Dados_Json/{lang}/` में कोई संस्करण नहीं मिला।",
        "warnings.folder_not_found": "❌ फ़ोल्डर `Dados_Json/{lang}/` नहीं मिला।"
    },
    "ja": {
        "errors.load_bible_data": "⚠️ bible_data.jsonの読み込みエラー: {error}。空のデータを使用しています。",
        "errors.unexpected_error": "❌ データ読み込み中の予期しないエラー: {error}",
        "errors.load_json_file": "⚠️ {filename}の読み込みエラー: {error}",
        "warnings.no_json_files": "⚠️ `Dados_Json/{lang}/`にJSONファイルが見つかりません",
        "warnings.folder_not_exist": "❌ フォルダ`Dados_Json/{lang}/`は存在しません。",
        "warnings.no_versions_found": "⚠️ `Dados_Json/{lang}/`にバージョンが見つかりません。",
        "warnings.folder_not_found": "❌ フォルダ`Dados_Json/{lang}/`が見つかりません。"
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
    
    print(f"✅ {lang.upper()}: {updated} mensagens de erro/aviso adicionadas")

print("\n✨ Mensagens de erro e avisos traduzidos!")
