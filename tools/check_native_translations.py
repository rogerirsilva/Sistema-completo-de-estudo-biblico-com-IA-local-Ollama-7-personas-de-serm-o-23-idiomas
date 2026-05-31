#!/usr/bin/env python3
"""
Verifica se há strings em inglês ou português em arquivos de tradução não-EN/PT.
Identifica possíveis textos não traduzidos.
"""

import json
from pathlib import Path
import re

# Palavras comuns em inglês/português que indicam texto não traduzido
ENGLISH_INDICATORS = [
    "Select", "Import", "Export", "file", "folder", "Book", "Chapter",
    "Verse", "History", "Search", "Filter", "Keep", "already", "imported",
    "versions", "optional", "selected", "found", "Preview", "View",
    "Context", "Explanation", "Full", "How", "Add", "Versions", "Bible",
    "Studies", "Sermon", "Scope", "Devotional", "Meditation", "Theological",
    "Chat", "Conversation", "Generator", "Testament", "Whole", "Specific"
]

PORTUGUESE_INDICATORS = [
    "Selecione", "Importar", "Exportar", "arquivo", "pasta", "Livro",
    "Capítulo", "Versículo", "História", "Buscar", "Filtrar", "Manter",
    "importadas", "versões", "opcional", "selecionado", "encontrado",
    "Prévia", "Ver", "Contexto", "Explicação", "Completo", "Como",
    "Adicionar", "Versões", "Bíblia", "Estudos", "Sermão", "Escopo",
    "Devocional", "Meditação", "Teológico", "Chat", "Conversa"
]

def check_for_untranslated(lang_code, data, excluded_langs={"en", "pt", "es"}):
    """Verifica se há textos não traduzidos em um idioma."""
    
    if lang_code in excluded_langs:
        return []
    
    issues = []
    
    def check_value(section, key, value, path=""):
        """Verifica um valor específico."""
        if not isinstance(value, str):
            return
        
        # Verificar indicadores de inglês
        for indicator in ENGLISH_INDICATORS:
            # Usar regex para encontrar palavras completas
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, value, re.IGNORECASE):
                issues.append({
                    "section": section,
                    "key": key,
                    "value": value,
                    "issue": f"Possível inglês: '{indicator}'",
                    "path": path
                })
                return
        
        # Verificar indicadores de português (só se não for espanhol, que é similar)
        if lang_code != "es":
            for indicator in PORTUGUESE_INDICATORS:
                pattern = r'\b' + re.escape(indicator) + r'\b'
                if re.search(pattern, value, re.IGNORECASE):
                    issues.append({
                        "section": section,
                        "key": key,
                        "value": value,
                        "issue": f"Possível português: '{indicator}'",
                        "path": path
                    })
                    return
    
    # Percorrer todas as seções
    for section, content in data.items():
        if isinstance(content, dict):
            for key, value in content.items():
                check_value(section, key, value, f"{section}.{key}")
        elif isinstance(content, str):
            check_value("root", section, content, section)
    
    return issues

def verify_all_translations():
    """Verifica todos os arquivos de tradução."""
    
    translations_dir = Path("translations")
    
    print("🔍 Verificando traduções em todos os idiomas...\n")
    print("=" * 80)
    
    total_issues = 0
    languages_with_issues = []
    
    for json_file in sorted(translations_dir.glob("*.json")):
        lang_code = json_file.stem
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            issues = check_for_untranslated(lang_code, data)
            
            if issues:
                print(f"\n⚠️  {lang_code}.json - {len(issues)} possível(is) problema(s):")
                for issue in issues[:5]:  # Mostrar apenas os 5 primeiros
                    print(f"   • {issue['path']}: {issue['issue']}")
                    print(f"     Valor: '{issue['value'][:60]}...'")
                
                if len(issues) > 5:
                    print(f"   ... e mais {len(issues) - 5} problema(s)")
                
                total_issues += len(issues)
                languages_with_issues.append((lang_code, len(issues)))
            else:
                lang_name = data.get("language_name", lang_code)
                print(f"✅ {lang_code}.json ({lang_name}) - 100% nativo!")
        
        except Exception as e:
            print(f"❌ Erro ao processar {lang_code}.json: {e}")
    
    print("\n" + "=" * 80)
    print(f"\n📊 Resumo:")
    print(f"   Total de problemas encontrados: {total_issues}")
    
    if languages_with_issues:
        print(f"\n   Idiomas com possíveis problemas:")
        for lang, count in languages_with_issues:
            print(f"   • {lang}: {count} problema(s)")
    else:
        print(f"\n   🎉 Todos os idiomas estão 100% nativos!")
    
    return total_issues == 0

if __name__ == "__main__":
    all_native = verify_all_translations()
    
    if all_native:
        print("\n✨ Sistema 100% multilíngue! Todos os idiomas nativos!")
    else:
        print("\n⚠️ Alguns idiomas ainda têm textos não nativos.")
        print("   Execute os scripts de correção para completar as traduções.")
