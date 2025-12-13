"""
Adicionar traduções para botões de copiar específicos
"""
import json
from pathlib import Path

# Novas traduções para botões específicos
button_translations = {
    "pt": {
        "copy_sermon": "📋 Copiar sermão",
        "copy_devotional": "📋 Copiar devocional",
        "copy_conversation": "📋 Copiar conversa"
    },
    "en": {
        "copy_sermon": "📋 Copy sermon",
        "copy_devotional": "📋 Copy devotional",
        "copy_conversation": "📋 Copy conversation"
    },
    "hi": {
        "copy_sermon": "📋 उपदेश कॉपी करें",
        "copy_devotional": "📋 भक्ति कॉपी करें",
        "copy_conversation": "📋 बातचीत कॉपी करें"
    },
    "ja": {
        "copy_sermon": "📋 説教をコピー",
        "copy_devotional": "📋 黙想をコピー",
        "copy_conversation": "📋 会話をコピー"
    }
}

translations_dir = Path("translations")

for lang_code, buttons in button_translations.items():
    filepath = translations_dir / f"{lang_code}.json"
    
    # Carregar arquivo existente
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Adicionar à seção buttons
    if "buttons" not in data:
        data["buttons"] = {}
    
    for key, value in buttons.items():
        data["buttons"][key] = value
    
    # Salvar arquivo atualizado
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {lang_code.upper()}: {len(buttons)} novos botões adicionados")

print("\n🎉 Traduções de botões específicos adicionadas!")
