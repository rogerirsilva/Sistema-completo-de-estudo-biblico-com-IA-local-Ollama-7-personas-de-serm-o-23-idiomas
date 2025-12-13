#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para SUBSTITUIR traduções em inglês por traduções nativas
"""

import json
import os
import re

# Mapeamento de traduções: texto em inglês -> tradução em cada idioma
TRANSLATIONS_MAP = {
    "fa": {  # Persa
        # Labels
        "Ollama Model (or type)": "مدل Ollama",
        "Ollama Status": "وضعیت Ollama",
        "Online": "آنلاین",
        "Offline": "آفلاین",
        "If models don't appear, use 'ollama pull <model>' via terminal.": "اگر مدل‌ها نمایش داده نمی‌شوند، از 'ollama pull <model>' در ترمینال استفاده کنید",
        "Guided Reading": "خواندن راهنما",
        "Base": "پایه",
        "Base Chapter": "فصل پایه",
        "Verses (e.g., 1, 1-5)": "آیات (مثال: 1، 1-5)",
        "Enter a single verse or range to use as base or leave blank for the entire chapter.": "یک آیه یا محدوده را وارد کنید یا برای کل فصل خالی بگذارید",
        "Full chapter": "فصل کامل",
        "Theme (optional)": "موضوع (اختیاری)",
        "Target audience (optional)": "مخاطب هدف (اختیاری)",
        "Extra notes (preacher's context)": "یادداشت‌های اضافی",
        "Theme or feeling to meditate on": "موضوع یا احساس برای مراقبه",
        "Type your biblical question": "سوال کتاب مقدس خود را تایپ کنید",
        "Search history": "جستجوی تاریخچه",
        "Type book, chapter or keyword...": "کتاب، فصل یا کلمه کلیدی را تایپ کنید...",
        "Sort by": "مرتب‌سازی بر اساس",
        "Most recent": "جدیدترین",
        "Oldest": "قدیمی‌ترین",
        "Book": "کتاب",
        "Search sermons": "جستجوی موعظه‌ها",
        "Theme, reference, content...": "موضوع، مرجع، محتوا...",
        "Search devotionals": "جستجوی عبادات",
        "Feeling, reference, content...": "احساس، مرجع، محتوا...",
        "Search conversations": "جستجوی گفتگوها",
        "Question, answer, reference...": "سوال، پاسخ، مرجع...",
        "Order by": "مرتب‌سازی بر اساس",
        "Keep already imported versions": "نگه داشتن نسخه‌های وارد شده",
        "Merge with existing versions instead of replacing": "ادغام با نسخه‌های موجود به جای جایگزینی",
        "Select the scope for sermon generation:": "محدوده تولید موعظه را انتخاب کنید:",
        "Specific Book": "کتاب خاص",
        "Old Testament": "عهد عتیق",
        "New Testament": "عهد جدید",
        "Whole Bible": "کل کتاب مقدس",
        "Sermon": "موعظه",
        "Sermon Chapter": "فصل موعظه",
        "Sermon Verse": "آیه موعظه",
        "Select multiple books": "انتخاب چند کتاب",
        "Check to manually select specific books": "علامت بزنید تا کتاب‌های خاص را به صورت دستی انتخاب کنید",
        "Select the books for the sermon:": "کتاب‌ها را برای موعظه انتخاب کنید:",
        "Select the scope for devotional generation:": "محدوده تولید عبادت را انتخاب کنید:",
        "Devotional": "عبادت",
        "Select the books for the devotional:": "کتاب‌ها را برای عبادت انتخاب کنید:",
        "Book:": "کتاب:",
        "Chapter": "فصل",
        "Verse": "آیه",
        "book(s) selected:": "کتاب(ها) انتخاب شده:",
        "Scope:": "محدوده:",
        "Entire Old Testament": "کل عهد عتیق",
        "Entire New Testament": "کل عهد جدید",
        "Entire Bible": "کل کتاب مقدس",
        "No theme": "بدون موضوع",
        "Generic": "عمومی",
        "Undefined": "تعریف نشده",
        "Sort": "مرتب‌سازی",
        "Ex: nvi,kjv,acf": "مثال: nvi,kjv,acf",
        "Selected:": "انتخاب شده:",
        "Import folder:": "پوشه وارد کردن:",
        "file(s) found": "فایل(ها) یافت شد",
        "Filter versions (optional)": "فیلتر نسخه‌ها (اختیاری)",
        "Devotional Chapter": "فصل عبادت",
        "Devotional Verse": "آیه عبادت",
        "Chat": "گفتگو",
        "Reading page": "صفحه خواندن",
        "Set as default version on startup": "تنظیم به عنوان نسخه پیش‌فرض در شروع",
        "Multiple Books": "کتاب‌های متعدد",
        "Scope": "محدوده",
        "Selected book:": "کتاب انتخاب شده:",
        "Select books": "انتخاب کتاب‌ها",
        "Selected books:": "کتاب‌های انتخاب شده:",
        "Number of questions": "تعداد سوالات",
        "Number of questions to generate": "تعداد سوالات برای تولید",
        "With Answers": "با پاسخ‌ها",
        "Questions Only": "فقط سوالات",
        "Generation Mode": "حالت تولید",
        "Filter by mode": "فیلتر بر اساس حالت",
        "All": "همه",
        "Search": "جستجو",
        "Type to search...": "برای جستجو تایپ کنید...",
        
        # Buttons
        "Generate Devotional": "تولید عبادت",
        "Clear Cache": "پاک کردن حافظه موقت",
        "Delete": "حذف",
        "Import Versions from Folder": "وارد کردن نسخه‌ها از پوشه",
        "Copy sermon": "کپی موعظه",
        "Copy devotional": "کپی عبادت",
        "Copy conversation": "کپی گفتگو",
        
        # Menu
        "Sermon Generator": "تولیدکننده موعظه",
        "Sermon History": "تاریخچه موعظه‌ها",
        "Devotional & Meditation": "عبادت و مراقبه",
        "Devotional History": "تاریخچه عبادات",
        "Chat History": "تاریخچه گفتگو",
        
        # Messages
        "Import a Bible version to start guided reading.": "یک نسخه کتاب مقدس را وارد کنید تا خواندن راهنما را شروع کنید",
        "Select at least 2 books.": "حداقل 2 کتاب انتخاب کنید",
        "Select books to continue": "کتاب‌ها را برای ادامه انتخاب کنید",
        "Please select a valid scope.": "لطفاً یک محدوده معتبر انتخاب کنید",
        "Generating Bible questions...": "در حال تولید سوالات کتاب مقدس...",
        "Questions generated and saved!": "سوالات تولید و ذخیره شدند!",
        "Go to 'Questions History' tab.": "به تب 'تاریخچه سوالات' بروید",
        "No questions generated yet.": "هنوز سوالی تولید نشده است",
        
        # Headers
        "Bible Questions Generator": "تولیدکننده سوالات کتاب مقدس",
        "Query Scope": "محدوده پرس‌وجو",
        
        # Captions
        "Generate questions about biblical knowledge.": "سوالاتی درباره دانش کتاب مقدس تولید کنید",
        "All generated questions are automatically saved here.": "تمام سوالات تولید شده به صورت خودکار اینجا ذخیره می‌شوند",
        "{count} question set(s) found": "{count} مجموعه سوال یافت شد",
        
        # Expanders
        "Questions Preview": "پیش‌نمایش سوالات",
    }
}

def replace_english_with_native(filepath, translations_map):
    """Substitui textos em inglês por traduções nativas"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir cada texto em inglês pela tradução
        for english, native in translations_map.items():
            # Escapar caracteres especiais para regex
            english_escaped = re.escape(english)
            # Substituir o texto mantendo as aspas e formatação JSON
            content = re.sub(f'"{english_escaped}"', f'"{native}"', content)
        
        # Salvar de volta
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def main():
    print("🔄 Substituindo textos em inglês por traduções nativas...")
    print()
    
    for lang_code, translations in TRANSLATIONS_MAP.items():
        filepath = os.path.join("translations", f"{lang_code}.json")
        
        if os.path.exists(filepath):
            if replace_english_with_native(filepath, translations):
                print(f"✅ {lang_code}.json - {len(translations)} substituições aplicadas")
            else:
                print(f"❌ Erro ao processar {lang_code}.json")
        else:
            print(f"⚠️  {lang_code}.json não encontrado")
    
    print()
    print("🎉 Substituições concluídas!")

if __name__ == "__main__":
    main()
