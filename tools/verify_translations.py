"""
Verificador de traduções - testa se todas as strings estão traduzidas
"""
import json
from pathlib import Path

def verify_translations():
    """Verifica se todos os idiomas têm as mesmas chaves"""
    
    translations_dir = Path("translations")
    languages = ["pt", "en", "hi", "ja"]
    
    # Carregar todas as traduções
    all_translations = {}
    for lang in languages:
        filepath = translations_dir / f"{lang}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            all_translations[lang] = json.load(f)
    
    # Usar português como referência
    pt_keys = get_all_keys(all_translations["pt"])
    
    print("="*70)
    print("VERIFICAÇÃO DE TRADUÇÕES COMPLETAS")
    print("="*70)
    
    all_complete = True
    
    for lang in languages:
        lang_keys = get_all_keys(all_translations[lang])
        missing = pt_keys - lang_keys
        extra = lang_keys - pt_keys
        
        lang_name = all_translations[lang].get("language_name", lang)
        print(f"\n📖 {lang.upper()} - {lang_name}")
        print(f"   Total de chaves: {len(lang_keys)}")
        
        if missing:
            print(f"   ❌ Chaves faltando: {len(missing)}")
            for key in sorted(missing)[:5]:  # Mostrar apenas as 5 primeiras
                print(f"      - {key}")
            if len(missing) > 5:
                print(f"      ... e mais {len(missing) - 5}")
            all_complete = False
        else:
            print(f"   ✅ Todas as chaves presentes!")
        
        if extra:
            print(f"   ⚠️  Chaves extras: {len(extra)}")
    
    print("\n" + "="*70)
    if all_complete:
        print("🎉 SUCESSO! Todos os idiomas estão completos!")
    else:
        print("⚠️  Alguns idiomas estão incompletos. Verifique acima.")
    print("="*70)
    
    # Estatísticas gerais
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Idiomas verificados: {len(languages)}")
    print(f"   Chaves base (português): {len(pt_keys)}")
    print(f"   Seções principais:")
    for section in ["labels", "buttons", "menu", "messages", "expanders", "headers", "prompts"]:
        if section in all_translations["pt"]:
            count = len(all_translations["pt"][section])
            print(f"      - {section}: {count} itens")

def get_all_keys(translation_dict, prefix=""):
    """Obtém todas as chaves aninhadas de um dicionário de tradução"""
    keys = set()
    for key, value in translation_dict.items():
        if key == "language_name":
            continue
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys

if __name__ == "__main__":
    verify_translations()
