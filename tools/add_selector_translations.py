import json

# Novas traduções para os seletores
new_translations = {
    "pt": {
        "labels.book_selector": "Livro",
        "labels.chapter_selector": "Capítulo",
        "labels.verse_selector": "Versículo",
        "labels.book_colon": "Livro:",
        "labels.chapter_colon": "Capítulo",
        "labels.verse_colon": "Versículo",
        "labels.selected_books_count": "livro(s) selecionado(s):",
        "labels.scope_prefix": "Escopo:",
        "labels.whole_old_testament": "Todo o Velho Testamento",
        "labels.whole_new_testament": "Todo o Novo Testamento",
        "labels.whole_bible": "Toda a Bíblia"
    },
    "en": {
        "labels.book_selector": "Book",
        "labels.chapter_selector": "Chapter",
        "labels.verse_selector": "Verse",
        "labels.book_colon": "Book:",
        "labels.chapter_colon": "Chapter",
        "labels.verse_colon": "Verse",
        "labels.selected_books_count": "book(s) selected:",
        "labels.scope_prefix": "Scope:",
        "labels.whole_old_testament": "Entire Old Testament",
        "labels.whole_new_testament": "Entire New Testament",
        "labels.whole_bible": "Entire Bible"
    },
    "hi": {
        "labels.book_selector": "पुस्तक",
        "labels.chapter_selector": "अध्याय",
        "labels.verse_selector": "पद",
        "labels.book_colon": "पुस्तक:",
        "labels.chapter_colon": "अध्याय",
        "labels.verse_colon": "पद",
        "labels.selected_books_count": "पुस्तक(ें) चयनित:",
        "labels.scope_prefix": "दायरा:",
        "labels.whole_old_testament": "संपूर्ण पुराना नियम",
        "labels.whole_new_testament": "संपूर्ण नया नियम",
        "labels.whole_bible": "संपूर्ण बाइबिल"
    },
    "ja": {
        "labels.book_selector": "書",
        "labels.chapter_selector": "章",
        "labels.verse_selector": "節",
        "labels.book_colon": "書:",
        "labels.chapter_colon": "章",
        "labels.verse_colon": "節",
        "labels.selected_books_count": "冊選択済み:",
        "labels.scope_prefix": "範囲:",
        "labels.whole_old_testament": "旧約聖書全体",
        "labels.whole_new_testament": "新約聖書全体",
        "labels.whole_bible": "聖書全体"
    }
}

# Atualizar cada arquivo de tradução
for lang in ["pt", "en", "hi", "ja"]:
    file_path = f"translations/{lang}.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
    
    # Adicionar novas traduções
    updated_count = 0
    for key, value in new_translations[lang].items():
        section, key_name = key.split(".", 1)
        if section not in translations:
            translations[section] = {}
        if key_name not in translations[section]:
            translations[section][key_name] = value
            updated_count += 1
    
    # Salvar de volta
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {lang.upper()}: {updated_count} novas traduções de seletor adicionadas")

print("\n📊 Resumo das novas traduções:")
print("- Seletores (Livro, Capítulo, Versículo)")
print("- Labels de contexto (Livro:, Capítulo, Versículo)")
print("- Contadores e escopos")
