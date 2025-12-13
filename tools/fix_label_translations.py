#!/usr/bin/env python3
"""Script para corrigir labels sem acentos e adicionar traduções faltantes."""

import json
from pathlib import Path

# Traduções para corrigir/adicionar
LABEL_TRANSLATIONS = {
    "pt": {
        "sermon_book_label": "Sermão",
        "sermon_chapter_label": "Sermão Capítulo",
        "sermon_verse_label": "Sermão Versículo",
        "devotional_book_label": "Devocional",
        "devotional_chapter_label": "Devocional Capítulo",
        "devotional_verse_label": "Devocional Versículo",
        "chat_book_label": "Chat",
        "base_book": "Base"
    },
    "en": {
        "sermon_book_label": "Sermon",
        "sermon_chapter_label": "Sermon Chapter",
        "sermon_verse_label": "Sermon Verse",
        "devotional_book_label": "Devotional",
        "devotional_chapter_label": "Devotional Chapter",
        "devotional_verse_label": "Devotional Verse",
        "chat_book_label": "Chat",
        "base_book": "Base"
    },
    "es": {
        "sermon_book_label": "Sermón",
        "sermon_chapter_label": "Sermón Capítulo",
        "sermon_verse_label": "Sermón Versículo",
        "devotional_book_label": "Devocional",
        "devotional_chapter_label": "Devocional Capítulo",
        "devotional_verse_label": "Devocional Versículo",
        "chat_book_label": "Chat",
        "base_book": "Base"
    },
    "fr": {
        "sermon_book_label": "Sermon",
        "sermon_chapter_label": "Sermon Chapitre",
        "sermon_verse_label": "Sermon Verset",
        "devotional_book_label": "Dévotion",
        "devotional_chapter_label": "Dévotion Chapitre",
        "devotional_verse_label": "Dévotion Verset",
        "chat_book_label": "Chat",
        "base_book": "Base"
    },
    "de": {
        "sermon_book_label": "Predigt",
        "sermon_chapter_label": "Predigt Kapitel",
        "sermon_verse_label": "Predigt Vers",
        "devotional_book_label": "Andacht",
        "devotional_chapter_label": "Andacht Kapitel",
        "devotional_verse_label": "Andacht Vers",
        "chat_book_label": "Chat",
        "base_book": "Basis"
    },
    "ar": {
        "sermon_book_label": "عظة",
        "sermon_chapter_label": "عظة الفصل",
        "sermon_verse_label": "عظة الآية",
        "devotional_book_label": "تأملي",
        "devotional_chapter_label": "تأملي الفصل",
        "devotional_verse_label": "تأملي الآية",
        "chat_book_label": "محادثة",
        "base_book": "قاعدة"
    },
    "hi": {
        "sermon_book_label": "उपदेश",
        "sermon_chapter_label": "उपदेश अध्याय",
        "sermon_verse_label": "उपदेश पद",
        "devotional_book_label": "भक्ति",
        "devotional_chapter_label": "भक्ति अध्याय",
        "devotional_verse_label": "भक्ति पद",
        "chat_book_label": "चैट",
        "base_book": "आधार"
    },
    "ja": {
        "sermon_book_label": "説教",
        "sermon_chapter_label": "説教章",
        "sermon_verse_label": "説教節",
        "devotional_book_label": "デボーション",
        "devotional_chapter_label": "デボーション章",
        "devotional_verse_label": "デボーション節",
        "chat_book_label": "チャット",
        "base_book": "ベース"
    },
    "ru": {
        "sermon_book_label": "Проповедь",
        "sermon_chapter_label": "Проповедь Глава",
        "sermon_verse_label": "Проповедь Стих",
        "devotional_book_label": "Размышление",
        "devotional_chapter_label": "Размышление Глава",
        "devotional_verse_label": "Размышление Стих",
        "chat_book_label": "Чат",
        "base_book": "База"
    },
    "zh": {
        "sermon_book_label": "讲道",
        "sermon_chapter_label": "讲道章",
        "sermon_verse_label": "讲道节",
        "devotional_book_label": "灵修",
        "devotional_chapter_label": "灵修章",
        "devotional_verse_label": "灵修节",
        "chat_book_label": "聊天",
        "base_book": "基础"
    },
    "it": {
        "sermon_book_label": "Sermone",
        "sermon_chapter_label": "Sermone Capitolo",
        "sermon_verse_label": "Sermone Versetto",
        "devotional_book_label": "Devozionale",
        "devotional_chapter_label": "Devozionale Capitolo",
        "devotional_verse_label": "Devozionale Versetto",
        "chat_book_label": "Chat",
        "base_book": "Base"
    }
}

# Traduções de headers
HEADER_TRANSLATIONS = {
    "pt": {
        "sermon_generator": "Gerador de Sermões",
        "devotional_meditation": "Devocional e Meditação",
        "theological_chat": "Chat Teológico"
    },
    "en": {
        "sermon_generator": "Sermon Generator",
        "devotional_meditation": "Devotional and Meditation",
        "theological_chat": "Theological Chat"
    },
    "es": {
        "sermon_generator": "Generador de Sermones",
        "devotional_meditation": "Devocional y Meditación",
        "theological_chat": "Chat Teológico"
    },
    "fr": {
        "sermon_generator": "Générateur de Sermons",
        "devotional_meditation": "Dévotion et Méditation",
        "theological_chat": "Chat Théologique"
    },
    "de": {
        "sermon_generator": "Predigtgenerator",
        "devotional_meditation": "Andacht und Meditation",
        "theological_chat": "Theologischer Chat"
    },
    "ar": {
        "sermon_generator": "مولد العظات",
        "devotional_meditation": "التأمل والتفكر",
        "theological_chat": "محادثة لاهوتية"
    },
    "hi": {
        "sermon_generator": "उपदेश जनरेटर",
        "devotional_meditation": "भक्ति और ध्यान",
        "theological_chat": "धार्मिक चैट"
    },
    "ja": {
        "sermon_generator": "説教ジェネレーター",
        "devotional_meditation": "デボーションと瞑想",
        "theological_chat": "神学チャット"
    },
    "ru": {
        "sermon_generator": "Генератор проповедей",
        "devotional_meditation": "Размышление и медитация",
        "theological_chat": "Богословский чат"
    },
    "zh": {
        "sermon_generator": "讲道生成器",
        "devotional_meditation": "灵修和冥想",
        "theological_chat": "神学聊天"
    },
    "it": {
        "sermon_generator": "Generatore di Sermoni",
        "devotional_meditation": "Devozionale e Meditazione",
        "theological_chat": "Chat Teologica"
    }
}

def fix_translations():
    translations_dir = Path("translations")
    
    for lang_code in LABEL_TRANSLATIONS.keys():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ Arquivo não encontrado: {json_file}")
            continue
        
        try:
            # Carregar o arquivo JSON
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            # Atualizar labels
            if "labels" not in data:
                data["labels"] = {}
                changed = True
            
            for key, value in LABEL_TRANSLATIONS[lang_code].items():
                if key not in data["labels"] or data["labels"][key] != value:
                    data["labels"][key] = value
                    changed = True
                    print(f"  ✅ {lang_code}.json labels.{key} = {value}")
            
            # Atualizar headers
            if "headers" not in data:
                data["headers"] = {}
                changed = True
            
            if lang_code in HEADER_TRANSLATIONS:
                for key, value in HEADER_TRANSLATIONS[lang_code].items():
                    if key not in data["headers"] or data["headers"][key] != value:
                        data["headers"][key] = value
                        changed = True
                        print(f"  ✅ {lang_code}.json headers.{key} = {value}")
            
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
    print("🔧 Corrigindo traduções de labels e headers...\n")
    fix_translations()
    print("\n✨ Processo concluído!")
