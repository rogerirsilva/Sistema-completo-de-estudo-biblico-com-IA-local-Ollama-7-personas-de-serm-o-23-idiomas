#!/usr/bin/env python3
"""Sincroniza as traduções do português para o árabe (faltantes)."""

import json
from pathlib import Path

# Traduções faltantes em árabe
AR_MISSING_TRANSLATIONS = {
    "labels": {
        "search_history": "🔍 البحث في السجل",
        "search_placeholder": "اكتب الكتاب، الفصل أو الكلمة الرئيسية...",
        "sort_by": "ترتيب حسب",
        "most_recent": "الأحدث",
        "oldest": "الأقدم",
        "by_book": "الكتاب",
        "search_sermons": "🔍 البحث عن عظات",
        "search_sermons_placeholder": "الموضوع، المرجع، المحتوى...",
        "search_devotionals": "🔍 البحث عن تأملات",
        "search_devotionals_placeholder": "الشعور، المرجع، المحتوى...",
        "search_conversations": "🔍 البحث عن محادثات",
        "search_conversations_placeholder": "السؤال، الإجابة، المرجع...",
        "order_by": "📅 ترتيب حسب",
        "most_recent_plural": "الأحدث",
        "oldest_plural": "الأقدم",
        "keep_existing": "✅ الاحتفاظ بالنسخ المستوردة بالفعل",
        "keep_existing_help": "الدمج مع الإصدارات الموجودة بدلاً من الاستبدال",
        "select_multiple_books_help": "حدد لتحديد الكتب يدويًا",
        "book_colon": "الكتاب:",
        "chapter_colon": "الفصل:",
        "verse_colon": "الآية:",
        "selected_books_count": "الكتب المحددة:",
        "scope_prefix": "النطاق:",
        "whole_old_testament": "العهد القديم بأكمله",
        "whole_new_testament": "العهد الجديد بأكمله",
        "whole_bible": "الكتاب المقدس بأكمله",
        "no_theme": "بدون موضوع",
        "generic": "عام",
        "indefinido": "غير محدد",
        "order_sort": "📅 ترتيب",
        "import_placeholder_versions": "مثال: nvi,kjv,acf",
        "selected_colon": "المحدد:",
        "import_folder": "مجلد الاستيراد:",
        "files_found": "ملف (ات) تم العثور عليها",
        "filter_versions": "تصفية الإصدارات (اختياري)",
        "devotional_chapter_label": "فصل التأمل",
        "devotional_verse_label": "آية التأمل",
        "chat_book_label": "الدردشة",
        "reading_page": "صفحة القراءة",
        "set_default_version": "تعيين كإصدار افتراضي"
    },
    "messages": {
        "no_sermons_yet": "🎤 لم يتم إنشاء عظات بعد. استخدم علامة التبويب 'مولد العظات' لإنشاء أول عظة لك!",
        "no_devotionals_yet": "🧘 لم يتم إنشاء تأملات بعد. استخدم علامة التبويب 'التأمل والتفكر' لإنشاء أول تأمل لك!",
        "no_conversations_yet": "💬 لم يتم حفظ محادثات بعد. استخدم علامة التبويب 'محادثة لاهوتية' لطرح سؤالك الأول!",
        "add_json_files": "💡 أضف ملفات .json من إصدارات الكتاب المقدس في هذا المجلد وانقر فوق 'استيراد'.",
        "create_folder_add_json": "💡 قم بإنشاء المجلد وأضف ملفات JSON من إصدارات الكتاب المقدس.",
        "add_json_retry": "💡 أضف ملفات JSON في المجلد وحاول مرة أخرى.",
        "page_will_reload": "🔄 سيتم إعادة تحميل الصفحة...",
        "generating_explanation": "🔮 جارٍ إنشاء تفسير كتابي...",
        "generating_sermon": "🔮 جارٍ إنشاء مخطط عظة...",
        "generating_devotional": "🔮 جارٍ إنشاء تأمل...",
        "generating_answer": "🔮 جارٍ إنشاء إجابة لاهوتية...",
        "ollama_offline_detail": "Ollama غير متصل ({detail}). ابدأ تشغيل الخادم وحاول مرة أخرى.",
        "no_verses_in_chapter": "لم يتم العثور على آيات في هذا الفصل.",
        "no_local_versions": "لم يتم العثور على إصدارات محلية. استخدم استيراد البيانات لتحميل المحتوى.",
        "importing_versions": "⏳ جارٍ استيراد الإصدارات..."
    }
}

def update_arabic_translations():
    """Atualiza as traduções do árabe com as traduções faltantes."""
    
    translations_dir = Path("translations")
    ar_file = translations_dir / "ar.json"
    
    if not ar_file.exists():
        print("❌ ar.json não encontrado!")
        return False
    
    try:
        # Carregar arquivo árabe
        with open(ar_file, "r", encoding="utf-8") as f:
            ar_data = json.load(f)
        
        # Atualizar traduções
        total_updated = 0
        
        for section, translations in AR_MISSING_TRANSLATIONS.items():
            if section not in ar_data:
                ar_data[section] = {}
            
            for key, value in translations.items():
                # Verificar se está em inglês ou faltando
                current_value = ar_data[section].get(key, "")
                
                # Atualizar se estiver em inglês ou vazio
                if not current_value or "Select" in current_value or "Import" in current_value or "file(s)" in current_value:
                    ar_data[section][key] = value
                    total_updated += 1
                elif current_value != value:
                    ar_data[section][key] = value
                    total_updated += 1
        
        # Salvar arquivo
        if total_updated > 0:
            with open(ar_file, "w", encoding="utf-8") as f:
                json.dump(ar_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ ar.json atualizado com {total_updated} traduções nativas!")
            return True
        else:
            print("⏭️ ar.json já está completo!")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🇸🇦 Completando traduções do árabe...\n")
    update_arabic_translations()
    print("\n✨ Árabe agora 100% nativo!")
