#!/usr/bin/env python3
"""Script para sincronizar traduções faltantes em todos os idiomas."""

import json
from pathlib import Path

# Traduções completas para todas as chaves faltantes
MISSING_TRANSLATIONS = {
    "es": {
        "labels": {
            "sermon_scope_prompt": "Seleccione el alcance para la generación del sermón:",
            "sermon_scope_specific_book": "📖 Libro Específico",
            "sermon_scope_old_testament": "📜 Antiguo Testamento",
            "sermon_scope_new_testament": "✝️ Nuevo Testamento",
            "sermon_scope_whole_bible": "🌍 Toda la Biblia",
            "select_multiple_books": "🔖 Seleccionar múltiples libros",
            "select_multiple_books_help": "Marcar para seleccionar libros específicos manualmente",
            "select_books_for_sermon": "Seleccione los libros para el sermón:",
            "devotional_scope_prompt": "Seleccione el alcance para la generación del devocional:",
            "select_books_for_devotional": "Seleccione los libros para el devocional:",
            "book_selector": "Libro",
            "chapter_selector": "Capítulo",
            "verse_selector": "Versículo",
            "book_colon": "Libro:",
            "chapter_colon": "Capítulo",
            "verse_colon": "Versículo",
            "selected_books_count": "libro(s) seleccionado(s):",
            "scope_prefix": "Alcance:",
            "whole_old_testament": "Todo el Antiguo Testamento",
            "whole_new_testament": "Todo el Nuevo Testamento",
            "whole_bible": "Toda la Biblia",
            "no_theme": "Sin tema",
            "generic": "Genérico",
            "indefinido": "Indefinido",
            "most_recent_plural": "Más recientes",
            "oldest_plural": "Más antiguos",
            "keep_existing": "✅ Mantener versiones ya importadas",
            "keep_existing_help": "Fusionar con versiones existentes en lugar de reemplazar",
            "guided_reading": "Lectura Guiada",
            "base_book": "Base",
            "base_chapter": "Base Capítulo",
            "full_chapter": "Capítulo completo"
        }
    },
    "fr": {
        "labels": {
            "sermon_scope_prompt": "Sélectionnez la portée pour la génération du sermon:",
            "sermon_scope_specific_book": "📖 Livre Spécifique",
            "sermon_scope_old_testament": "📜 Ancien Testament",
            "sermon_scope_new_testament": "✝️ Nouveau Testament",
            "sermon_scope_whole_bible": "🌍 Toute la Bible",
            "select_multiple_books": "🔖 Sélectionner plusieurs livres",
            "select_multiple_books_help": "Cocher pour sélectionner manuellement des livres spécifiques",
            "select_books_for_sermon": "Sélectionnez les livres pour le sermon:",
            "devotional_scope_prompt": "Sélectionnez la portée pour la génération du dévotion:",
            "select_books_for_devotional": "Sélectionnez les livres pour le dévotion:",
            "book_selector": "Livre",
            "chapter_selector": "Chapitre",
            "verse_selector": "Verset",
            "book_colon": "Livre:",
            "chapter_colon": "Chapitre",
            "verse_colon": "Verset"
        }
    },
    "de": {
        "labels": {
            "sermon_scope_prompt": "Wählen Sie den Umfang für die Predigterstellung:",
            "sermon_scope_specific_book": "📖 Spezifisches Buch",
            "sermon_scope_old_testament": "📜 Altes Testament",
            "sermon_scope_new_testament": "✝️ Neues Testament",
            "sermon_scope_whole_bible": "🌍 Die ganze Bibel",
            "select_multiple_books": "🔖 Mehrere Bücher auswählen",
            "select_multiple_books_help": "Ankreuzen, um spezifische Bücher manuell auszuwählen",
            "select_books_for_sermon": "Wählen Sie die Bücher für die Predigt:",
            "devotional_scope_prompt": "Wählen Sie den Umfang für die Andachtserstellung:",
            "select_books_for_devotional": "Wählen Sie die Bücher für die Andacht:"
        }
    },
    "ar": {
        "labels": {
            "sermon_scope_prompt": "حدد نطاق إنشاء الوعظ:",
            "sermon_scope_specific_book": "📖 كتاب محدد",
            "sermon_scope_old_testament": "📜 العهد القديم",
            "sermon_scope_new_testament": "✝️ العهد الجديد",
            "sermon_scope_whole_bible": "🌍 الكتاب المقدس بأكمله",
            "select_multiple_books": "🔖 اختر كتب متعددة",
            "select_books_for_sermon": "اختر الكتب للوعظ:",
            "devotional_scope_prompt": "حدد نطاق إنشاء التأمل:",
            "select_books_for_devotional": "اختر الكتب للتأمل:"
        }
    },
    "hi": {
        "labels": {
            "sermon_scope_prompt": "उपदेश निर्माण के लिए दायरा चुनें:",
            "sermon_scope_specific_book": "📖 विशिष्ट पुस्तक",
            "sermon_scope_old_testament": "📜 पुराना नियम",
            "sermon_scope_new_testament": "✝️ नया नियम",
            "sermon_scope_whole_bible": "🌍 संपूर्ण बाइबिल",
            "select_multiple_books": "🔖 कई पुस्तकें चुनें",
            "select_books_for_sermon": "उपदेश के लिए पुस्तकें चुनें:",
            "devotional_scope_prompt": "भक्ति निर्माण के लिए दायरा चुनें:",
            "select_books_for_devotional": "भक्ति के लिए पुस्तकें चुनें:"
        }
    },
    "ja": {
        "labels": {
            "sermon_scope_prompt": "説教生成の範囲を選択:",
            "sermon_scope_specific_book": "📖 特定の書",
            "sermon_scope_old_testament": "📜 旧約聖書",
            "sermon_scope_new_testament": "✝️ 新約聖書",
            "sermon_scope_whole_bible": "🌍 聖書全体",
            "select_multiple_books": "🔖 複数の書を選択",
            "select_books_for_sermon": "説教用の書を選択:",
            "devotional_scope_prompt": "デボーション生成の範囲を選択:",
            "select_books_for_devotional": "デボーション用の書を選択:"
        }
    },
    "ru": {
        "labels": {
            "sermon_scope_prompt": "Выберите объем для создания проповеди:",
            "sermon_scope_specific_book": "📖 Конкретная книга",
            "sermon_scope_old_testament": "📜 Ветхий Завет",
            "sermon_scope_new_testament": "✝️ Новый Завет",
            "sermon_scope_whole_bible": "🌍 Вся Библия",
            "select_multiple_books": "🔖 Выбрать несколько книг",
            "select_books_for_sermon": "Выберите книги для проповеди:",
            "devotional_scope_prompt": "Выберите объем для создания размышления:",
            "select_books_for_devotional": "Выберите книги для размышления:"
        }
    },
    "zh": {
        "labels": {
            "sermon_scope_prompt": "选择讲道生成的范围:",
            "sermon_scope_specific_book": "📖 特定书卷",
            "sermon_scope_old_testament": "📜 旧约",
            "sermon_scope_new_testament": "✝️ 新约",
            "sermon_scope_whole_bible": "🌍 整本圣经",
            "select_multiple_books": "🔖 选择多个书卷",
            "select_books_for_sermon": "选择讲道的书卷:",
            "devotional_scope_prompt": "选择灵修生成的范围:",
            "select_books_for_devotional": "选择灵修的书卷:"
        }
    },
    "it": {
        "labels": {
            "sermon_scope_prompt": "Seleziona l'ambito per la generazione del sermone:",
            "sermon_scope_specific_book": "📖 Libro Specifico",
            "sermon_scope_old_testament": "📜 Antico Testamento",
            "sermon_scope_new_testament": "✝️ Nuovo Testamento",
            "sermon_scope_whole_bible": "🌍 Tutta la Bibbia",
            "select_multiple_books": "🔖 Seleziona più libri",
            "select_books_for_sermon": "Seleziona i libri per il sermone:",
            "devotional_scope_prompt": "Seleziona l'ambito per la generazione del devozionale:",
            "select_books_for_devotional": "Seleziona i libri per il devozionale:"
        }
    }
}

def sync_translations():
    translations_dir = Path("translations")
    
    for lang_code, sections in MISSING_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            for section, translations in sections.items():
                if section not in data:
                    data[section] = {}
                    changed = True
                
                for key, value in translations.items():
                    if key not in data[section]:
                        data[section][key] = value
                        changed = True
                        print(f"  ✅ {lang_code}.json {section}.{key} = {value[:50]}...")
            
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Arquivo {lang_code}.json atualizado!\n")
            else:
                print(f"⏭️ {lang_code}.json já está completo\n")
        
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")

if __name__ == "__main__":
    print("🔧 Sincronizando traduções faltantes...\n")
    sync_translations()
    print("\n✨ Sincronização concluída!")
