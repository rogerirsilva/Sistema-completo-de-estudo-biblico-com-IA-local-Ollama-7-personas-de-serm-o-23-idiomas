#!/usr/bin/env python3
"""Script para copiar todas as traduções de en.json para os idiomas incompletos."""

import json
from pathlib import Path
from typing import Dict, Any

# Mapeamento manual de traduções para cada seção
MANUAL_TRANSLATIONS = {
    "es": {
        "language_name": "Español"
    },
    "fr": {
        "language_name": "Français"
    },
    "de": {
        "language_name": "Deutsch"
    },
    "ar": {
        "language_name": "العربية"
    },
    "ru": {
        "language_name": "Русский"
    },
    "zh": {
        "language_name": "中文"
    },
    "it": {
        "language_name": "Italiano"
    }
}

def merge_translations(base: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
    """Mescla traduções base com target, mantendo traduções existentes."""
    result = target.copy()
    
    for key, value in base.items():
        if key not in result:
            result[key] = value
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_translations(value, result[key])
    
    return result

def complete_all_translations():
    translations_dir = Path("translations")
    
    # Carregar en.json como base (está completo)
    en_file = translations_dir / "en.json"
    with open(en_file, "r", encoding="utf-8") as f:
        en_data = json.load(f)
    
    print("📚 Usando en.json como base de referência\n")
    
    # Processar cada idioma
    for lang_code in ["es", "fr", "de", "ar", "ru", "zh", "it"]:
        lang_file = translations_dir / f"{lang_code}.json"
        
        if not lang_file.exists():
            print(f"⚠️ {lang_code}.json não encontrado")
            continue
        
        print(f"🔧 Processando {lang_code}.json...")
        
        try:
            # Carregar arquivo existente
            with open(lang_file, "r", encoding="utf-8") as f:
                lang_data = json.load(f)
            
            # Contar traduções antes
            def count_keys(d):
                count = 0
                for v in d.values():
                    if isinstance(v, dict):
                        count += count_keys(v)
                    else:
                        count += 1
                return count
            
            before = count_keys(lang_data)
            
            # Mesclar com en.json
            merged = merge_translations(en_data, lang_data)
            
            # Aplicar traduções manuais (como language_name)
            if lang_code in MANUAL_TRANSLATIONS:
                for key, value in MANUAL_TRANSLATIONS[lang_code].items():
                    merged[key] = value
            
            # Contar depois
            after = count_keys(merged)
            added = after - before
            
            # Salvar
            with open(lang_file, "w", encoding="utf-8") as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)
            
            if added > 0:
                print(f"   ✅ Adicionadas {added} traduções ({before} → {after})")
            else:
                print(f"   ⏭️ Já estava completo ({after} traduções)")
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n✨ Sincronização completa concluída!")
    print("\n⚠️ IMPORTANTE: As traduções foram copiadas do inglês.")
    print("   Revise os arquivos e ajuste as traduções específicas de cada idioma.")

if __name__ == "__main__":
    print("🌍 Completando TODAS as traduções faltantes...\n")
    complete_all_translations()
