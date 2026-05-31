#!/usr/bin/env python3
"""Script para adicionar tradução de 'Contexto selecionado'."""

import json
from pathlib import Path

CONTEXT_TRANSLATIONS = {
    "pt": "Contexto selecionado:",
    "en": "Selected context:",
    "es": "Contexto seleccionado:",
    "fr": "Contexte sélectionné:",
    "de": "Ausgewählter Kontext:",
    "ar": "السياق المحدد:",
    "hi": "चयनित संदर्भ:",
    "ja": "選択されたコンテキスト:",
    "ru": "Выбранный контекст:",
    "zh": "选定的上下文:",
    "it": "Contesto selezionato:"
}

def add_context_translation():
    translations_dir = Path("translations")
    
    for lang_code, translation in CONTEXT_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            if "formatting" not in data:
                data["formatting"] = {}
                changed = True
            
            if "selected_context" not in data["formatting"]:
                data["formatting"]["selected_context"] = translation
                changed = True
                print(f"  ✅ {lang_code}.json formatting.selected_context = {translation}")
            
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Arquivo {lang_code}.json atualizado!")
            else:
                print(f"⏭️ {lang_code}.json já está atualizado")
        
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")

if __name__ == "__main__":
    add_context_translation()
    print("\n✨ Concluído!")
