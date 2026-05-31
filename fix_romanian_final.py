import json
import re

# Traduções romenas completas
ROMANIAN_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ Generator de Predici",
    "📋 Sermon History": "📋 Istoric Predici",
    "🧘 Devotional & Meditation": "🧘 Devoțiune & Meditație",
    "🕊️ Devotional History": "🕊️ Istoric Devoțiuni",
    "💭 Chat History": "💭 Istoric Conversații",
    
    # Scope labels
    "📖 Specific Book": "📖 Carte Specifică",
    "📜 Old Testament": "📜 Vechiul Testament",
    "✝️ New Testament": "✝️ Noul Testament",
    "🌍 Whole Bible": "🌍 Întreaga Biblie",
    
    # Additional scope
    "Entire Old Testament": "Întregul Vechi Testament",
    "Entire New Testament": "Întregul Nou Testament",
    "Specific Book": "Carte Specifică",
    "Entire Bible": "Întreaga Biblie",
    "Multiple Books": "Cărți Multiple",
    
    # Labels
    "Ollama Model (or type)": "Model Ollama (sau tip)",
    "Ollama Status": "Stare Ollama",
    "Online": "Conectat",
    "Offline": "Deconectat",
    "Guided Reading": "Lectură Ghidată",
    "Base": "Bază",
    "Base Chapter": "Capitol de Bază",
    "Verses (e.g., 1, 1-5)": "Versete (ex: 1, 1-5)",
    "Full chapter": "Capitol complet",
    "Theme (optional)": "Temă (opțional)",
    "Target audience (optional)": "Public țintă (opțional)",
    "Extra notes (preacher's context)": "Note suplimentare (context predicator)",
    "Type your biblical question": "Scrieți întrebarea dvs. biblică",
    "Search history": "Căutare istoric",
    "Sort by": "Sortează după",
    "Most recent": "Cel mai recent",
    "Oldest": "Cel mai vechi",
    "Book": "Carte",
    "Sermon": "Predică",
    "Sermon Chapter": "Capitol Predică",
    "Sermon Verse": "Verset Predică",
    "Devotional": "Devoțiune",
    "Devotional Chapter": "Capitol Devoțiune",
    "Devotional Verse": "Verset Devoțiune",
    "Chat": "Conversație",
    "Reading page": "Pagină de lectură",
    "Scope": "Domeniu",
    "Number of questions": "Număr de întrebări",
    "With Answers": "Cu Răspunsuri",
    "Generation Mode": "Mod de Generare",
    "Filter by mode": "Filtrează după mod",
    "All": "Toate",
    "Search": "🔍 Căutare",
    "Type to search...": "Tastați pentru căutare...",
    "Generic": "Generic",
    "Undefined": "Nedefinit",
    
    # Buttons
    "Generate Devotional": "Generează Devoțiune",
    "Clear Cache": "Șterge Cache",
    "Delete": "Șterge",
    "Import Versions from Folder": "Importă Versiuni din Folder",
    
    # Scope prefixes
    "Book:": "Carte:",
    "Chapter": "Capitol",
    "Verse": "Verset",
    "book(s) selected:": "cărți selectate:",
    "Scope:": "Domeniu:",
    "file(s) found": "fișiere găsite",
    "Filter versions (optional)": "Filtrează versiuni (opțional)",
    
    # Search
    "Search sermons": "Căutare predici",
    "Search devotionals": "Căutare devoțiuni",
    "Search conversations": "Căutare conversații",
    "Type book, chapter or keyword...": "Tastați carte, capitol sau cuvânt cheie...",
    "Theme, reference, content...": "Temă, referință, conținut...",
    "Feeling, reference, content...": "Sentiment, referință, conținut...",
    "Order by": "Sortează după",
    
    # Keep existing
    "Keep already imported versions": "Păstrează versiunile deja importate",
    
    # Select multiple
    "Select multiple books": "Selectează cărți multiple",
    
    # Ollama messages
    "Ollama is offline. Start the local server.": "Ollama este offline. Pornește serverul local.",
    "Ollama is offline. Turn on the server and try again.": "Ollama este offline. Pornește serverul și încearcă din nou.",
    "Ollama is offline. Please start the server.": "Ollama este offline. Te rog pornește serverul.",
    "Ollama is offline ({detail}). Please start the server or check your connection.": "Ollama este offline ({detail}). Te rog pornește serverul sau verifică conexiunea.",
    "If models don't appear, use 'ollama pull <model>' via terminal.": "Dacă modelele nu apar, folosește 'ollama pull <model>' prin terminal.",
    
    # Additional labels
    "Please select a valid scope.": "Te rog selectează un domeniu valid.",
    "Choose a base verse to generate the sermon:": "Alege un verset de bază pentru generarea predicii:",
    "Choose a base verse to generate devotional:": "Alege un verset de bază pentru generarea devoțiunii:",
    "Text ready to copy!": "Text gata de copiat!",
    "Enter a single verse or range to use as base or leave blank for the entire chapter.": "Introdu un singur verset sau interval pentru bază sau lasă gol pentru întregul capitol.",
    
    # Messages
    "No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "Nicio predică generată încă. Folosește fila 'Generator de Predici' pentru a crea prima predică!",
    "No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first devotional!": "Nicio devoțiune generată încă. Folosește fila 'Devoțiune & Meditație' pentru a crea prima devoțiune!",
    "No conversations yet. Use 'Theological Chat' tab to start your first conversation!": "Nicio conversație încă. Folosește fila 'Conversație Teologică' pentru a începe prima conversație!",
    "No questions generated yet. Use 'Question Generator' tab to create your first set!": "Nicio întrebare generată încă. Folosește fila 'Generator de Întrebări' pentru a crea primul set!",
    
    # History messages
    "Go to 'Sermon History' tab to review all your sermons.": "Mergi la fila 'Istoric Predici' pentru a revizui toate predicile tale.",
    "Go to 'Devotional History' tab to review all your devotionals.": "Mergi la fila 'Istoric Devoțiuni' pentru a revizui toate devoțiunile tale.",
    "Go to 'Chat History' tab to review all your conversations.": "Mergi la fila 'Istoric Conversații' pentru a revizui toate conversațiile tale.",
    "Go to 'Questions History' tab to review all generated questions.": "Mergi la fila 'Istoric Întrebări' pentru a revizui toate întrebările generate.",
    
    # Additional scope and history
    "study(ies) found": "studii găsite",
    "sermons found": "predici găsite",
    "devotionals found": "devoțiuni găsite",
    "conversations found": "conversații găsite",
    "question set(s) found": "seturi de întrebări găsite",
    "Version:": "Versiune:",
    "Audience:": "Public:",
    "Model:": "Model:",
    "Reference:": "Referință:",
    "Feeling:": "Sentiment:",
    "Question:": "Întrebare:",
    "Answer:": "Răspuns:",
    "Additional notes:": "Note suplimentare:",
    "Context:": "Context:",
    "Explanation:": "Explicație:",
    
    # Prompts
    "Theme:": "Temă:",
    "Audience:": "Public:",
    
    # Headers
    "Sermon Carte": "Carte Predică",
}

def translate_romanian_final(file_path):
    """Traduzir romeno completamente"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    count = 0
    
    for english, romanian in ROMANIAN_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais para regex
        english_escaped = re.escape(english)
        
        # Substituir apenas em valores JSON (após ": ")
        pattern = f'(": ")({english_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, f'\\1{romanian}\\3', content)
            matches = len(re.findall(pattern, original_content))
            count += matches
            print(f"✅ Traduzido ({matches}x): {english} -> {romanian}")
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Total de {count} strings traduzidas em romeno")
    return count

if __name__ == "__main__":
    print("=" * 80)
    print("CORRIGINDO TRADUÇÃO - ROMENO (Română)")
    print("=" * 80)
    
    count = translate_romanian_final("translations/ro.json")
    
    print("\n" + "=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    print(f"✅ Romeno (Română): {count} strings traduzidas")
    print("=" * 80)
