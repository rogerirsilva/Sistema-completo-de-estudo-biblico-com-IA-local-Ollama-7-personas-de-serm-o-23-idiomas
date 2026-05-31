"""
Script para testar o carregamento de Bíblias em Hindi e Japonês
"""
import json
from pathlib import Path
from book_names_mapping import get_book_name

# Testar Hindi
print("=" * 80)
print("TESTANDO HINDI (हिन्दी)")
print("=" * 80)

hi_file = Path("Dados_Json/hi/irv.json")
if hi_file.exists():
    print(f"✅ Arquivo encontrado: {hi_file}")
    with open(hi_file, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()
        data = json.loads(content)
    
    if isinstance(data, list):
        print(f"📚 Total de livros no arquivo: {len(data)}")
        print("\nPrimeiros 5 livros:")
        for idx, book in enumerate(data[:5]):
            abbrev = book.get("abbrev", "?")
            json_name = book.get("name", "Sem nome")
            mapped_name = get_book_name(abbrev, "hi", fallback=json_name)
            chapters = len(book.get("chapters", []))
            print(f"  {idx+1}. Abbrev: '{abbrev}' | JSON: '{json_name}' | Mapeado: '{mapped_name}' | Capítulos: {chapters}")
else:
    print(f"❌ Arquivo não encontrado: {hi_file}")

print("\n" + "=" * 80)
print("TESTANDO JAPONÊS (日本語)")
print("=" * 80)

ja_file = Path("Dados_Json/ja/kougo.json")
if ja_file.exists():
    print(f"✅ Arquivo encontrado: {ja_file}")
    with open(ja_file, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()
        data = json.loads(content)
    
    if isinstance(data, list):
        print(f"📚 Total de livros no arquivo: {len(data)}")
        print("\nPrimeiros 5 livros:")
        for idx, book in enumerate(data[:5]):
            abbrev = book.get("abbrev", "?")
            json_name = book.get("name", "Sem nome")
            mapped_name = get_book_name(abbrev, "ja", fallback=json_name)
            chapters = len(book.get("chapters", []))
            print(f"  {idx+1}. Abbrev: '{abbrev}' | JSON: '{json_name}' | Mapeado: '{mapped_name}' | Capítulos: {chapters}")
else:
    print(f"❌ Arquivo não encontrado: {ja_file}")

print("\n" + "=" * 80)
print("✅ TESTE COMPLETO!")
print("=" * 80)
