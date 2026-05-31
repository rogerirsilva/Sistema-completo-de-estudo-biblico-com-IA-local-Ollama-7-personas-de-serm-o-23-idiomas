"""
Adicionar traduções específicas do Gerador de Sermões
"""
import json
from pathlib import Path

# Novas traduções para adicionar
new_translations = {
    "pt": {
        "sermon_scope_prompt": "Selecione o escopo para geração do sermão:",
        "sermon_scope_specific_book": "📖 Livro Específico",
        "sermon_scope_old_testament": "📜 Velho Testamento",
        "sermon_scope_new_testament": "✝️ Novo Testamento",
        "sermon_scope_whole_bible": "🌍 Toda a Bíblia",
        "sermon_book_label": "Sermao Livro",
        "sermon_chapter_label": "Sermao Capitulo",
        "sermon_verse_label": "Sermao Versiculo",
        "select_multiple_books": "🔖 Selecionar múltiplos livros",
        "select_multiple_books_help": "Marque para selecionar livros específicos manualmente",
        "select_books_for_sermon": "Selecione os livros para o sermão:"
    },
    "en": {
        "sermon_scope_prompt": "Select the scope for sermon generation:",
        "sermon_scope_specific_book": "📖 Specific Book",
        "sermon_scope_old_testament": "📜 Old Testament",
        "sermon_scope_new_testament": "✝️ New Testament",
        "sermon_scope_whole_bible": "🌍 Whole Bible",
        "sermon_book_label": "Sermon Book",
        "sermon_chapter_label": "Sermon Chapter",
        "sermon_verse_label": "Sermon Verse",
        "select_multiple_books": "🔖 Select multiple books",
        "select_multiple_books_help": "Check to manually select specific books",
        "select_books_for_sermon": "Select the books for the sermon:"
    },
    "hi": {
        "sermon_scope_prompt": "उपदेश निर्माण के लिए दायरा चुनें:",
        "sermon_scope_specific_book": "📖 विशिष्ट पुस्तक",
        "sermon_scope_old_testament": "📜 पुराना नियम",
        "sermon_scope_new_testament": "✝️ नया नियम",
        "sermon_scope_whole_bible": "🌍 पूरी बाइबिल",
        "sermon_book_label": "उपदेश पुस्तक",
        "sermon_chapter_label": "उपदेश अध्याय",
        "sermon_verse_label": "उपदेश पद",
        "select_multiple_books": "🔖 कई पुस्तकें चुनें",
        "select_multiple_books_help": "विशिष्ट पुस्तकों को मैन्युअल रूप से चुनने के लिए चिह्नित करें",
        "select_books_for_sermon": "उपदेश के लिए पुस्तकें चुनें:"
    },
    "ja": {
        "sermon_scope_prompt": "説教生成の範囲を選択してください:",
        "sermon_scope_specific_book": "📖 特定の書",
        "sermon_scope_old_testament": "📜 旧約聖書",
        "sermon_scope_new_testament": "✝️ 新約聖書",
        "sermon_scope_whole_bible": "🌍 聖書全体",
        "sermon_book_label": "説教の書",
        "sermon_chapter_label": "説教の章",
        "sermon_verse_label": "説教の節",
        "select_multiple_books": "🔖 複数の書を選択",
        "select_multiple_books_help": "特定の書を手動で選択する場合はチェックしてください",
        "select_books_for_sermon": "説教の書を選択してください:"
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

print("\n🎉 Todos os arquivos de tradução foram atualizados!")
