"""
Conversor de Bíblias TXT (BibleSuperSearch format) para JSON
Formato esperado pelo sistema
"""
import json
import re
from pathlib import Path

# Mapeamento de nomes de livros para abreviações
BOOK_MAPPING = {
    # Antigo Testamento
    "Genesis": {"abbrev": "gn", "name": "Gênesis"},
    "Exodus": {"abbrev": "ex", "name": "Êxodo"},
    "Leviticus": {"abbrev": "lv", "name": "Levítico"},
    "Numbers": {"abbrev": "nm", "name": "Números"},
    "Deuteronomy": {"abbrev": "dt", "name": "Deuteronômio"},
    "Joshua": {"abbrev": "js", "name": "Josué"},
    "Judges": {"abbrev": "jz", "name": "Juízes"},
    "Ruth": {"abbrev": "rt", "name": "Rute"},
    "1 Samuel": {"abbrev": "1sm", "name": "1 Samuel"},
    "2 Samuel": {"abbrev": "2sm", "name": "2 Samuel"},
    "1 Kings": {"abbrev": "1rs", "name": "1 Reis"},
    "2 Kings": {"abbrev": "2rs", "name": "2 Reis"},
    "1 Chronicles": {"abbrev": "1cr", "name": "1 Crônicas"},
    "2 Chronicles": {"abbrev": "2cr", "name": "2 Crônicas"},
    "Ezra": {"abbrev": "ed", "name": "Esdras"},
    "Nehemiah": {"abbrev": "ne", "name": "Neemias"},
    "Esther": {"abbrev": "et", "name": "Ester"},
    "Job": {"abbrev": "job", "name": "Jó"},
    "Psalms": {"abbrev": "sl", "name": "Salmos"},
    "Proverbs": {"abbrev": "pv", "name": "Provérbios"},
    "Ecclesiastes": {"abbrev": "ec", "name": "Eclesiastes"},
    "Song of Solomon": {"abbrev": "ct", "name": "Cânticos"},
    "Isaiah": {"abbrev": "is", "name": "Isaías"},
    "Jeremiah": {"abbrev": "jr", "name": "Jeremias"},
    "Lamentations": {"abbrev": "lm", "name": "Lamentações"},
    "Ezekiel": {"abbrev": "ez", "name": "Ezequiel"},
    "Daniel": {"abbrev": "dn", "name": "Daniel"},
    "Hosea": {"abbrev": "os", "name": "Oséias"},
    "Joel": {"abbrev": "jl", "name": "Joel"},
    "Amos": {"abbrev": "am", "name": "Amós"},
    "Obadiah": {"abbrev": "ob", "name": "Obadias"},
    "Jonah": {"abbrev": "jn", "name": "Jonas"},
    "Micah": {"abbrev": "mq", "name": "Miquéias"},
    "Nahum": {"abbrev": "na", "name": "Naum"},
    "Habakkuk": {"abbrev": "hc", "name": "Habacuque"},
    "Zephaniah": {"abbrev": "sf", "name": "Sofonias"},
    "Haggai": {"abbrev": "ag", "name": "Ageu"},
    "Zechariah": {"abbrev": "zc", "name": "Zacarias"},
    "Malachi": {"abbrev": "ml", "name": "Malaquias"},
    # Novo Testamento
    "Matthew": {"abbrev": "mt", "name": "Mateus"},
    "Mark": {"abbrev": "mc", "name": "Marcos"},
    "Luke": {"abbrev": "lc", "name": "Lucas"},
    "John": {"abbrev": "jo", "name": "João"},
    "Acts": {"abbrev": "at", "name": "Atos"},
    "Romans": {"abbrev": "rm", "name": "Romanos"},
    "1 Corinthians": {"abbrev": "1co", "name": "1 Coríntios"},
    "2 Corinthians": {"abbrev": "2co", "name": "2 Coríntios"},
    "Galatians": {"abbrev": "gl", "name": "Gálatas"},
    "Ephesians": {"abbrev": "ef", "name": "Efésios"},
    "Philippians": {"abbrev": "fp", "name": "Filipenses"},
    "Colossians": {"abbrev": "cl", "name": "Colossenses"},
    "1 Thessalonians": {"abbrev": "1ts", "name": "1 Tessalonicenses"},
    "2 Thessalonians": {"abbrev": "2ts", "name": "2 Tessalonicenses"},
    "1 Timothy": {"abbrev": "1tm", "name": "1 Timóteo"},
    "2 Timothy": {"abbrev": "2tm", "name": "2 Timóteo"},
    "Titus": {"abbrev": "tt", "name": "Tito"},
    "Philemon": {"abbrev": "fm", "name": "Filemom"},
    "Hebrews": {"abbrev": "hb", "name": "Hebreus"},
    "James": {"abbrev": "tg", "name": "Tiago"},
    "1 Peter": {"abbrev": "1pe", "name": "1 Pedro"},
    "2 Peter": {"abbrev": "2pe", "name": "2 Pedro"},
    "1 John": {"abbrev": "1jo", "name": "1 João"},
    "2 John": {"abbrev": "2jo", "name": "2 João"},
    "3 John": {"abbrev": "3jo", "name": "3 João"},
    "Jude": {"abbrev": "jd", "name": "Judas"},
    "Revelation": {"abbrev": "ap", "name": "Apocalipse"}
}


def parse_txt_bible(txt_file):
    """
    Parse arquivo TXT da BibleSuperSearch
    Formato: Book Chapter:Verse Text
    """
    bible_data = []
    current_book = None
    current_book_data = None
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse formato: "Book Chapter:Verse Text"
            # Exemplo: "Genesis 1:1 In the beginning..."
            match = re.match(r'^([A-Za-z\s0-9]+)\s+(\d+):(\d+)\s+(.+)$', line)
            if not match:
                continue
            
            book_name = match.group(1).strip()
            chapter_num = int(match.group(2))
            verse_num = int(match.group(3))
            verse_text = match.group(4).strip()
            
            # Verificar se mudou de livro
            if current_book != book_name:
                if current_book_data:
                    bible_data.append(current_book_data)
                
                # Buscar mapeamento do livro
                book_info = BOOK_MAPPING.get(book_name, {"abbrev": book_name.lower().replace(" ", ""), "name": book_name})
                
                current_book = book_name
                current_book_data = {
                    "abbrev": book_info["abbrev"],
                    "book": book_info["name"],
                    "chapters": []
                }
            
            # Garantir que temos capítulos suficientes
            while len(current_book_data["chapters"]) < chapter_num:
                current_book_data["chapters"].append([])
            
            # Adicionar versículo ao capítulo (índice chapter_num-1)
            chapter = current_book_data["chapters"][chapter_num - 1]
            
            # Garantir que temos versículos suficientes
            while len(chapter) < verse_num:
                chapter.append("")
            
            # Adicionar versículo (índice verse_num-1)
            chapter[verse_num - 1] = verse_text
    
    # Adicionar último livro
    if current_book_data:
        bible_data.append(current_book_data)
    
    return bible_data


def convert_bible(txt_path, output_path, lang_code):
    """
    Converte arquivo TXT para JSON
    """
    print(f"Convertendo {txt_path.name}...")
    
    try:
        bible_data = parse_txt_bible(txt_path)
        
        # Salvar JSON
        output_dir = Path("Dados_Json") / lang_code
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / output_path
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bible_data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ Salvo em: {output_file}")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


if __name__ == "__main__":
    # Diretório fonte
    source_dir = Path(r"C:\Users\Rogerio\Documents\Projetos\Biblia\biblesupersearch_client_6.1.1\assets\extras\text_bibles")
    
    # Mapeamento de arquivos para converter
    conversions = [
        ("diodati.txt", "diodati.json", "it"),        # Italiano
        ("kougo.txt", "kougo.json", "ja"),            # Japonês
        ("indo_tm.txt", "indo_tm.json", "id"),        # Indonésio (novo idioma!)
        ("irv.txt", "irv.json", "hi"),                # Hindi (novo idioma!)
        ("pol_ubg.txt", "pol_ubg.json", "pl"),        # Polonês (novo idioma!)
        ("opt.txt", "opt.json", "fa"),                # Persa (novo idioma!)
        ("swahili.txt", "swahili.json", "sw"),        # Swahili (novo idioma!)
        ("thaikjv.txt", "thaikjv.json", "th"),        # Tailandês (novo idioma!)
        ("turkish.txt", "turkish.json", "tr"),        # Turco (novo idioma!)
    ]
    
    print("🔄 Iniciando conversão de Bíblias TXT para JSON...\n")
    
    success_count = 0
    for txt_file, json_file, lang in conversions:
        txt_path = source_dir / txt_file
        if txt_path.exists():
            if convert_bible(txt_path, json_file, lang):
                success_count += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {txt_file}")
    
    print(f"\n✅ Conversão concluída: {success_count}/{len(conversions)} arquivos convertidos com sucesso!")
