import json
import re

# Traduções vietnamitas faltantes
VIETNAMESE_ADDITIONS = {
    # Chat scope prompt e specific verse
    "chat_scope_prompt": "Chọn phạm vi cho truy vấn Kinh Thánh:",
    "chat_scope_specific_verse": "📖 Câu Cụ Thể",
}

# Traduções turcas completas
TURKISH_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ Vaaz Üretici",
    "🧘 Devotional & Meditation": "🧘 İbadet & Meditasyon",
    
    # Scope labels
    "📖 Specific Book": "📖 Belirli Kitap",
    "📜 Old Testament": "📜 Eski Ahit",
    "✝️ New Testament": "✝️ Yeni Ahit",
    "🌍 Whole Bible": "🌍 Tüm İncil",
    
    # Additional scope
    "Entire Old Testament": "Tüm Eski Ahit",
    "Entire New Testament": "Tüm Yeni Ahit",
    "Specific Book": "Belirli Kitap",
    
    # Labels and buttons
    "Ollama Model (or type)": "Ollama Modeli (veya tür)",
    "Ollama Status": "Ollama Durumu",
    "Online": "Çevrimiçi",
    "Offline": "Çevrimdışı",
    "Guided Reading": "Rehberli Okuma",
    "Base": "Temel",
    "Base Chapter": "Temel Bölüm",
    "Verses (e.g., 1, 1-5)": "Ayetler (örn. 1, 1-5)",
    "Full chapter": "Tam bölüm",
    "Theme (optional)": "Tema (isteğe bağlı)",
    "Target audience (optional)": "Hedef kitle (isteğe bağlı)",
    "Extra notes (preacher's context)": "Ekstra notlar (vaizin bağlamı)",
    "Type your biblical question": "İncil sorunuzu yazın",
    "Search history": "Geçmişi ara",
    "Sort by": "Sırala",
    "Most recent": "En son",
    "Oldest": "En eski",
    "Book": "Kitap",
    "Search sermons": "Vaazları ara",
    "Search devotionals": "İbadetleri ara",
    "Search conversations": "Konuşmaları ara",
    "Order by": "Sırala",
    "Sermon": "Vaaz",
    "Sermon Chapter": "Vaaz Bölümü",
    "Sermon Verse": "Vaaz Ayeti",
    "Devotional": "İbadet",
    "Devotional Chapter": "İbadet Bölümü",
    "Devotional Verse": "İbadet Ayeti",
    "Chat": "Sohbet",
    "Reading page": "Okuma sayfası",
    "Multiple Books": "Birden Fazla Kitap",
    "Entire Bible": "Tüm İncil",
    "Scope": "Kapsam",
    "Number of questions": "Soru sayısı",
    "With Answers": "Cevaplarla",
    "Generation Mode": "Üretim Modu",
    "Filter by mode": "Moda göre filtrele",
    "All": "Tümü",
    "Search": "🔍 Ara",
    "Type to search...": "Aramak için yazın...",
    
    # Buttons
    "Generate Devotional": "İbadet Oluştur",
    "Clear Cache": "Önbelleği Temizle",
    "Delete": "Sil",
    "Import Versions from Folder": "Klasörden Sürümleri İçe Aktar",
    
    # Scope prefixes
    "Book:": "Kitap:",
    "Chapter": "Bölüm",
    "Verse": "Ayet",
    "book(s) selected:": "kitap seçildi:",
    "Scope:": "Kapsam:",
    "file(s) found": "dosya bulundu",
    "Filter versions (optional)": "Sürümleri filtrele (isteğe bağlı)",
    
    # Messages
    "Sermon Kitap": "Vaaz Kitabı",
    
    # Ollama messages
    "Ollama is offline. Start the local server.": "Ollama çevrimdışı. Yerel sunucuyu başlatın.",
    "Ollama is offline. Turn on the server and try again.": "Ollama çevrimdışı. Sunucuyu açın ve tekrar deneyin.",
    "Ollama is offline. Please start the server.": "Ollama çevrimdışı. Lütfen sunucuyu başlatın.",
    "Ollama is offline ({detail}). Please start the server or check your connection.": "Ollama çevrimdışı ({detail}). Lütfen sunucuyu başlatın veya bağlantınızı kontrol edin.",
    
    # Additional labels
    "Please select a valid scope.": "Lütfen geçerli bir kapsam seçin.",
    "Choose a base verse to generate the sermon:": "Vaazı oluşturmak için bir temel ayet seçin:",
    "Choose a base verse to generate devotional:": "İbadet oluşturmak için bir temel ayet seçin:",
    "Text ready to copy!": "Metin kopyalamaya hazır!",
    "No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "Henüz vaaz oluşturulmadı. İlk vaazınızı oluşturmak için 'Vaaz Üretici' sekmesini kullanın!",
    "No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first devotional!": "Henüz ibadet oluşturulmadı. İlk ibadetinizi oluşturmak için 'İbadet & Meditasyon' sekmesini kullanın!",
    "No conversations yet. Use 'Theological Chat' tab to start your first conversation!": "Henüz konuşma yok. İlk konuşmanızı başlatmak için 'Teolojik Sohbet' sekmesini kullanın!",
    "No questions generated yet. Use 'Question Generator' tab to create your first set!": "Henüz soru oluşturulmadı. İlk setinizi oluşturmak için 'Soru Üretici' sekmesini kullanın!",
    
    # Additional scope and history
    "study(ies) found": "çalışma bulundu",
    "sermons found": "vaaz bulundu",
    "devotionals found": "ibadet bulundu",
    "conversations found": "konuşma bulundu",
    "question set(s) found": "soru seti bulundu",
    "Version:": "Sürüm:",
    "Audience:": "Hedef Kitle:",
    "Model:": "Model:",
    "Reference:": "Referans:",
    "Feeling:": "His:",
    "Question:": "Soru:",
    "Answer:": "Cevap:",
    "Additional notes:": "Ek notlar:",
    "Context:": "Bağlam:",
    "Explanation:": "Açıklama:",
    
    # Prompts
    "Theme:": "Tema:",
    "Audience:": "Hedef Kitle:",
}

def translate_vietnamese(file_path):
    """Adicionar traduções vietnamitas faltantes"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Adicionar traduções faltantes na seção labels
    if 'labels' not in data:
        data['labels'] = {}
    
    count = 0
    for key, value in VIETNAMESE_ADDITIONS.items():
        if key not in data['labels']:
            data['labels'][key] = value
            count += 1
            print(f"✅ Adicionado (vi): {key} -> {value}")
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Total de {count} strings adicionadas em vietnamita")
    return count

def translate_turkish_final(file_path):
    """Traduzir turco completamente"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    count = 0
    
    for english, turkish in TURKISH_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais para regex
        english_escaped = re.escape(english)
        
        # Substituir apenas em valores JSON (após ": ")
        pattern = f'(": ")({english_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, f'\\1{turkish}\\3', content)
            matches = len(re.findall(pattern, original_content))
            count += matches
            print(f"✅ Traduzido ({matches}x): {english} -> {turkish}")
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Total de {count} strings traduzidas em turco")
    return count

if __name__ == "__main__":
    print("=" * 80)
    print("CORRIGINDO TRADUÇÕES - VIETNAMITA E TURCO")
    print("=" * 80)
    
    # Vietnamita - adicionar strings faltantes
    print("\n1. VIETNAMITA (Tiếng Việt) - Adicionando strings faltantes...")
    print("-" * 80)
    vi_count = translate_vietnamese("translations/vi.json")
    
    # Turco - tradução completa
    print("\n2. TURCO (Türkçe) - Tradução completa...")
    print("-" * 80)
    tr_count = translate_turkish_final("translations/tr.json")
    
    print("\n" + "=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    print(f"✅ Vietnamita: {vi_count} strings adicionadas")
    print(f"✅ Turco: {tr_count} strings traduzidas")
    print(f"✅ Total: {vi_count + tr_count} strings")
    print("=" * 80)
