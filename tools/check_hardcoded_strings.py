#!/usr/bin/env python3
"""Script para verificar se ainda há textos em português hardcoded no código."""

import re
from pathlib import Path

# Padrões de texto em português para procurar (excluindo comentários e docstrings)
PORTUGUESE_PATTERNS = [
    r'"[^"]*(?:ão|ções|ção|ã|õ|á|é|í|ó|ú|ê|â|ô|à)[^"]*"',  # Strings com acentos portugueses
    r"'[^']*(?:ão|ções|ção|ã|õ|á|é|í|ó|ú|ê|â|ô|à)[^']*'",  # Strings com acentos portugueses
]

# Exceções permitidas (variáveis, nomes de arquivos, etc.)
ALLOWED_EXCEPTIONS = [
    "Dados_Json",
    "version",
    "versions",
    "books",
    "chapters",
    "verses",
    "abbrev",
    "notas",
    "publico",
    "question",
    "answer",
    "sermon",
    "reference",
    ".json",
    "bible_data",
    "app_config",
]

def check_hardcoded_strings():
    app_file = Path("app.py")
    
    if not app_file.exists():
        print("❌ Arquivo app.py não encontrado!")
        return
    
    print("🔍 Verificando strings hardcoded em app.py...\n")
    
    with open(app_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    found_issues = []
    
    for line_num, line in enumerate(lines, 1):
        # Ignorar comentários e docstrings
        if line.strip().startswith("#") or '"""' in line or "'''" in line:
            continue
        
        # Ignorar linhas com t(trans, ...)
        if "t(trans," in line:
            continue
        
        # Procurar por strings com acentos portugueses
        for pattern in PORTUGUESE_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                text = match.group()
                
                # Verificar se é uma exceção permitida
                is_exception = any(exc in text for exc in ALLOWED_EXCEPTIONS)
                
                if not is_exception:
                    found_issues.append({
                        "line": line_num,
                        "text": text.strip(),
                        "context": line.strip()
                    })
    
    if found_issues:
        print(f"⚠️ Encontradas {len(found_issues)} possíveis strings hardcoded:\n")
        for issue in found_issues[:20]:  # Mostrar apenas os primeiros 20
            print(f"Linha {issue['line']}: {issue['text']}")
            print(f"  Contexto: {issue['context'][:100]}...\n")
        
        if len(found_issues) > 20:
            print(f"... e mais {len(found_issues) - 20} ocorrências.")
    else:
        print("✅ Nenhuma string hardcoded encontrada!")
        print("✨ Todas as strings parecem estar usando a função t() para tradução.")

if __name__ == "__main__":
    check_hardcoded_strings()
