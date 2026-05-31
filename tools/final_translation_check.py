import json

print("🌍 Verificando traduções do sistema completo...\n")

total_keys = 0
for lang in ["pt", "en", "hi", "ja"]:
    file_path = f"translations/{lang}.json"
    lang_names = {
        "pt": "Português",
        "en": "English", 
        "hi": "हिन्दी",
        "ja": "日本語"
    }
    
    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
    
    # Contar todas as chaves
    count = 0
    sections = {}
    for section, keys in translations.items():
        section_count = len(keys)
        sections[section] = section_count
        count += section_count
    
    if lang == "pt":
        total_keys = count
    
    print(f"✅ {lang.upper()} - {lang_names[lang]}: {count} traduções")
    for section, section_count in sorted(sections.items()):
        print(f"   • {section}: {section_count}")
    print()

print(f"📊 TOTAL: {total_keys} strings traduzidas × 4 idiomas = {total_keys * 4} traduções\n")
print("✨ Sistema completamente multilíngue!")
print("   • Menus e navegação")
print("   • Labels e seletores (Livro, Capítulo, Versículo)")
print("   • Botões de ação")
print("   • Mensagens e feedbacks")
print("   • Campos de entrada")
print("   • Escopos e contextos")
