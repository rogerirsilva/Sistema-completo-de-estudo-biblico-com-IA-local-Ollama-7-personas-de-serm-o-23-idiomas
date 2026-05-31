import json
import re

# Traduções polonesas completas
POLISH_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ Generator Kazań",
    "📋 Sermon History": "📋 Historia Kazań",
    "🧘 Devotional & Meditation": "🧘 Rozważania & Medytacja",
    "🕊️ Devotional History": "🕊️ Historia Rozważań",
    "💭 Chat History": "💭 Historia Rozmów",
    
    # Scope labels
    "📖 Specific Book": "📖 Konkretna Księga",
    "📜 Old Testament": "📜 Stary Testament",
    "✝️ New Testament": "✝️ Nowy Testament",
    "🌍 Whole Bible": "🌍 Cała Biblia",
    
    # Additional scope
    "Entire Old Testament": "Cały Stary Testament",
    "Entire New Testament": "Cały Nowy Testament",
    "Specific Book": "Konkretna Księga",
    "Entire Bible": "Cała Biblia",
    "Multiple Books": "Wiele Ksiąg",
    
    # Labels
    "Ollama Model (or type)": "Model Ollama (lub typ)",
    "Ollama Status": "Status Ollama",
    "Online": "Online",
    "Offline": "Offline",
    "Guided Reading": "Czytanie z Przewodnikiem",
    "Base": "Baza",
    "Base Chapter": "Rozdział Bazowy",
    "Verses (e.g., 1, 1-5)": "Wersety (np. 1, 1-5)",
    "Full chapter": "Pełny rozdział",
    "Theme (optional)": "Temat (opcjonalnie)",
    "Target audience (optional)": "Grupa docelowa (opcjonalnie)",
    "Extra notes (preacher's context)": "Dodatkowe notatki (kontekst kaznodziei)",
    "Type your biblical question": "Wpisz swoje pytanie biblijne",
    "Search history": "Przeszukaj historię",
    "Sort by": "Sortuj według",
    "Most recent": "Najnowsze",
    "Oldest": "Najstarsze",
    "Book": "Księga",
    "Sermon": "Kazanie",
    "Sermon Chapter": "Rozdział Kazania",
    "Sermon Verse": "Werset Kazania",
    "Devotional": "Rozważanie",
    "Devotional Chapter": "Rozdział Rozważania",
    "Devotional Verse": "Werset Rozważania",
    "Chat": "Rozmowa",
    "Reading page": "Strona czytania",
    "Scope": "Zakres",
    "Number of questions": "Liczba pytań",
    "With Answers": "Z Odpowiedziami",
    "Generation Mode": "Tryb Generowania",
    "Filter by mode": "Filtruj według trybu",
    "All": "Wszystkie",
    "Search": "🔍 Szukaj",
    "Type to search...": "Wpisz, aby wyszukać...",
    "Generic": "Ogólny",
    "Undefined": "Nieokreślony",
    
    # Buttons
    "Generate Devotional": "Wygeneruj Rozważanie",
    "Clear Cache": "Wyczyść Pamięć Podręczną",
    "Delete": "Usuń",
    "Import Versions from Folder": "Importuj Wersje z Folderu",
    "Copy sermon": "Kopiuj kazanie",
    "Copy devotional": "Kopiuj rozważanie",
    "Copy conversation": "Kopiuj rozmowę",
    
    # Scope prefixes
    "Book:": "Księga:",
    "Chapter": "Rozdział",
    "Verse": "Werset",
    "book(s) selected:": "wybranych ksiąg:",
    "Scope:": "Zakres:",
    "file(s) found": "znalezionych plików",
    "Filter versions (optional)": "Filtruj wersje (opcjonalnie)",
    
    # Search
    "Search sermons": "Szukaj kazań",
    "Search devotionals": "Szukaj rozważań",
    "Search conversations": "Szukaj rozmów",
    "Type book, chapter or keyword...": "Wpisz księgę, rozdział lub słowo kluczowe...",
    "Theme, reference, content...": "Temat, odniesienie, treść...",
    "Feeling, reference, content...": "Uczucie, odniesienie, treść...",
    "Order by": "Sortuj według",
    
    # Keep existing
    "Keep already imported versions": "Zachowaj już zaimportowane wersje",
    
    # Select multiple
    "Select multiple books": "Wybierz wiele ksiąg",
    
    # Ollama messages
    "Ollama is offline. Start the local server.": "Ollama jest offline. Uruchom lokalny serwer.",
    "Ollama is offline. Turn on the server and try again.": "Ollama jest offline. Włącz serwer i spróbuj ponownie.",
    "Ollama is offline. Please start the server.": "Ollama jest offline. Proszę uruchomić serwer.",
    "Ollama is offline ({detail}). Please start the server or check your connection.": "Ollama jest offline ({detail}). Proszę uruchomić serwer lub sprawdzić połączenie.",
    "If models don't appear, use 'ollama pull <model>' via terminal.": "Jeśli modele nie pojawiają się, użyj 'ollama pull <model>' w terminalu.",
    
    # Additional labels
    "Please select a valid scope.": "Proszę wybrać prawidłowy zakres.",
    "Choose a base verse to generate the sermon:": "Wybierz werset bazowy do wygenerowania kazania:",
    "Choose a base verse to generate devotional:": "Wybierz werset bazowy do wygenerowania rozważania:",
    "Text ready to copy!": "Tekst gotowy do skopiowania!",
    "Enter a single verse or range to use as base or leave blank for the entire chapter.": "Wprowadź pojedynczy werset lub zakres jako bazę lub pozostaw puste dla całego rozdziału.",
    
    # Messages
    "No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "Nie wygenerowano jeszcze żadnych kazań. Użyj zakładki 'Generator Kazań', aby stworzyć pierwsze kazanie!",
    "No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first devotional!": "Nie wygenerowano jeszcze żadnych rozważań. Użyj zakładki 'Rozważania & Medytacja', aby stworzyć pierwsze rozważanie!",
    "No conversations yet. Use 'Theological Chat' tab to start your first conversation!": "Nie ma jeszcze żadnych rozmów. Użyj zakładki 'Czat Teologiczny', aby rozpocząć pierwszą rozmowę!",
    "No questions generated yet. Use 'Question Generator' tab to create your first set!": "Nie wygenerowano jeszcze żadnych pytań. Użyj zakładki 'Generator Pytań', aby stworzyć pierwszy zestaw!",
    
    # History messages
    "Go to 'Sermon History' tab to review all your sermons.": "Przejdź do zakładki 'Historia Kazań', aby przejrzeć wszystkie swoje kazania.",
    "Go to 'Devotional History' tab to review all your devotionals.": "Przejdź do zakładki 'Historia Rozważań', aby przejrzeć wszystkie swoje rozważania.",
    "Go to 'Chat History' tab to review all your conversations.": "Przejdź do zakładki 'Historia Rozmów', aby przejrzeć wszystkie swoje rozmowy.",
    "Go to 'Questions History' tab to review all generated questions.": "Przejdź do zakładki 'Historia Pytań', aby przejrzeć wszystkie wygenerowane pytania.",
    
    # Additional scope and history
    "study(ies) found": "znalezionych studiów",
    "sermons found": "znalezionych kazań",
    "devotionals found": "znalezionych rozważań",
    "conversations found": "znalezionych rozmów",
    "question set(s) found": "znalezionych zestawów pytań",
    "Version:": "Wersja:",
    "Audience:": "Odbiorcy:",
    "Model:": "Model:",
    "Reference:": "Odniesienie:",
    "Feeling:": "Uczucie:",
    "Question:": "Pytanie:",
    "Answer:": "Odpowiedź:",
    "Additional notes:": "Dodatkowe notatki:",
    "Context:": "Kontekst:",
    "Explanation:": "Wyjaśnienie:",
    
    # Prompts
    "Theme:": "Temat:",
    "Audience:": "Odbiorcy:",
    
    # Headers
    "Sermon Księga": "Księga Kazania",
}

def translate_polish_final(file_path):
    """Traduzir polonês completamente"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    count = 0
    
    for english, polish in POLISH_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais para regex
        english_escaped = re.escape(english)
        
        # Substituir apenas em valores JSON (após ": ")
        pattern = f'(": ")({english_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, f'\\1{polish}\\3', content)
            matches = len(re.findall(pattern, original_content))
            count += matches
            print(f"✅ Traduzido ({matches}x): {english} -> {polish}")
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Total de {count} strings traduzidas em polonês")
    return count

if __name__ == "__main__":
    print("=" * 80)
    print("CORRIGINDO TRADUÇÃO - POLONÊS (Polski)")
    print("=" * 80)
    
    count = translate_polish_final("translations/pl.json")
    
    print("\n" + "=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    print(f"✅ Polonês (Polski): {count} strings traduzidas")
    print("=" * 80)
