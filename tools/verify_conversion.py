"""
Verificar o conteúdo dos arquivos JSON convertidos
"""
import json

def check_bible_json(filepath, lang_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"📖 {lang_name}")
    print(f"{'='*60}")
    print(f"Total de livros: {len(data)}")
    
    # Primeiros 5 livros
    print(f"\n✅ Primeiros 5 livros:")
    for i, book in enumerate(data[:5], 1):
        print(f"   {i}. {book['name']} ({book['abbrev']}) - {len(book['chapters'])} capítulos")
    
    # Últimos 3 livros
    print(f"\n✅ Últimos 3 livros:")
    for i, book in enumerate(data[-3:], len(data)-2):
        print(f"   {i}. {book['name']} ({book['abbrev']}) - {len(book['chapters'])} capítulos")
    
    # Exemplo de conteúdo
    print(f"\n📜 Exemplo - {data[0]['name']} 1:1")
    print(f"   {data[0]['chapters'][0][0]}")

# Verificar Hindi
check_bible_json('Dados_Json/hi/irv.json', 'Hindi (हिन्दी) - Indian Revised Version')

# Verificar Japonês
check_bible_json('Dados_Json/ja/kougo.json', 'Japonês (日本語) - Kougo-yaku')

print(f"\n{'='*60}")
print("🎉 Todos os dados foram convertidos com sucesso!")
print(f"{'='*60}\n")
