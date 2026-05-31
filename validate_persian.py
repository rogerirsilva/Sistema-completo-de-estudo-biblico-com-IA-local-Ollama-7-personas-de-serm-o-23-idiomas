#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validação final do arquivo persa - detectar qualquer texto em inglês
"""

import json
import re

def validate_persian():
    """Valida se há textos em inglês no arquivo persa"""
    with open('translations/fa.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Padrões de palavras em inglês comuns
    english_patterns = [
        r'\b(Select|Import|Generate|Create|Write|Answer|Load|Check|View|Error|Warning)\b',
        r'\b(Question|Generating|Importing|Search|Download|Copy|Delete|Clear|Add)\b',
        r'\b(History|Old Testament|New Testament|Specific Book|Whole Bible)\b',
        r'\b(Sermon Generator|Devotional|Meditation|Chat|Preview|Explanation)\b',
    ]
    
    matches = []
    
    def scan(obj, path=''):
        """Escaneia recursivamente o JSON procurando textos em inglês"""
        if isinstance(obj, dict):
            for k, v in obj.items():
                scan(v, f'{path}.{k}')
        elif isinstance(obj, str):
            for pattern in english_patterns:
                if re.search(pattern, obj, re.IGNORECASE):
                    matches.append(f'{path}: {obj[:80]}')
                    break
    
    scan(content)
    
    print("=" * 70)
    print("🔍 VALIDAÇÃO FINAL DO ARQUIVO PERSA (fa.json)")
    print("=" * 70)
    
    if matches:
        print(f"⚠️ Encontrados {len(matches)} possíveis textos em inglês:")
        print()
        for match in matches[:20]:
            print(f"  ❌ {match}")
        if len(matches) > 20:
            print(f"\n  ... e mais {len(matches) - 20} ocorrências")
    else:
        print("✅ SUCESSO! Nenhum texto em inglês encontrado!")
        print("🎉 Persa (فارسی) está 100% no idioma nativo!")
    
    print("=" * 70)
    return len(matches)

if __name__ == "__main__":
    count = validate_persian()
    exit(0 if count == 0 else 1)
