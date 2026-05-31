"""
Verificar e melhorar traduções dos menus em todos os idiomas
"""
import json
from pathlib import Path

# Traduções completas e corretas dos menus
menu_translations = {
    "pt": {
        "reading": "📖 Leitura & Exegese",
        "history": "📚 Histórico de Estudos",
        "sermon_gen": "🗣️ Gerador Sermões",
        "sermon_hist": "📋 Histórico Sermões",
        "devotional": "🧘 Devocional & Meditação",
        "devotional_hist": "🕊️ Histórico Devocionais",
        "chat": "💬 Chat Teológico",
        "chat_hist": "💭 Histórico Chat",
        "import": "📥 Importar Dados"
    },
    "en": {
        "reading": "📖 Reading & Exegesis",
        "history": "📚 Study History",
        "sermon_gen": "🗣️ Sermon Generator",
        "sermon_hist": "📋 Sermon History",
        "devotional": "🧘 Devotional & Meditation",
        "devotional_hist": "🕊️ Devotional History",
        "chat": "💬 Theological Chat",
        "chat_hist": "💭 Chat History",
        "import": "📥 Import Data"
    },
    "hi": {
        "reading": "📖 पठन और व्याख्या",
        "history": "📚 अध्ययन इतिहास",
        "sermon_gen": "🗣️ उपदेश जनरेटर",
        "sermon_hist": "📋 उपदेश इतिहास",
        "devotional": "🧘 भक्ति और ध्यान",
        "devotional_hist": "🕊️ भक्ति इतिहास",
        "chat": "💬 धर्मशास्त्रीय चैट",
        "chat_hist": "💭 चैट इतिहास",
        "import": "📥 डेटा आयात करें"
    },
    "ja": {
        "reading": "📖 読書と釈義",
        "history": "📚 学習履歴",
        "sermon_gen": "🗣️ 説教ジェネレーター",
        "sermon_hist": "📋 説教履歴",
        "devotional": "🧘 黙想と瞑想",
        "devotional_hist": "🕊️ 黙想履歴",
        "chat": "💬 神学チャット",
        "chat_hist": "💭 チャット履歴",
        "import": "📥 データをインポート"
    }
}

translations_dir = Path("translations")

for lang_code, menus in menu_translations.items():
    filepath = translations_dir / f"{lang_code}.json"
    
    # Carregar arquivo existente
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Atualizar seção de menu
    if "menu" not in data:
        data["menu"] = {}
    
    data["menu"] = menus
    
    # Salvar arquivo atualizado
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {lang_code.upper()}: Menus atualizados")
    for key, value in menus.items():
        print(f"   - {key}: {value}")

print("\n🎉 Todos os menus foram verificados e atualizados!")
