import json

# Traduções para captions e outros elementos
new_translations = {
    "pt": {
        "captions.default_pattern": "✅ Padrão:",
        "captions.studies_found": "📊 {count} estudo(s) encontrado(s)",
        "captions.sermons_found": "📄 {count} sermões encontrados",
        "captions.devotionals_found": "📄 {count} devocionais encontrados",
        "captions.conversations_found": "📄 {count} conversas encontradas",
        "captions.version": "📚 Versão:",
        "captions.audience": "👥 Público:",
        "captions.model": "🤖 Modelo:",
        "captions.reference": "📝 Referência:",
        "captions.feeling": "❤️ Sentimento:",
        "captions.folder_instruction": "Crie a pasta manualmente ou a aplicação criará automaticamente ao importar."
    },
    "en": {
        "captions.default_pattern": "✅ Default:",
        "captions.studies_found": "📊 {count} study(ies) found",
        "captions.sermons_found": "📄 {count} sermons found",
        "captions.devotionals_found": "📄 {count} devotionals found",
        "captions.conversations_found": "📄 {count} conversations found",
        "captions.version": "📚 Version:",
        "captions.audience": "👥 Audience:",
        "captions.model": "🤖 Model:",
        "captions.reference": "📝 Reference:",
        "captions.feeling": "❤️ Feeling:",
        "captions.folder_instruction": "Create the folder manually or the application will create it automatically when importing."
    },
    "hi": {
        "captions.default_pattern": "✅ डिफ़ॉल्ट:",
        "captions.studies_found": "📊 {count} अध्ययन मिला",
        "captions.sermons_found": "📄 {count} उपदेश मिले",
        "captions.devotionals_found": "📄 {count} भक्ति मिली",
        "captions.conversations_found": "📄 {count} बातचीत मिली",
        "captions.version": "📚 संस्करण:",
        "captions.audience": "👥 दर्शक:",
        "captions.model": "🤖 मॉडल:",
        "captions.reference": "📝 संदर्भ:",
        "captions.feeling": "❤️ भावना:",
        "captions.folder_instruction": "फ़ोल्डर मैन्युअल रूप से बनाएं या आयात करते समय एप्लिकेशन स्वचालित रूप से इसे बना देगा।"
    },
    "ja": {
        "captions.default_pattern": "✅ デフォルト:",
        "captions.studies_found": "📊 {count}件の学習が見つかりました",
        "captions.sermons_found": "📄 {count}件の説教が見つかりました",
        "captions.devotionals_found": "📄 {count}件の黙想が見つかりました",
        "captions.conversations_found": "📄 {count}件の会話が見つかりました",
        "captions.version": "📚 版:",
        "captions.audience": "👥 対象者:",
        "captions.model": "🤖 モデル:",
        "captions.reference": "📝 参照:",
        "captions.feeling": "❤️ 感情:",
        "captions.folder_instruction": "フォルダを手動で作成するか、インポート時にアプリケーションが自動的に作成します。"
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
    
    print(f"✅ {lang.upper()}: {updated} captions adicionadas")

print("\n✨ Captions traduzidas com sucesso!")
