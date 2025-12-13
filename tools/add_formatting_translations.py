#!/usr/bin/env python3
"""Script para adicionar traduções de textos formatados em markdown."""

import json
from pathlib import Path

# Traduções de formatações
FORMATTING_TRANSLATIONS = {
    "pt": {
        "question_label": "💬 Pergunta:",
        "answer_label": "🤖 Resposta:",
        "additional_notes": "📝 Notas adicionais:"
    },
    "en": {
        "question_label": "💬 Question:",
        "answer_label": "🤖 Answer:",
        "additional_notes": "📝 Additional notes:"
    },
    "es": {
        "question_label": "💬 Pregunta:",
        "answer_label": "🤖 Respuesta:",
        "additional_notes": "📝 Notas adicionales:"
    },
    "fr": {
        "question_label": "💬 Question:",
        "answer_label": "🤖 Réponse:",
        "additional_notes": "📝 Notes supplémentaires:"
    },
    "de": {
        "question_label": "💬 Frage:",
        "answer_label": "🤖 Antwort:",
        "additional_notes": "📝 Zusätzliche Hinweise:"
    },
    "ar": {
        "question_label": "💬 سؤال:",
        "answer_label": "🤖 إجابة:",
        "additional_notes": "📝 ملاحظات إضافية:"
    },
    "hi": {
        "question_label": "💬 प्रश्न:",
        "answer_label": "🤖 उत्तर:",
        "additional_notes": "📝 अतिरिक्त नोट्स:"
    },
    "ja": {
        "question_label": "💬 質問:",
        "answer_label": "🤖 回答:",
        "additional_notes": "📝 追加メモ:"
    },
    "ru": {
        "question_label": "💬 Вопрос:",
        "answer_label": "🤖 Ответ:",
        "additional_notes": "📝 Дополнительные заметки:"
    },
    "zh": {
        "question_label": "💬 问题:",
        "answer_label": "🤖 回答:",
        "additional_notes": "📝 附加说明:"
    },
    "it": {
        "question_label": "💬 Domanda:",
        "answer_label": "🤖 Risposta:",
        "additional_notes": "📝 Note aggiuntive:"
    }
}

def add_formatting_translations():
    translations_dir = Path("translations")
    
    for lang_code, translations in FORMATTING_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            # Carregar o arquivo JSON
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            # Criar a seção formatting se não existir
            if "formatting" not in data:
                data["formatting"] = {}
                changed = True
            
            # Adicionar traduções
            for key, value in translations.items():
                if key not in data["formatting"] or data["formatting"][key] != value:
                    data["formatting"][key] = value
                    changed = True
                    print(f"  ✅ {lang_code}.json formatting.{key} = {value}")
            
            # Salvar se houve mudanças
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Arquivo {lang_code}.json atualizado!")
            else:
                print(f"⏭️ {lang_code}.json já está atualizado")
        
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")

if __name__ == "__main__":
    print("🔧 Adicionando traduções de formatação...\n")
    add_formatting_translations()
    print("\n✨ Processo concluído!")
