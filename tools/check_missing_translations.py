#!/usr/bin/env python3
"""Script para verificar traduções ausentes comparando todos os idiomas com pt.json."""

import json
from pathlib import Path
from typing import Dict, Set

def get_all_keys(data: dict, prefix: str = "") -> Set[str]:
    """Extrai todas as chaves de um dicionário aninhado."""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys

def check_missing_translations():
    translations_dir = Path("translations")
    
    # Carregar pt.json como referência
    pt_file = translations_dir / "pt.json"
    with open(pt_file, "r", encoding="utf-8") as f:
        pt_data = json.load(f)
    
    # Obter todas as chaves de pt.json
    pt_keys = get_all_keys(pt_data)
    print(f"📊 Total de chaves em pt.json: {len(pt_keys)}\n")
    
    # Verificar cada idioma
    lang_files = sorted(translations_dir.glob("*.json"))
    
    for lang_file in lang_files:
        if lang_file.name == "pt.json":
            continue
        
        lang_code = lang_file.stem
        
        with open(lang_file, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
        
        lang_keys = get_all_keys(lang_data)
        missing_keys = pt_keys - lang_keys
        
        if missing_keys:
            print(f"⚠️ {lang_code}.json - Faltam {len(missing_keys)} traduções:")
            for key in sorted(missing_keys)[:10]:  # Mostrar apenas 10 primeiras
                print(f"   - {key}")
            if len(missing_keys) > 10:
                print(f"   ... e mais {len(missing_keys) - 10} chaves")
            print()
        else:
            print(f"✅ {lang_code}.json - Completo ({len(lang_keys)} chaves)")

if __name__ == "__main__":
    print("🔍 Verificando traduções ausentes...\n")
    check_missing_translations()
    print("\n✨ Verificação concluída!")
