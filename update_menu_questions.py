#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar traduções do menu de perguntas
"""

import json
import os

# Traduções para os menus
MENU_TRANSLATIONS = {
    "pt": {
        "questions_gen": "❓ Gerar Perguntas",
        "questions_hist": "📚 Histórico de Perguntas"
    },
    "en": {
        "questions_gen": "❓ Questions Generator",
        "questions_hist": "📚 Questions History"
    },
    "es": {
        "questions_gen": "❓ Generador de Preguntas",
        "questions_hist": "📚 Historial de Preguntas"
    },
    "ar": {
        "questions_gen": "❓ مولد الأسئلة",
        "questions_hist": "📚 سجل الأسئلة"
    },
    "de": {
        "questions_gen": "❓ Fragengenerator",
        "questions_hist": "📚 Fragenverlauf"
    },
    "fr": {
        "questions_gen": "❓ Générateur de Questions",
        "questions_hist": "📚 Historique des Questions"
    },
    "ru": {
        "questions_gen": "❓ Генератор Вопросов",
        "questions_hist": "📚 История Вопросов"
    },
    "zh": {
        "questions_gen": "❓ 问题生成器",
        "questions_hist": "📚 问题历史"
    },
    "ja": {
        "questions_gen": "❓ 質問ジェネレーター",
        "questions_hist": "📚 質問履歴"
    },
    "ko": {
        "questions_gen": "❓ 질문 생성기",
        "questions_hist": "📚 질문 기록"
    },
    "it": {
        "questions_gen": "❓ Generatore di Domande",
        "questions_hist": "📚 Cronologia Domande"
    },
    "el": {
        "questions_gen": "❓ Γεννήτρια Ερωτήσεων",
        "questions_hist": "📚 Ιστορικό Ερωτήσεων"
    },
    "hi": {
        "questions_gen": "❓ प्रश्न जनरेटर",
        "questions_hist": "📚 प्रश्न इतिहास"
    },
    "th": {
        "questions_gen": "❓ ตัวสร้างคำถาม",
        "questions_hist": "📚 ประวัติคำถาม"
    },
    "vi": {
        "questions_gen": "❓ Trình Tạo Câu Hỏi",
        "questions_hist": "📚 Lịch Sử Câu Hỏi"
    },
    "id": {
        "questions_gen": "❓ Generator Pertanyaan",
        "questions_hist": "📚 Riwayat Pertanyaan"
    },
    "tr": {
        "questions_gen": "❓ Soru Üretici",
        "questions_hist": "📚 Soru Geçmişi"
    },
    "pl": {
        "questions_gen": "❓ Generator Pytań",
        "questions_hist": "📚 Historia Pytań"
    },
    "ro": {
        "questions_gen": "❓ Generator de Întrebări",
        "questions_hist": "📚 Istoric Întrebări"
    },
    "sw": {
        "questions_gen": "❓ Kizalishi cha Maswali",
        "questions_hist": "📚 Historia ya Maswali"
    },
    "fa": {
        "questions_gen": "❓ تولیدکننده سوال",
        "questions_hist": "📚 تاریخچه سوالات"
    },
    "fi": {
        "questions_gen": "❓ Kysymysgeneraattori",
        "questions_hist": "📚 Kysymyshistoria"
    },
    "eo": {
        "questions_gen": "❓ Questions Generator",
        "questions_hist": "📚 Questions History"
    }
}

def update_menu_translations():
    translations_dir = "translations"
    updated_count = 0
    
    print("🔄 Atualizando traduções dos menus...")
    print()
    
    for lang_code, translations in MENU_TRANSLATIONS.items():
        filepath = os.path.join(translations_dir, f"{lang_code}.json")
        
        if not os.path.exists(filepath):
            print(f"⚠️  {lang_code}.json não encontrado")
            continue
            
        try:
            # Ler arquivo
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Garantir que a seção 'menu' existe
            if 'menu' not in data:
                data['menu'] = {}
            
            # Adicionar traduções
            data['menu']['questions_gen'] = translations['questions_gen']
            data['menu']['questions_hist'] = translations['questions_hist']
            
            # Salvar
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {lang_code}.json - Menu atualizado")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Erro ao processar {lang_code}.json: {e}")
    
    print()
    print(f"🎉 {updated_count}/{len(MENU_TRANSLATIONS)} arquivos atualizados!")

if __name__ == "__main__":
    update_menu_translations()
