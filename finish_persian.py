#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script FINAL para traduzir TODAS as strings restantes em Persa
"""

import json
import re

# Últimas strings faltando
FINAL_TRANSLATIONS = {
    "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "یک مراقبه شخصی بنویسید که آرامش روحانی، تأمل عمیق و کاربرد عملی ارائه دهد",
    "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "با وضوح الهیاتی و لطف شبانی پاسخ دهید، همیشه بر اساس اقتدار کتاب مقدس",
    "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "یک طرح کلی کامل موعظه با عنوان، مقدمه، موضوعات تفسیری، تصاویر و نتیجه‌گیری بنویسید",
    "The sermon should cover texts from:": "موعظه باید متون را پوشش دهد از:",
    "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "یک خواندن آرام، یک تأمل مختصر و یک دعای نهایی ایجاد کنید که احساس انتخاب شده را به متن کتاب مقدس متصل می‌کند",
    "Selected context:": "زمینه انتخاب شده:",
    "Explanation:": "توضیح:",
}

def replace_final_strings(filepath, translations):
    """جایگزینی نهایی تمام متون انگلیسی"""
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
    print("🔄 Traduzindo as ÚLTIMAS strings em inglês...")
    
    count = replace_final_strings(filepath, FINAL_TRANSLATIONS)
    
    print(f"✅ {count} strings finais traduzidas")
    print("🎉 Persa (فارسی) agora está COMPLETAMENTE traduzido!")

if __name__ == "__main__":
    main()
