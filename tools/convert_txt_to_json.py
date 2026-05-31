"""
Converte arquivos TXT de Bíblia (formato BibleSuperSearch) para JSON
"""
import json
import re
from pathlib import Path
from collections import defaultdict

def parse_bible_txt(txt_file):
    """
    Formato do TXT:
    उत्पत्ति 1:1 ¶ आदि में परमेश्‍वर ने...
    Livro Capítulo:Versículo Texto
    """
    books = defaultdict(lambda: {"name": "", "abbrev": "", "chapters": defaultdict(list)})
    
    # Mapeamento de nomes de livros para abreviações
    book_mappings = {
        # Hindi
        "उत्पत्ति": "gn",
        "निर्गमन": "ex",
        "लैव्यवस्था": "lv",
        "गिनती": "nm",
        "व्यवस्थाविवरण": "dt",
        "यहोशू": "js",
        "न्यायियों": "jz",
        "रूत": "rt",
        "1 शमूएल": "1sm",
        "2 शमूएल": "2sm",
        "1 राजा": "1rs",
        "2 राजा": "2rs",
        "1 इतिहास": "1cr",
        "2 इतिहास": "2cr",
        "एज्रा": "ed",
        "नहेम्याह": "ne",
        "एस्तेर": "et",
        "अय्यूब": "job",
        "भजन संहिता": "sl",
        "नीतिवचन": "pv",
        "सभोपदेशक": "ec",
        "श्रेष्ठगीत": "ct",
        "यशायाह": "is",
        "यिर्मयाह": "jr",
        "विलापगीत": "lm",
        "यहेजकेल": "ez",
        "दानिय्येल": "dn",
        "होशे": "os",
        "योएल": "jl",
        "आमोस": "am",
        "ओबद्याह": "ob",
        "योना": "jn",
        "मीका": "mq",
        "नहूम": "na",
        "हबक्कूक": "hc",
        "सपन्याह": "sf",
        "हाग्गै": "ag",
        "जकर्याह": "zc",
        "मलाकी": "ml",
        "मत्ती": "mt",
        "मरकुस": "mc",
        "लूका": "lc",
        "यूहन्ना": "jo",
        "प्रेरितों के काम": "at",
        "रोमियों": "rm",
        "1 कुरिन्थियों": "1co",
        "2 कुरिन्थियों": "2co",
        "गलातियों": "gl",
        "इफिसियों": "ef",
        "फिलिप्पियों": "fp",
        "कुलुस्सियों": "cl",
        "1 थिस्सलुनीकियों": "1ts",
        "2 थिस्सलुनीकियों": "2ts",
        "1 तीमुथियुस": "1tm",
        "2 तीमुथियुस": "2tm",
        "तीतुस": "tt",
        "फिलेमोन": "fm",
        "इब्रानियों": "hb",
        "याकूब": "tg",
        "1 पतरस": "1pe",
        "2 पतरस": "2pe",
        "1 यूहन्ना": "1jo",
        "2 यूहन्ना": "2jo",
        "3 यूहन्ना": "3jo",
        "यहूदा": "jd",
        "प्रकाशितवाक्य": "ap",
        
        # Japonês
        "創世記": "gn",
        "出エジプト記": "ex",
        "レビ記": "lv",
        "民数記": "nm",
        "申命記": "dt",
        "ヨシュア記": "js",
        "士師記": "jz",
        "ルツ記": "rt",
        "サムエル記上": "1sm",
        "サムエル記下": "2sm",
        "列王紀上": "1rs",
        "列王紀下": "2rs",
        "歴代志上": "1cr",
        "歴代志下": "2cr",
        "エズラ記": "ed",
        "ネヘミヤ記": "ne",
        "エステル記": "et",
        "ヨブ記": "job",
        "詩篇": "sl",
        "箴言": "pv",
        "伝道の書": "ec",
        "雅歌": "ct",
        "イザヤ書": "is",
        "エレミヤ書": "jr",
        "哀歌": "lm",
        "エゼキエル書": "ez",
        "ダニエル書": "dn",
        "ホセア書": "os",
        "ヨエル書": "jl",
        "アモス書": "am",
        "オバデヤ書": "ob",
        "ヨナ書": "jn",
        "ミカ書": "mq",
        "ナホム書": "na",
        "ハバクク書": "hc",
        "ゼパニヤ書": "sf",
        "ハガイ書": "ag",
        "ゼカリヤ書": "zc",
        "マラキ書": "ml",
        "マタイによる福音書": "mt",
        "マルコによる福音書": "mc",
        "ルカによる福音書": "lc",
        "ヨハネによる福音書": "jo",
        "使徒行伝": "at",
        "ローマ人への手紙": "rm",
        "コリント人への第一の手紙": "1co",
        "コリント人への第二の手紙": "2co",
        "ガラテヤ人への手紙": "gl",
        "エペソ人への手紙": "ef",
        "ピリピ人への手紙": "fp",
        "コロサイ人への手紙": "cl",
        "テサロニケ人への第一の手紙": "1ts",
        "テサロニケ人への第二の手紙": "2ts",
        "テモテへの第一の手紙": "1tm",
        "テモテへの第二の手紙": "2tm",
        "テトスへの手紙": "tt",
        "ピレモンへの手紙": "fm",
        "ヘブル人への手紙": "hb",
        "ヤコブの手紙": "tg",
        "ペテロの第一の手紙": "1pe",
        "ペテロの第二の手紙": "2pe",
        "ヨハネの第一の手紙": "1jo",
        "ヨハネの第二の手紙": "2jo",
        "ヨハネの第三の手紙": "3jo",
        "ユダの手紙": "jd",
        "ヨハネの黙示録": "ap",
    }
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('This Bible') or line.startswith('Indian Revised') or line.startswith('Kougo-yaku'):
                continue
            
            # Formato: Livro Capítulo:Versículo Texto
            match = re.match(r'^(.+?)\s+(\d+):(\d+)\s+¶?\s*(.+)$', line)
            if match:
                book_name = match.group(1).strip()
                chapter_num = int(match.group(2))
                verse_num = int(match.group(3))
                verse_text = match.group(4).strip()
                
                # Obter abreviação
                abbrev = book_mappings.get(book_name, None)
                if not abbrev:
                    # Tentar sem números (ex: "1 शमूएल" -> "शमूएल")
                    book_base = re.sub(r'^\d+\s+', '', book_name)
                    for key, val in book_mappings.items():
                        if book_base in key or key in book_base:
                            abbrev = val
                            break
                
                if abbrev:
                    if not books[abbrev]["name"]:
                        books[abbrev]["name"] = book_name
                        books[abbrev]["abbrev"] = abbrev
                    
                    # Garantir que o capítulo existe
                    while len(books[abbrev]["chapters"][chapter_num]) < verse_num:
                        books[abbrev]["chapters"][chapter_num].append("")
                    
                    # Adicionar o versículo (índice zero-based)
                    if verse_num <= len(books[abbrev]["chapters"][chapter_num]):
                        books[abbrev]["chapters"][chapter_num][verse_num - 1] = verse_text
                    else:
                        books[abbrev]["chapters"][chapter_num].append(verse_text)
    
    # Converter para formato JSON final
    result = []
    
    # Ordem correta dos livros da Bíblia
    book_order = [
        "gn", "ex", "lv", "nm", "dt", "js", "jz", "rt", "1sm", "2sm",
        "1rs", "2rs", "1cr", "2cr", "ed", "ne", "et", "job", "sl", "pv",
        "ec", "ct", "is", "jr", "lm", "ez", "dn", "os", "jl", "am",
        "ob", "jn", "mq", "na", "hc", "sf", "ag", "zc", "ml",
        "mt", "mc", "lc", "jo", "at", "rm", "1co", "2co", "gl", "ef",
        "fp", "cl", "1ts", "2ts", "1tm", "2tm", "tt", "fm", "hb", "tg",
        "1pe", "2pe", "1jo", "2jo", "3jo", "jd", "ap"
    ]
    
    for abbrev in book_order:
        if abbrev in books:
            book = books[abbrev]
            chapters = []
            for ch_num in sorted(book["chapters"].keys()):
                chapters.append(book["chapters"][ch_num])
            
            result.append({
                "abbrev": abbrev,
                "name": book["name"],
                "chapters": chapters
            })
    
    return result

def main():
    print("🔄 Convertendo Bíblias TXT para JSON...\n")
    
    # Criar diretórios de destino
    Path("Dados_Json/hi").mkdir(parents=True, exist_ok=True)
    Path("Dados_Json/ja").mkdir(parents=True, exist_ok=True)
    
    # Converter Hindi
    print("📖 Processando Hindi (IRV)...")
    hindi_data = parse_bible_txt("temp_hindi/irv.txt")
    with open("Dados_Json/hi/irv.json", "w", encoding="utf-8") as f:
        json.dump(hindi_data, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {len(hindi_data)} livros salvos em Dados_Json/hi/irv.json")
    
    # Converter Japonês
    print("📖 Processando Japonês (Kougo)...")
    japanese_data = parse_bible_txt("temp_japon/kougo.txt")
    with open("Dados_Json/ja/kougo.json", "w", encoding="utf-8") as f:
        json.dump(japanese_data, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {len(japanese_data)} livros salvos em Dados_Json/ja/kougo.json")
    
    print("\n🎉 Conversão concluída com sucesso!")
    print("\nAgora você pode:")
    print("1. Executar: streamlit run app.py")
    print("2. Selecionar Hindi (हिन्दी) ou Japonês (日本語)")
    print("3. Ver todos os livros da Bíblia em seus idiomas nativos!")

if __name__ == "__main__":
    main()
