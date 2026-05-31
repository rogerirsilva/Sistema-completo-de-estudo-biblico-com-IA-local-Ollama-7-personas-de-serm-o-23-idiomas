#!/usr/bin/env python3
"""Script para traduzir TODAS as strings para idiomas 100% nativos."""

import json
from pathlib import Path

# Traduções completas e nativas para cada idioma
NATIVE_TRANSLATIONS = {
    "ar": {
        # Árabe - Tradução completa
        "language_name": "العربية",
        "menu": {
            "reading": "📖 القراءة والتفسير",
            "history": "📚 تاريخ الدراسات",
            "sermon_gen": "🗣️ مولد العظات",
            "sermon_hist": "📋 تاريخ العظات",
            "devotional": "🧘 التأمل والتفكر",
            "devotional_hist": "🕊️ تاريخ التأملات",
            "chat": "💬 محادثة لاهوتية",
            "chat_hist": "💭 تاريخ المحادثات",
            "import": "📥 استيراد البيانات"
        },
        "labels": {
            "bible_version": "نسخة الكتاب المقدس",
            "ollama_model": "نموذج Ollama",
            "ollama_status": "حالة Ollama",
            "ollama_status_online": "متصل",
            "ollama_status_offline": "غير متصل",
            "ollama_help": "إذا لم تظهر النماذج، استخدم 'ollama pull <model>' عبر الطرفية.",
            "language_selector": "🌍 اللغة",
            "guided_reading": "القراءة الموجهة",
            "base_book": "الكتاب الأساسي",
            "base_chapter": "الفصل الأساسي",
            "verses": "الآيات (مثال: 1، 1-5)",
            "full_chapter": "الفصل كاملاً",
            "theme_optional": "الموضوع (اختياري)",
            "audience_optional": "الجمهور المستهدف (اختياري)",
            "extra_notes": "ملاحظات إضافية",
            "theme_or_feeling": "موضوع أو شعور للتأمل",
            "your_question": "اكتب سؤالك الكتابي",
            "book_selector": "الكتاب",
            "chapter_selector": "الفصل",
            "verse_selector": "الآية",
            "language": "اللغة"
        },
        "buttons": {
            "generate_explanation": "✨ إنشاء تفسير كتابي",
            "generate_sermon": "✨ إنشاء مخطط عظة",
            "generate_devotional": "✨ إنشاء تأمل",
            "send_question": "✨ إرسال السؤال",
            "clear_history": "🗑️ مسح السجل",
            "clear_cache": "🔄 مسح ذاكرة التخزين المؤقت",
            "copy": "📋 نسخ",
            "delete": "🗑️ حذف",
            "import_versions": "🔄 استيراد الإصدارات من المجلد",
            "copy_sermon": "📋 نسخ العظة",
            "copy_devotional": "📋 نسخ التأمل",
            "copy_conversation": "📋 نسخ المحادثة"
        }
    },
    "de": {
        # Alemão - Tradução completa
        "language_name": "Deutsch",
        "menu": {
            "reading": "📖 Lesen & Exegese",
            "history": "📚 Studienhistorie",
            "sermon_gen": "🗣️ Predigtgenerator",
            "sermon_hist": "📋 Predigthistorie",
            "devotional": "🧘 Andacht & Meditation",
            "devotional_hist": "🕊️ Andachtshistorie",
            "chat": "💬 Theologischer Chat",
            "chat_hist": "💭 Chat-Historie",
            "import": "📥 Daten importieren"
        },
        "labels": {
            "bible_version": "Bibelversion",
            "ollama_model": "Ollama-Modell",
            "ollama_status": "Ollama-Status",
            "ollama_status_online": "Online",
            "ollama_status_offline": "Offline",
            "ollama_help": "Falls Modelle nicht erscheinen, verwenden Sie 'ollama pull <Modell>' über das Terminal.",
            "language_selector": "🌍 Sprache",
            "guided_reading": "Geführtes Lesen",
            "base_book": "Basisbuch",
            "base_chapter": "Basiskapitel",
            "verses": "Verse (z.B.: 1, 1-5)",
            "full_chapter": "Ganzes Kapitel",
            "theme_optional": "Thema (optional)",
            "audience_optional": "Zielgruppe (optional)",
            "extra_notes": "Zusätzliche Notizen",
            "theme_or_feeling": "Thema oder Gefühl zur Meditation",
            "your_question": "Geben Sie Ihre biblische Frage ein",
            "book_selector": "Buch",
            "chapter_selector": "Kapitel",
            "verse_selector": "Vers",
            "language": "Sprache"
        },
        "buttons": {
            "generate_explanation": "✨ Biblische Erklärung generieren",
            "generate_sermon": "✨ Predigtgliederung generieren",
            "generate_devotional": "✨ Andacht generieren",
            "send_question": "✨ Frage senden",
            "clear_history": "🗑️ Verlauf löschen",
            "clear_cache": "🔄 Cache leeren",
            "copy": "📋 Kopieren",
            "delete": "🗑️ Löschen",
            "import_versions": "🔄 Versionen aus Ordner importieren",
            "copy_sermon": "📋 Predigt kopieren",
            "copy_devotional": "📋 Andacht kopieren",
            "copy_conversation": "📋 Gespräch kopieren"
        }
    },
    "fr": {
        # Francês - Tradução completa
        "language_name": "Français",
        "menu": {
            "reading": "📖 Lecture & Exégèse",
            "history": "📚 Historique des Études",
            "sermon_gen": "🗣️ Générateur de Sermons",
            "sermon_hist": "📋 Historique des Sermons",
            "devotional": "🧘 Dévotion & Méditation",
            "devotional_hist": "🕊️ Historique des Dévotions",
            "chat": "💬 Chat Théologique",
            "chat_hist": "💭 Historique des Discussions",
            "import": "📥 Importer des Données"
        },
        "labels": {
            "bible_version": "Version de la Bible",
            "ollama_model": "Modèle Ollama",
            "ollama_status": "Statut Ollama",
            "ollama_status_online": "En ligne",
            "ollama_status_offline": "Hors ligne",
            "ollama_help": "Si les modèles n'apparaissent pas, utilisez 'ollama pull <modèle>' via le terminal.",
            "language_selector": "🌍 Langue",
            "guided_reading": "Lecture Guidée",
            "base_book": "Livre de Base",
            "base_chapter": "Chapitre de Base",
            "verses": "Versets (ex: 1, 1-5)",
            "full_chapter": "Chapitre complet",
            "theme_optional": "Thème (optionnel)",
            "audience_optional": "Public cible (optionnel)",
            "extra_notes": "Notes supplémentaires",
            "theme_or_feeling": "Thème ou sentiment à méditer",
            "your_question": "Posez votre question biblique",
            "book_selector": "Livre",
            "chapter_selector": "Chapitre",
            "verse_selector": "Verset",
            "language": "Langue"
        },
        "buttons": {
            "generate_explanation": "✨ Générer une Explication Biblique",
            "generate_sermon": "✨ Générer un Plan de Sermon",
            "generate_devotional": "✨ Générer une Dévotion",
            "send_question": "✨ Envoyer la Question",
            "clear_history": "🗑️ Effacer l'historique",
            "clear_cache": "🔄 Vider le Cache",
            "copy": "📋 Copier",
            "delete": "🗑️ Supprimer",
            "import_versions": "🔄 Importer des Versions du Dossier",
            "copy_sermon": "📋 Copier le sermon",
            "copy_devotional": "📋 Copier la dévotion",
            "copy_conversation": "📋 Copier la conversation"
        }
    },
    "it": {
        # Italiano - Tradução completa
        "language_name": "Italiano",
        "menu": {
            "reading": "📖 Lettura & Esegesi",
            "history": "📚 Cronologia degli Studi",
            "sermon_gen": "🗣️ Generatore di Sermoni",
            "sermon_hist": "📋 Cronologia dei Sermoni",
            "devotional": "🧘 Devozionale & Meditazione",
            "devotional_hist": "🕊️ Cronologia dei Devozionali",
            "chat": "💬 Chat Teologica",
            "chat_hist": "💭 Cronologia Chat",
            "import": "📥 Importa Dati"
        },
        "labels": {
            "bible_version": "Versione della Bibbia",
            "ollama_model": "Modello Ollama",
            "ollama_status": "Stato Ollama",
            "ollama_status_online": "Online",
            "ollama_status_offline": "Offline",
            "ollama_help": "Se i modelli non appaiono, usa 'ollama pull <modello>' tramite terminale.",
            "language_selector": "🌍 Lingua",
            "guided_reading": "Lettura Guidata",
            "base_book": "Libro Base",
            "base_chapter": "Capitolo Base",
            "verses": "Versetti (es: 1, 1-5)",
            "full_chapter": "Capitolo completo",
            "theme_optional": "Tema (opzionale)",
            "audience_optional": "Pubblico di destinazione (opzionale)",
            "extra_notes": "Note aggiuntive",
            "theme_or_feeling": "Tema o sentimento da meditare",
            "your_question": "Scrivi la tua domanda biblica",
            "book_selector": "Libro",
            "chapter_selector": "Capitolo",
            "verse_selector": "Versetto",
            "language": "Lingua"
        },
        "buttons": {
            "generate_explanation": "✨ Genera Spiegazione Biblica",
            "generate_sermon": "✨ Genera Schema del Sermone",
            "generate_devotional": "✨ Genera Devozionale",
            "send_question": "✨ Invia Domanda",
            "clear_history": "🗑️ Cancella cronologia",
            "clear_cache": "🔄 Svuota Cache",
            "copy": "📋 Copia",
            "delete": "🗑️ Elimina",
            "import_versions": "🔄 Importa Versioni dalla Cartella",
            "copy_sermon": "📋 Copia sermone",
            "copy_devotional": "📋 Copia devozionale",
            "copy_conversation": "📋 Copia conversazione"
        }
    },
    "ru": {
        # Russo - Tradução completa
        "language_name": "Русский",
        "menu": {
            "reading": "📖 Чтение и Экзегеза",
            "history": "📚 История Исследований",
            "sermon_gen": "🗣️ Генератор Проповедей",
            "sermon_hist": "📋 История Проповедей",
            "devotional": "🧘 Размышление и Медитация",
            "devotional_hist": "🕊️ История Размышлений",
            "chat": "💬 Богословский Чат",
            "chat_hist": "💭 История Чата",
            "import": "📥 Импорт Данных"
        },
        "labels": {
            "bible_version": "Версия Библии",
            "ollama_model": "Модель Ollama",
            "ollama_status": "Статус Ollama",
            "ollama_status_online": "В сети",
            "ollama_status_offline": "Не в сети",
            "ollama_help": "Если модели не появляются, используйте 'ollama pull <модель>' через терминал.",
            "language_selector": "🌍 Язык",
            "guided_reading": "Управляемое Чтение",
            "base_book": "Базовая Книга",
            "base_chapter": "Базовая Глава",
            "verses": "Стихи (напр.: 1, 1-5)",
            "full_chapter": "Полная глава",
            "theme_optional": "Тема (необязательно)",
            "audience_optional": "Целевая аудитория (необязательно)",
            "extra_notes": "Дополнительные заметки",
            "theme_or_feeling": "Тема или чувство для медитации",
            "your_question": "Введите ваш библейский вопрос",
            "book_selector": "Книга",
            "chapter_selector": "Глава",
            "verse_selector": "Стих",
            "language": "Язык"
        },
        "buttons": {
            "generate_explanation": "✨ Создать Библейское Объяснение",
            "generate_sermon": "✨ Создать План Проповеди",
            "generate_devotional": "✨ Создать Размышление",
            "send_question": "✨ Отправить Вопрос",
            "clear_history": "🗑️ Очистить историю",
            "clear_cache": "🔄 Очистить кэш",
            "copy": "📋 Копировать",
            "delete": "🗑️ Удалить",
            "import_versions": "🔄 Импортировать Версии из Папки",
            "copy_sermon": "📋 Копировать проповедь",
            "copy_devotional": "📋 Копировать размышление",
            "copy_conversation": "📋 Копировать беседу"
        }
    },
    "zh": {
        # Chinês - Tradução completa
        "language_name": "中文",
        "menu": {
            "reading": "📖 阅读与释经",
            "history": "📚 研究历史",
            "sermon_gen": "🗣️ 讲道生成器",
            "sermon_hist": "📋 讲道历史",
            "devotional": "🧘 灵修与冥想",
            "devotional_hist": "🕊️ 灵修历史",
            "chat": "💬 神学聊天",
            "chat_hist": "💭 聊天历史",
            "import": "📥 导入数据"
        },
        "labels": {
            "bible_version": "圣经版本",
            "ollama_model": "Ollama 模型",
            "ollama_status": "Ollama 状态",
            "ollama_status_online": "在线",
            "ollama_status_offline": "离线",
            "ollama_help": "如果模型未显示，请通过终端使用'ollama pull <模型>'。",
            "language_selector": "🌍 语言",
            "guided_reading": "引导式阅读",
            "base_book": "基础书卷",
            "base_chapter": "基础章节",
            "verses": "经文（例：1, 1-5）",
            "full_chapter": "整章",
            "theme_optional": "主题（可选）",
            "audience_optional": "目标受众（可选）",
            "extra_notes": "附加说明",
            "theme_or_feeling": "冥想的主题或感受",
            "your_question": "输入您的圣经问题",
            "book_selector": "书卷",
            "chapter_selector": "章",
            "verse_selector": "节",
            "language": "语言"
        },
        "buttons": {
            "generate_explanation": "✨ 生成圣经解释",
            "generate_sermon": "✨ 生成讲道大纲",
            "generate_devotional": "✨ 生成灵修",
            "send_question": "✨ 发送问题",
            "clear_history": "🗑️ 清除历史",
            "clear_cache": "🔄 清除缓存",
            "copy": "📋 复制",
            "delete": "🗑️ 删除",
            "import_versions": "🔄 从文件夹导入版本",
            "copy_sermon": "📋 复制讲道",
            "copy_devotional": "📋 复制灵修",
            "copy_conversation": "📋 复制对话"
        }
    }
}

def apply_native_translations():
    """Aplica traduções 100% nativas para cada idioma."""
    translations_dir = Path("translations")
    
    for lang_code, sections in NATIVE_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ {lang_code}.json não encontrado")
            continue
        
        print(f"🌍 Atualizando {lang_code}.json para tradução 100% nativa...")
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            updated = 0
            
            for section, translations in sections.items():
                if isinstance(translations, dict):
                    if section not in data:
                        data[section] = {}
                    
                    for key, value in translations.items():
                        if data[section].get(key) != value:
                            data[section][key] = value
                            updated += 1
                else:
                    if data.get(section) != translations:
                        data[section] = translations
                        updated += 1
            
            if updated > 0:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"   ✅ {updated} traduções atualizadas")
            else:
                print(f"   ⏭️ Já nativo")
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    print("🌍 Aplicando traduções 100% nativas...\n")
    apply_native_translations()
    print("\n✨ Todos os idiomas agora são 100% nativos!")
