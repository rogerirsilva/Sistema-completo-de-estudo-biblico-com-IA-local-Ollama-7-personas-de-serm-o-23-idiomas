"""
Adicionar traduções específicas do Devocional
"""
import json
from pathlib import Path

# Novas traduções para adicionar
new_translations = {
    "pt": {
        "devotional_scope_prompt": "Selecione o escopo para geração do devocional:",
        "devotional_book_label": "Devocional Livro",
        "select_books_for_devotional": "Selecione os livros para o devocional:"
    },
    "en": {
        "devotional_scope_prompt": "Select the scope for devotional generation:",
        "devotional_book_label": "Devotional Book",
        "select_books_for_devotional": "Select the books for the devotional:"
    },
    "hi": {
        "devotional_scope_prompt": "भक्ति निर्माण के लिए दायरा चुनें:",
        "devotional_book_label": "भक्ति पुस्तक",
        "select_books_for_devotional": "भक्ति के लिए पुस्तकें चुनें:"
    },
    "ja": {
        "devotional_scope_prompt": "黙想生成の範囲を選択してください:",
        "devotional_book_label": "黙想の書",
        "select_books_for_devotional": "黙想の書を選択してください:"
    }
}

# Atualizar cada arquivo de tradução
translations_dir = Path("translations")

for lang_code, new_keys in new_translations.items():
    filepath = translations_dir / f"{lang_code}.json"
    
    # Carregar arquivo existente
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Adicionar novas chaves na seção labels
    if "labels" not in data:
        data["labels"] = {}
    
    for key, value in new_keys.items():
        data["labels"][key] = value
    
    # Salvar arquivo atualizado
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Atualizado {lang_code}.json - {len(new_keys)} novas traduções")

print("\n🎉 Traduções de Devocional adicionadas!")
