"""
Script para testar as traduções de nomes de livros bíblicos.
"""

from book_names_mapping import get_book_name

# Lista de idiomas para testar
languages = {
    "pt": "Português",
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "ru": "Русский",
    "zh": "中文",
    "ja": "日本語",
    "ar": "العربية",
    "el": "Ελληνικά",
    "eo": "Esperanto",
    "fi": "Suomi",
    "ko": "한국어",
    "ro": "Română",
    "vi": "Tiếng Việt",
    "hi": "हिन्दी",
    "id": "Bahasa Indonesia",
    "pl": "Polski",
    "fa": "فارسی",
    "sw": "Kiswahili",
    "th": "ไทย",
    "tr": "Türkçe"
}

# Livros para testar (alguns do VT e NT)
test_books = ["gn", "ex", "mt", "jo", "ap"]

print("=" * 80)
print("TESTE DE TRADUÇÕES DE NOMES DE LIVROS BÍBLICOS")
print("=" * 80)
print()

for abbrev in test_books:
    print(f"\n📖 LIVRO: {abbrev.upper()}")
    print("-" * 80)
    
    for lang_code, lang_name in languages.items():
        translated_name = get_book_name(abbrev, lang_code)
        print(f"{lang_code:4s} ({lang_name:20s}): {translated_name}")

print("\n" + "=" * 80)
print("✅ TESTE COMPLETO!")
print("=" * 80)
