#!/usr/bin/env python3
"""Script para testar carregamento das Bíblias."""

import json
from pathlib import Path

def test_load_bible():
    """Testa carregamento e conversão do formato."""
    lang_dir = Path("Dados_Json") / "pt"
    
    print(f"📁 Diretório: {lang_dir}")
    print(f"✅ Existe: {lang_dir.exists()}\n")
    
    if not lang_dir.exists():
        print("❌ Diretório não encontrado!")
        return
    
    # Listar arquivos JSON
    json_files = list(lang_dir.glob("*.json"))
    print(f"📄 Encontrados {len(json_files)} arquivos JSON:\n")
    
    for json_file in json_files:
        if json_file.name.lower() == "readme.json":
            continue
        
        print(f"   • {json_file.name} ({json_file.stat().st_size / 1024:.0f} KB)")
        
        try:
            # Testar leitura
            with open(json_file, "r", encoding="utf-8-sig") as f:
                content = f.read().strip()
            
            data = json.loads(content)
            
            # Verificar formato
            if isinstance(data, list):
                print(f"     ✅ Formato: Array com {len(data)} livros")
                if data:
                    first_book = data[0]
                    print(f"     📖 Primeiro livro: {first_book.get('name', 'N/A')}")
                    print(f"     📑 Capítulos no primeiro livro: {len(first_book.get('chapters', []))}")
            elif isinstance(data, dict):
                print(f"     ✅ Formato: Dicionário com chaves: {list(data.keys())}")
            
            print()
            
        except Exception as e:
            print(f"     ❌ Erro: {e}\n")
    
    print("\n🔄 Testando conversão para estrutura esperada...")
    
    # Simular conversão
    bible_data = {"versions": {}}
    
    for json_file in json_files:
        if json_file.name.lower() == "readme.json":
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8-sig") as f:
                content = f.read().strip()
            
            data = json.loads(content)
            version_name = json_file.stem.upper()
            
            if isinstance(data, list):
                books = {}
                for idx, book in enumerate(data):
                    book_name = book.get("name", book.get("abbrev", f"Book{idx}"))
                    chapters_dict = {}
                    
                    for ch_idx, chapter in enumerate(book.get("chapters", [])):
                        ch_num = str(ch_idx + 1)
                        chapters_dict[ch_num] = chapter
                    
                    books[book_name] = {
                        "abbrev": book.get("abbrev", ""),
                        "order": idx + 1,
                        "chapters": chapters_dict
                    }
                
                bible_data["versions"][version_name] = {
                    "books": books
                }
                
                print(f"✅ {version_name}: {len(books)} livros convertidos")
                
        except Exception as e:
            print(f"❌ {json_file.name}: {e}")
    
    print(f"\n📊 Resultado final:")
    print(f"   Versões disponíveis: {list(bible_data.get('versions', {}).keys())}")
    
    for version, ver_data in bible_data.get("versions", {}).items():
        books_count = len(ver_data.get("books", {}))
        print(f"   • {version}: {books_count} livros")

if __name__ == "__main__":
    test_load_bible()
