#!/usr/bin/env python3
"""Script para adicionar tradução do botão clear_cache em todos os idiomas."""

import json
from pathlib import Path

# Traduções para cada idioma
TRANSLATIONS = {
    "ar": "مسح ذاكرة التخزين المؤقت",
    "de": "Cache leeren",
    "en": "Clear Cache",
    "es": "Limpiar Caché",
    "fr": "Vider le Cache",
    "hi": "कैश साफ करें",
    "it": "Svuota Cache",
    "ja": "キャッシュをクリア",
    "pt": "Limpar Cache",
    "ru": "Очистить кэш",
    "zh": "清除缓存"
}

def add_clear_cache_translation():
    translations_dir = Path("translations")
    
    for lang_code, translation_text in TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            # Carregar o arquivo JSON
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Criar a seção buttons se não existir
            if "buttons" not in data:
                data["buttons"] = {}
                print(f"ℹ️ Criando seção 'buttons' em {lang_code}.json")
            
            # Adicionar a tradução se não existir
            if "clear_cache" not in data["buttons"]:
                data["buttons"]["clear_cache"] = f"🔄 {translation_text}"
                
                # Salvar o arquivo
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Adicionado em {lang_code}.json: {translation_text}")
            else:
                print(f"⏭️ Já existe em {lang_code}.json")
        
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")

if __name__ == "__main__":
    add_clear_cache_translation()
    print("\n✨ Processo concluído!")

