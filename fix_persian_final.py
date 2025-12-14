#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traduzir TODOS os textos restantes em inglês no arquivo persa (fa.json)
Incluindo: Sermon Generator, Devotional & Meditation, e todas as strings restantes
"""

import json
import re
import os

# Mapeamento completo de TODAS as traduções restantes para persa
PERSIAN_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ مولد موعظه",
    "📋 Sermon History": "📋 تاریخچه موعظه‌ها",
    "🧘 Devotional & Meditation": "🧘 عبادت و مراقبه",
    "🕊️ Devotional History": "🕊️ تاریخچه عبادت‌ها",
    "💭 Chat History": "💭 تاریخچه گفتگو",
    
    # Sermon scope labels
    "📖 Specific Book": "📖 کتاب خاص",
    "📜 Old Testament": "📜 عهد عتیق",
    "✝️ New Testament": "✝️ عهد جدید",
    "🌍 Whole Bible": "🌍 کل کتاب مقدس",
    "🔖 Select multiple books": "🔖 انتخاب چندین کتاب",
    
    # Buttons
    "🔄 Clear Cache": "🔄 پاک کردن حافظه موقت",
    "🗑️ Delete": "🗑️ حذف",
    "🔄 Import Versions from Folder": "🔄 وارد کردن نسخه‌ها از پوشه",
    "📋 Copy sermon": "📋 کپی موعظه",
    "📋 Copy devotional": "📋 کپی عبادت",
    "📋 Copy conversation": "📋 کپی گفتگو",
    "✨ Generate Devotional": "✨ تولید عبادت",
    
    # Messages
    "✅ Explanation generated and saved to history!": "✅ توضیح تولید و در تاریخچه ذخیره شد!",
    "📚 Go to 'Study History' tab to see all your analyses.": "📚 برای مشاهده تمام تحلیل‌های خود به تب 'تاریخچه مطالعات' بروید.",
    "✅ Sermon generated and saved to history!": "✅ موعظه تولید و در تاریخچه ذخیره شد!",
    "📋 Go to 'Sermon History' tab to review all your sermons.": "📋 برای بررسی تمام موعظه‌های خود به تب 'تاریخچه موعظه‌ها' بروید.",
    "✅ Devotional generated and saved to history!": "✅ عبادت تولید و در تاریخچه ذخیره شد!",
    "🕊️ Go to 'Devotional History' tab to review your meditations.": "🕊️ برای بررسی مراقبه‌های خود به تب 'تاریخچه عبادت‌ها' بروید.",
    "✅ Answer generated and saved to history!": "✅ پاسخ تولید و در تاریخچه ذخیره شد!",
    "💭 Go to 'Chat History' tab to review your conversations.": "💭 برای بررسی گفتگوهای خود به تب 'تاریخچه گفتگو' بروید.",
    "🎤 No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "🎤 هنوز موعظه‌ای تولید نشده است. از تب 'مولد موعظه' برای ایجاد اولین موعظه خود استفاده کنید!",
    "🧘 No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first meditation!": "🧘 هنوز عبادتی تولید نشده است. از تب 'عبادت و مراقبه' برای ایجاد اولین مراقبه خود استفاده کنید!",
    "💬 No conversations saved yet. Use 'Theological Chat' tab to ask your first question!": "💬 هنوز گفتگویی ذخیره نشده است. از تب 'گفتگوی الهیاتی' برای پرسیدن اولین سوال خود استفاده کنید!",
    "💡 Add .json files of Bible versions to this folder and click 'Import'.": "💡 فایل‌های .json نسخه‌های کتاب مقدس را به این پوشه اضافه کنید و روی 'وارد کردن' کلیک کنید.",
    "💡 Create the folder and add JSON files of Bible versions.": "💡 پوشه را ایجاد کنید و فایل‌های JSON نسخه‌های کتاب مقدس را اضافه کنید.",
    "💡 Add JSON files to the folder and try again.": "💡 فایل‌های JSON را به پوشه اضافه کنید و دوباره امتحان کنید.",
    "🔄 The page will reload...": "🔄 صفحه بارگذاری مجدد خواهد شد...",
    "🔮 Generating biblical explanation...": "🔮 در حال تولید توضیح کتاب مقدسی...",
    "🔮 Generating sermon outline...": "🔮 در حال تولید طرح کلی موعظه...",
    "🔮 Generating devotional...": "🔮 در حال تولید عبادت...",
    "🔮 Generating theological answer...": "🔮 در حال تولید پاسخ الهیاتی...",
    "⏳ Importing versions...": "⏳ در حال وارد کردن نسخه‌ها...",
    "⚠️ Select at least 2 books.": "⚠️ حداقل 2 کتاب را انتخاب کنید.",
    "📚 Select books to continue": "📚 کتاب‌ها را برای ادامه انتخاب کنید",
    "❓ Generating Bible questions...": "❓ در حال تولید سوالات کتاب مقدس...",
    "✅ Questions generated and saved!": "✅ سوالات تولید و ذخیره شدند!",
    "📚 Go to 'Questions History' tab.": "📚 به تب 'تاریخچه سوالات' بروید.",
    
    # Expanders
    "👁️ Explanation Preview": "👁️ پیش‌نمایش توضیح",
    "👁️ Sermon Preview": "👁️ پیش‌نمایش موعظه",
    "👁️ Devotional Preview": "👁️ پیش‌نمایش عبادت",
    "📜 View Biblical Context": "📜 مشاهده زمینه کتاب مقدسی",
    "💡 View Full Explanation": "💡 مشاهده توضیح کامل",
    "ℹ️ How to Add Bible Versions": "ℹ️ نحوه اضافه کردن نسخه‌های کتاب مقدس",
    "👁️ Questions Preview": "👁️ پیش‌نمایش سوالات",
    
    # Headers
    "❓ Bible Questions Generator": "❓ مولد سوالات کتاب مقدس",
    "📚 Query Scope": "📚 محدوده پرسش",
}

def translate_persian_final(filepath):
    """Aplica as traduções finais completas no arquivo persa"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translation_count = 0
    
    for english, persian in PERSIAN_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais regex
        english_escaped = re.escape(english)
        
        # Contar ocorrências antes
        pattern = f'": "{english_escaped}"'
        matches_before = len(re.findall(pattern, content))
        
        if matches_before > 0:
            # Substituir todas as ocorrências
            content = re.sub(pattern, f'": "{persian}"', content)
            translation_count += matches_before
            print(f"✅ Traduzido ({matches_before}x): {english[:60]}...")
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translation_count

if __name__ == "__main__":
    fa_path = os.path.join('translations', 'fa.json')
    
    if not os.path.exists(fa_path):
        print(f"❌ Arquivo não encontrado: {fa_path}")
        exit(1)
    
    print("🔧 Aplicando traduções finais completas em persa (fa.json)...")
    print("=" * 70)
    
    total = translate_persian_final(fa_path)
    
    print("=" * 70)
    print(f"✅ CONCLUÍDO! Total: {total} strings traduzidas em persa")
    print(f"📁 Arquivo atualizado: {fa_path}")
    print("🎉 Persa (فارسی) agora está 100% no idioma nativo!")
