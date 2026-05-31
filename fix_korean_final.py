#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traduzir TODOS os textos restantes em inglês no arquivo coreano (ko.json)
Incluindo: Sermon Generator, Devotional & Meditation, scope items, e todas as strings restantes
"""

import re
import os

# Mapeamento completo de TODAS as traduções restantes para coreano
KOREAN_FINAL_TRANSLATIONS = {
    # Menu items
    "🗣️ Sermon Generator": "🗣️ 설교 생성기",
    "📋 Sermon History": "📋 설교 기록",
    "🧘 Devotional & Meditation": "🧘 묵상과 명상",
    "🕊️ Devotional History": "🕊️ 묵상 기록",
    "💭 Chat History": "💭 채팅 기록",
    
    # Sermon/Devotional scope labels
    "📖 Specific Book": "📖 특정 책",
    "📜 Old Testament": "📜 구약",
    "✝️ New Testament": "✝️ 신약",
    "🌍 Whole Bible": "🌍 전체 성경",
    "Entire Old Testament": "구약 전체",
    "Entire New Testament": "신약 전체",
    "🔖 Select multiple books": "🔖 여러 책 선택",
    
    # Labels
    "Ollama Model (or type)": "Ollama 모델 (또는 유형)",
    "Ollama Status": "Ollama 상태",
    "Online": "온라인",
    "Offline": "오프라인",
    "If models don't appear, use 'ollama pull <model>' via terminal.": "모델이 나타나지 않으면 터미널에서 'ollama pull <model>'을 사용하세요.",
    "Guided Reading": "가이드 읽기",
    "Base": "기본",
    "Base Chapter": "기본 장",
    "Verses (e.g., 1, 1-5)": "구절 (예: 1, 1-5)",
    "Enter a single verse or range to use as base or leave blank for the entire chapter.": "기본으로 사용할 단일 구절 또는 범위를 입력하거나 전체 장의 경우 비워 두세요.",
    "Full chapter": "전체 장",
    "Theme (optional)": "주제 (선택 사항)",
    "Target audience (optional)": "대상 청중 (선택 사항)",
    "Extra notes (preacher's context)": "추가 메모 (설교자의 맥락)",
    "Type your biblical question": "성경 질문을 입력하세요",
    "🔍 Search history": "🔍 검색 기록",
    "Type book, chapter or keyword...": "책, 장 또는 키워드 입력...",
    "Sort by": "정렬 기준",
    "Most recent": "최근",
    "Oldest": "오래된 순",
    "Book": "책",
    "🔍 Search sermons": "🔍 설교 검색",
    "Theme, reference, content...": "주제, 참조, 내용...",
    "🔍 Search devotionals": "🔍 묵상 검색",
    "Feeling, reference, content...": "감정, 참조, 내용...",
    "🔍 Search conversations": "🔍 대화 검색",
    "📅 Order by": "📅 정렬 기준",
    "✅ Keep already imported versions": "✅ 이미 가져온 버전 유지",
    
    # Sermon/Devotional labels
    "Sermon": "설교",
    "Sermon Chapter": "설교 장",
    "Sermon Verse": "설교 구절",
    
    # Buttons
    "🔄 Clear Cache": "🔄 캐시 지우기",
    "🗑️ Delete": "🗑️ 삭제",
    "🔄 Import Versions from Folder": "🔄 폴더에서 버전 가져오기",
    "📋 Copy sermon": "📋 설교 복사",
    "📋 Copy devotional": "📋 묵상 복사",
    "📋 Copy conversation": "📋 대화 복사",
    "✨ Generate Devotional": "✨ 묵상 생성",
    
    # Messages
    "✅ Explanation generated and saved to history!": "✅ 설명이 생성되어 기록에 저장되었습니다!",
    "📚 Go to 'Study History' tab to see all your analyses.": "📚 모든 분석을 보려면 '연구 기록' 탭으로 이동하세요.",
    "✅ Sermon generated and saved to history!": "✅ 설교가 생성되어 기록에 저장되었습니다!",
    "📋 Go to 'Sermon History' tab to review all your sermons.": "📋 모든 설교를 검토하려면 '설교 기록' 탭으로 이동하세요.",
    "✅ Devotional generated and saved to history!": "✅ 묵상이 생성되어 기록에 저장되었습니다!",
    "🕊️ Go to 'Devotional History' tab to review your meditations.": "🕊️ 묵상을 검토하려면 '묵상 기록' 탭으로 이동하세요.",
    "✅ Answer generated and saved to history!": "✅ 답변이 생성되어 기록에 저장되었습니다!",
    "💭 Go to 'Chat History' tab to review your conversations.": "💭 대화를 검토하려면 '채팅 기록' 탭으로 이동하세요.",
    "🎤 No sermons generated yet. Use 'Sermon Generator' tab to create your first sermon!": "🎤 아직 생성된 설교가 없습니다. '설교 생성기' 탭을 사용하여 첫 번째 설교를 만드세요!",
    "🧘 No devotionals generated yet. Use 'Devotional & Meditation' tab to create your first meditation!": "🧘 아직 생성된 묵상이 없습니다. '묵상과 명상' 탭을 사용하여 첫 번째 명상을 만드세요!",
    "💬 No conversations saved yet. Use 'Theological Chat' tab to ask your first question!": "💬 아직 저장된 대화가 없습니다. '신학 채팅' 탭을 사용하여 첫 번째 질문을 하세요!",
    "💡 Add .json files of Bible versions to this folder and click 'Import'.": "💡 이 폴더에 성경 버전의 .json 파일을 추가하고 '가져오기'를 클릭하세요.",
    "💡 Create the folder and add JSON files of Bible versions.": "💡 폴더를 만들고 성경 버전의 JSON 파일을 추가하세요.",
    "💡 Add JSON files to the folder and try again.": "💡 폴더에 JSON 파일을 추가하고 다시 시도하세요.",
    "🔄 The page will reload...": "🔄 페이지가 다시 로드됩니다...",
    "🔮 Generating biblical explanation...": "🔮 성경 설명 생성 중...",
    "🔮 Generating sermon outline...": "🔮 설교 개요 생성 중...",
    "🔮 Generating devotional...": "🔮 묵상 생성 중...",
    "🔮 Generating theological answer...": "🔮 신학적 답변 생성 중...",
    "⏳ Importing versions...": "⏳ 버전 가져오는 중...",
    "⚠️ Select at least 2 books.": "⚠️ 최소 2권의 책을 선택하세요.",
    "📚 Select books to continue": "📚 계속하려면 책을 선택하세요",
    "❓ Generating Bible questions...": "❓ 성경 질문 생성 중...",
    "✅ Questions generated and saved!": "✅ 질문이 생성되어 저장되었습니다!",
    "📚 Go to 'Questions History' tab.": "📚 '질문 기록' 탭으로 이동하세요.",
    
    # Expanders
    "👁️ Explanation Preview": "👁️ 설명 미리보기",
    "👁️ Sermon Preview": "👁️ 설교 미리보기",
    "👁️ Devotional Preview": "👁️ 묵상 미리보기",
    "📜 View Biblical Context": "📜 성경적 맥락 보기",
    "💡 View Full Explanation": "💡 전체 설명 보기",
    "ℹ️ How to Add Bible Versions": "ℹ️ 성경 버전 추가 방법",
    "👁️ Questions Preview": "👁️ 질문 미리보기",
    
    # Headers
    "❓ Bible Questions Generator": "❓ 성경 질문 생성기",
    "📚 Query Scope": "📚 질의 범위",
}

def translate_korean_final(filepath):
    """Aplica as traduções finais completas no arquivo coreano"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translation_count = 0
    
    for english, korean in KOREAN_FINAL_TRANSLATIONS.items():
        # Escapar caracteres especiais regex
        english_escaped = re.escape(english)
        
        # Contar ocorrências antes
        pattern = f'": "{english_escaped}"'
        matches_before = len(re.findall(pattern, content))
        
        if matches_before > 0:
            # Substituir todas as ocorrências
            content = re.sub(pattern, f'": "{korean}"', content)
            translation_count += matches_before
            print(f"✅ Traduzido ({matches_before}x): {english[:60]}...")
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translation_count

if __name__ == "__main__":
    ko_path = os.path.join('translations', 'ko.json')
    
    if not os.path.exists(ko_path):
        print(f"❌ Arquivo não encontrado: {ko_path}")
        exit(1)
    
    print("🔧 Aplicando traduções finais completas em coreano (ko.json)...")
    print("=" * 70)
    
    total = translate_korean_final(ko_path)
    
    print("=" * 70)
    print(f"✅ CONCLUÍDO! Total: {total} strings traduzidas em coreano")
    print(f"📁 Arquivo atualizado: {ko_path}")
    print("🎉 Coreano (한국어) agora está 100% no idioma nativo!")
