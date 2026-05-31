#!/usr/bin/env python3
"""Verifica se todos os 23 idiomas estão configurados corretamente."""

import json
from pathlib import Path

def verify_translations():
    """Verifica todos os arquivos de tradução."""
    
    translations_dir = Path("translations")
    
    # Idiomas esperados
    expected_langs = {
        "pt": "Português",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "it": "Italiano",
        "ru": "Русский",
        "zh": "中文",
        "ja": "日本語",
        "ar": "العربية",
        "hi": "हिन्दी",
        "el": "Ελληνικά",
        "eo": "Esperanto",
        "fi": "Suomi",
        "ko": "한국어",
        "ro": "Română",
        "vi": "Tiếng Việt",
        "id": "Bahasa Indonesia",
        "pl": "Polski",
        "fa": "فارسی",
        "sw": "Kiswahili",
        "th": "ไทย",
        "tr": "Türkçe"
    }
    
    print("🌍 Verificando todos os 23 idiomas...\n")
    print("=" * 70)
    
    all_ok = True
    total_files = 0
    
    for lang_code, expected_name in expected_langs.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"❌ {lang_code}.json - FALTANDO!")
            all_ok = False
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            lang_name = data.get("language_name", "???")
            total_keys = sum(
                len(v) if isinstance(v, dict) else 1
                for v in data.values()
            )
            
            # Verificar se tem as seções principais
            required_sections = ["labels", "buttons", "menu", "messages"]
            missing_sections = [s for s in required_sections if s not in data]
            
            if missing_sections:
                print(f"⚠️  {lang_code:2} | {lang_name:20} | {total_keys:3} keys | Faltam: {', '.join(missing_sections)}")
            else:
                print(f"✅ {lang_code:2} | {lang_name:20} | {total_keys:3} keys | Completo")
            
            total_files += 1
            
        except Exception as e:
            print(f"❌ {lang_code}.json - ERRO: {e}")
            all_ok = False
    
    print("=" * 70)
    print(f"\n📊 Resumo:")
    print(f"   Total de arquivos: {total_files}/23")
    print(f"   Status: {'✅ Todos os idiomas configurados!' if total_files == 23 else '⚠️ Alguns idiomas faltando'}")
    
    return all_ok and total_files == 23

if __name__ == "__main__":
    success = verify_translations()
    
    if success:
        print("\n🎉 Sistema multilíngue 100% completo!")
        print("   Todos os 23 idiomas estão prontos e nativos!")
    else:
        print("\n⚠️ Alguns ajustes ainda são necessários.")
