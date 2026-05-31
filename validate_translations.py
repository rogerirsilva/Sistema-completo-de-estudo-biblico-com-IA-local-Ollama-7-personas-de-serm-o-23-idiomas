#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de VALIDAÇÃO FINAL - Verifica se há textos em inglês nos idiomas
"""

import json
import re
import os

# Palavras comuns em inglês que NÃO devem aparecer (exceto en.json e pt.json)
ENGLISH_PATTERNS = [
    r'"(Select|Import|Generate|Create|Write|Answer|Load|Check|View|Error|Warning|Question|Generating|Importing|Explanation)',
    r': "(No [A-Z]|The [A-Z]|How to|Use [A-Z])',
    r'"[A-Z][a-z]+( [a-z]+){3,}"',  # Frases longas em inglês
]

def check_english_text(filepath):
    """Verifica se há texto em inglês no arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    for pattern in ENGLISH_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            issues.extend(matches)
    
    return list(set(issues))  # Remove duplicatas

def main():
    translations_dir = "translations"
    # Idiomas a verificar (excluir en.json e pt.json que são base)
    check_langs = ["ar", "de", "el", "eo", "es", "fa", "fi", "fr", "hi", "id", 
                   "it", "ja", "ko", "pl", "ro", "ru", "sw", "th", "tr", "vi", "zh"]
    
    print("🔍 VALIDAÇÃO FINAL - Verificando textos em inglês...")
    print("=" * 70)
    
    total_issues = 0
    languages_with_issues = []
    
    for lang_code in check_langs:
        filepath = os.path.join(translations_dir, f"{lang_code}.json")
        
        if not os.path.exists(filepath):
            continue
        
        issues = check_english_text(filepath)
        
        if issues:
            total_issues += len(issues)
            languages_with_issues.append(lang_code)
            print(f"⚠️  {lang_code.upper()}: {len(issues)} possíveis textos em inglês")
            for issue in issues[:5]:  # Mostrar apenas os primeiros 5
                print(f"   - {issue}")
        else:
            print(f"✅ {lang_code.upper()}: LIMPO (0 textos em inglês)")
    
    print("=" * 70)
    if total_issues == 0:
        print("🎉 PERFEITO! TODOS os idiomas estão 100% traduzidos!")
        print("✨ Zero textos em inglês encontrados!")
    else:
        print(f"⚠️  {total_issues} possíveis problemas em {len(languages_with_issues)} idiomas")
        print(f"   Idiomas: {', '.join(languages_with_issues)}")

if __name__ == "__main__":
    main()
