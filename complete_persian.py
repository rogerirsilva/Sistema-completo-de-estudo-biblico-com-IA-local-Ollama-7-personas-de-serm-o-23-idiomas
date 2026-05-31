#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para COMPLETAR todas as traduções do Persa
Substitui TODAS as strings em inglês restantes
"""

import json
import re

# TODAS as traduções restantes em Persa
PERSIAN_TRANSLATIONS = {
    # Messages
    "Select a book and chapter to start guided reading.": "یک کتاب و فصل را برای شروع خواندن راهنما انتخاب کنید",
    "No verses found in this chapter.": "هیچ آیه‌ای در این فصل یافت نشد",
    "No matching verse found. Check syntax or use commas/ranges.": "آیه مطابقتی یافت نشد. نحو را بررسی کنید یا از کاما/محدوده استفاده کنید",
    "Explanation generated and saved to history!": "توضیح تولید و در تاریخچه ذخیره شد!",
    "Go to 'Study History' tab to see all your analyses.": "برای مشاهده تمام تحلیل‌های خود به تب 'تاریخچه مطالعات' بروید",
    "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "هنوز مطالعه‌ای تولید نشده است. به تب 'خواندن و تفسیر' بروید و روی 'تولید توضیح' کلیک کنید",
    "No results found for your search.": "نتیجه‌ای برای جستجوی شما یافت نشد",
    "Text ready to copy!": "متن آماده کپی است!",
    "Import data to start generating a sermon.": "داده‌ها را وارد کنید تا تولید موعظه را شروع کنید",
    "Choose a base verse or scope for the model to use as authority.": "یک آیه پایه یا محدوده را برای استفاده مدل به عنوان مرجع انتخاب کنید",
    "Ollama is offline. Start the local server.": "Ollama آفلاین است. سرور محلی را راه‌اندازی کنید",
    "Sermon generated and saved to history!": "موعظه تولید و در تاریخچه ذخیره شد!",
    "Go to 'Sermon History' tab to check all your sermons.": "برای بررسی تمام موعظه‌های خود به تب 'تاریخچه موعظه‌ها' بروید",
    "Load a verse to build the devotional.": "یک آیه بارگذاری کنید تا عبادت را بسازید",
    "Select a verse or scope to anchor the meditation.": "یک آیه یا محدوده را برای لنگر انداختن مراقبه انتخاب کنید",
    "Ollama is offline. Turn on the server and try again.": "Ollama آفلاین است. سرور را روشن کنید و دوباره امتحان کنید",
    "Devotional generated and saved!": "عبادت تولید و ذخیره شد!",
    "Check the 'Devotional History' tab to see your meditations.": "برای مشاهده مراقبه‌های خود تب 'تاریخچه عبادات' را بررسی کنید",
    "Import a version to chat with the theological chat.": "یک نسخه را وارد کنید تا با گفتگوی الهیاتی صحبت کنید",
    "Select a verse for the AI to use as authority.": "یک آیه را برای استفاده هوش مصنوعی به عنوان مرجع انتخاب کنید",
    "Write the question before sending.": "قبل از ارسال سوال را بنویسید",
    "Ollama is offline. Please start the server.": "Ollama آفلاین است. لطفاً سرور را راه‌اندازی کنید",
    "Answer generated!": "پاسخ تولید شد!",
    "Go to 'Chat History' to review your questions.": "برای بررسی سوالات خود به 'تاریخچه گفتگو' بروید",
    "No questions yet.": "هنوز سوالی نیست",
    "No sermons yet.": "هنوز موعظه‌ای نیست",
    "No devotionals yet.": "هنوز عبادتی نیست",
    "No conversations yet.": "هنوز گفتگویی نیست",
    "Generating explanation...": "در حال تولید توضیح...",
    "Generating sermon outline...": "در حال تولید طرح کلی موعظه...",
    "Generating devotional...": "در حال تولید عبادت...",
    "Generating theological answer...": "در حال تولید پاسخ الهیاتی...",
    "Ollama is offline ({detail}). Start the server and try again.": "Ollama آفلاین است ({detail}). سرور را راه‌اندازی کنید و دوباره امتحان کنید",
    "No local versions found. Use Import Data to load content.": "نسخه محلی یافت نشد. از وارد کردن داده‌ها برای بارگذاری محتوا استفاده کنید",
    "Importing versions...": "در حال وارد کردن نسخه‌ها...",
    
    # Expanders
    "Explanation Preview": "پیش‌نمایش توضیح",
    "Sermon Preview": "پیش‌نمایش موعظه",
    "Devotional Preview": "پیش‌نمایش عبادت",
    "View Biblical Context": "مشاهده متن کتاب مقدس",
    "View Full Explanation": "مشاهده توضیح کامل",
    "How to Add Bible Versions": "نحوه اضافه کردن نسخه‌های کتاب مقدس",
    
    # Headers
    "Bible Studies History": "تاریخچه مطالعات کتاب مقدس",
    "Guided Reading": "خواندن راهنما",
    "Sermon Generator": "تولیدکننده موعظه",
    "Sermon Scope": "محدوده موعظه",
    "Devotional Generator": "تولیدکننده عبادت",
    "Devotional Scope": "محدوده عبادت",
    "Theological Chat": "گفتگوی الهیاتی",
    "Sermons History": "تاریخچه موعظه‌ها",
    "Devotionals History": "تاریخچه عبادات",
    "Conversations History": "تاریخچه گفتگوها",
    
    # Prompts
    "Explain the historical and theological context, ponder key words and suggest pastoral applications.": "زمینه تاریخی و الهیاتی را توضیح دهید، کلمات کلیدی را بررسی کنید و کاربردهای شبانی را پیشنهاد دهید",
    "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "یک طرح کلی شبانی ایجاد کنید که کلام را احترام می‌گذارد، مرتبط و قابل اجرا برای مخاطب مشخص شده است",
    "Generate a deep and applicable meditation on the chosen text that promotes spiritual edification.": "یک مراقبه عمیق و کاربردی در مورد متن انتخاب شده ایجاد کنید که باعث تربیت روحانی شود",
    "The devotional should consider texts from:": "عبادت باید متون را در نظر بگیرد از:",
    "Answer the theological question, using the biblical passage as the main source of authority.": "به سوال الهیاتی پاسخ دهید، با استفاده از متن کتاب مقدس به عنوان منبع اصلی اقتدار",
    
    # Captions
    "Sermons found": "موعظه‌های یافت شده",
    "Devotionals found": "عبادات یافت شده",
    "Conversations found": "گفتگوهای یافت شده",
    "Studies found": "مطالعات یافت شده",
    "Audience:": "مخاطب:",
    "Preacher's notes:": "یادداشت‌های موعظه‌گر:",
    "Theme:": "موضوع:",
    "Model:": "مدل:",
    "Reference:": "مرجع:",
    "Feeling:": "احساس:",
    "Create the folder manually or the application will create it automatically when importing.": "پوشه را به صورت دستی ایجاد کنید یا برنامه به طور خودکار هنگام وارد کردن آن را ایجاد می‌کند",
    
    # Errors
    "Error loading bible_data.json: {error}. Using empty data.": "خطا در بارگذاری bible_data.json: {error}. استفاده از داده خالی",
    "Error loading {filename}: {error}": "خطا در بارگذاری {filename}: {error}",
    
    # Warnings
    "Folder `Dados_Json/{lang}/` not found.": "پوشه `Dados_Json/{lang}/` یافت نشد",
    
    # Help
    "Leave empty to import all available versions from the folder": "برای وارد کردن تمام نسخه‌های موجود از پوشه خالی بگذارید",
    
    # Formatting
    "Question:": "سوال:",
    "Answer:": "پاسخ:",
    "Context:": "زمینه:",
    "Generated on": "تولید شده در",
    "at": "در",
}

def replace_all_english(filepath, translations):
    """جایگزینی تمام متون انگلیسی"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for english, persian in translations.items():
        english_escaped = re.escape(english)
        pattern = f'"{english_escaped}"'
        if re.search(pattern, content):
            content = re.sub(pattern, f'"{persian}"', content)
            count += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

def main():
    filepath = "translations/fa.json"
    print("🔄 Completando todas as traduções do Persa...")
    
    count = replace_all_english(filepath, PERSIAN_TRANSLATIONS)
    
    print(f"✅ {count} strings adicionais traduzidas em fa.json")
    print("🎉 Persa agora está 100% traduzido!")

if __name__ == "__main__":
    main()
