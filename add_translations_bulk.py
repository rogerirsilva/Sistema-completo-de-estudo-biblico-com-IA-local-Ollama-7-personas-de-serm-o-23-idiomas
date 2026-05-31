#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar traduções faltantes em todos os idiomas
"""

import json
import os

# Definir todas as traduções para cada idioma
TRANSLATIONS = {
    "de": {  # Alemão
        "headers": {
            "questions_generator": "❓ Bibelfragen-Generator",
            "chat_scope": "📚 Abfragebereich"
        },
        "labels": {
            "specific_book": "Bestimmtes Buch",
            "multiple_books": "Mehrere Bücher",
            "entire_bible": "Gesamte Bibel",
            "scope": "Bereich",
            "selected_book_colon": "Ausgewähltes Buch:",
            "select_books": "Bücher auswählen",
            "selected_books_colon": "Ausgewählte Bücher:",
            "scope_colon": "Bereich:",
            "questions_count": "Anzahl der Fragen",
            "questions_count_help": "Anzahl der zu generierenden Fragen",
            "with_answers": "Mit Antworten",
            "only_questions": "Nur Fragen",
            "generation_mode": "Generierungsmodus",
            "filter_by_mode": "Nach Modus filtern",
            "all": "Alle",
            "search": "🔍 Suchen",
            "search_placeholder_general": "Zum Suchen eingeben..."
        },
        "messages": {
            "select_at_least_two_books": "⚠️ Wählen Sie mindestens 2 Bücher aus.",
            "select_books_to_continue": "📚 Wählen Sie Bücher aus",
            "select_valid_scope": "Bitte wählen Sie einen gültigen Bereich aus.",
            "generating_questions": "❓ Bibelfragen generieren...",
            "questions_generated": "✅ Fragen generiert und gespeichert!",
            "check_questions_history": "📚 Gehen Sie zur Registerkarte 'Fragenverlauf'.",
            "no_questions_history": "Noch keine Fragen generiert."
        },
        "captions": {
            "questions_description": "Generieren Sie Fragen über biblisches Wissen.",
            "questions_history_description": "Alle generierten Fragen werden hier gespeichert.",
            "questions_found": "❓ {count} Fragenset(s) gefunden"
        },
        "expanders": {
            "questions_preview": "👁️ Fragenvorschau"
        }
    },
    
    "fr": {  # Francês
        "headers": {
            "questions_generator": "❓ Générateur de Questions Bibliques",
            "chat_scope": "📚 Portée de la Requête"
        },
        "labels": {
            "specific_book": "Livre Spécifique",
            "multiple_books": "Plusieurs Livres",
            "entire_bible": "Bible Entière",
            "scope": "Portée",
            "selected_book_colon": "Livre sélectionné :",
            "select_books": "Sélectionner les livres",
            "selected_books_colon": "Livres sélectionnés :",
            "scope_colon": "Portée :",
            "questions_count": "Nombre de questions",
            "questions_count_help": "Nombre de questions à générer",
            "with_answers": "Avec Réponses",
            "only_questions": "Questions Seulement",
            "generation_mode": "Mode de Génération",
            "filter_by_mode": "Filtrer par mode",
            "all": "Tous",
            "search": "🔍 Rechercher",
            "search_placeholder_general": "Tapez pour rechercher..."
        },
        "messages": {
            "select_at_least_two_books": "⚠️ Sélectionnez au moins 2 livres.",
            "select_books_to_continue": "📚 Sélectionnez les livres",
            "select_valid_scope": "Veuillez sélectionner une portée valide.",
            "generating_questions": "❓ Génération de questions bibliques...",
            "questions_generated": "✅ Questions générées et enregistrées !",
            "check_questions_history": "📚 Accédez à l'onglet 'Historique des Questions'.",
            "no_questions_history": "Aucune question générée."
        },
        "captions": {
            "questions_description": "Générez des questions sur les connaissances bibliques.",
            "questions_history_description": "Toutes les questions générées sont enregistrées ici.",
            "questions_found": "❓ {count} ensemble(s) de questions"
        },
        "expanders": {
            "questions_preview": "👁️ Aperçu des Questions"
        }
    },
    
    "ru": {  # Russo
        "headers": {
            "questions_generator": "❓ Генератор библейских вопросов",
            "chat_scope": "📚 Область запроса"
        },
        "labels": {
            "specific_book": "Конкретная книга",
            "multiple_books": "Несколько книг",
            "entire_bible": "Вся Библия",
            "scope": "Область",
            "selected_book_colon": "Выбранная книга:",
            "select_books": "Выбрать книги",
            "selected_books_colon": "Выбранные книги:",
            "scope_colon": "Область:",
            "questions_count": "Количество вопросов",
            "questions_count_help": "Количество вопросов для генерации",
            "with_answers": "С ответами",
            "only_questions": "Только вопросы",
            "generation_mode": "Режим генерации",
            "filter_by_mode": "Фильтр по режиму",
            "all": "Все",
            "search": "🔍 Поиск",
            "search_placeholder_general": "Введите для поиска..."
        },
        "messages": {
            "select_at_least_two_books": "⚠️ Выберите не менее 2 книг.",
            "select_books_to_continue": "📚 Выберите книги",
            "select_valid_scope": "Пожалуйста, выберите действительную область.",
            "generating_questions": "❓ Генерация библейских вопросов...",
            "questions_generated": "✅ Вопросы сгенерированы и сохранены!",
            "check_questions_history": "📚 Перейдите во вкладку 'История вопросов'.",
            "no_questions_history": "Вопросы еще не сгенерированы."
        },
        "captions": {
            "questions_description": "Генерируйте вопросы о библейских знаниях.",
            "questions_history_description": "Все сгенерированные вопросы сохраняются здесь.",
            "questions_found": "❓ Найдено {count} набор(ов) вопросов"
        },
        "expanders": {
            "questions_preview": "👁️ Предварительный просмотр вопросов"
        }
    },
    
    "zh": {  # Chinês
        "headers": {
            "questions_generator": "❓ 圣经问题生成器",
            "chat_scope": "📚 查询范围"
        },
        "labels": {
            "specific_book": "特定书卷",
            "multiple_books": "多本书卷",
            "entire_bible": "整本圣经",
            "scope": "范围",
            "selected_book_colon": "选定的书卷：",
            "select_books": "选择书卷",
            "selected_books_colon": "选定的书卷：",
            "scope_colon": "范围：",
            "questions_count": "问题数量",
            "questions_count_help": "要生成的问题数量",
            "with_answers": "带答案",
            "only_questions": "仅问题",
            "generation_mode": "生成模式",
            "filter_by_mode": "按模式筛选",
            "all": "全部",
            "search": "🔍 搜索",
            "search_placeholder_general": "输入搜索..."
        },
        "messages": {
            "select_at_least_two_books": "⚠️ 至少选择2本书。",
            "select_books_to_continue": "📚 选择书卷继续",
            "select_valid_scope": "请选择有效的范围。",
            "generating_questions": "❓ 生成圣经问题...",
            "questions_generated": "✅ 问题已生成并保存！",
            "check_questions_history": "📚 转到问题历史选项卡。",
            "no_questions_history": "尚未生成问题。"
        },
        "captions": {
            "questions_description": "生成关于圣经知识的问题。",
            "questions_history_description": "所有生成的问题都自动保存在这里。",
            "questions_found": "❓ 找到 {count} 个问题集"
        },
        "expanders": {
            "questions_preview": "👁️ 问题预览"
        }
    },
    
    "ja": {  # Japonês
        "headers": {
            "questions_generator": "❓ 聖書質問ジェネレーター",
            "chat_scope": "📚 クエリ範囲"
        },
        "labels": {
            "specific_book": "特定の書",
            "multiple_books": "複数の書",
            "entire_bible": "聖書全体",
            "scope": "範囲",
            "selected_book_colon": "選択した書：",
            "select_books": "書を選択",
            "selected_books_colon": "選択した書：",
            "scope_colon": "範囲：",
            "questions_count": "質問数",
            "questions_count_help": "生成する質問の数",
            "with_answers": "回答付き",
            "only_questions": "質問のみ",
            "generation_mode": "生成モード",
            "filter_by_mode": "モードで絞り込み",
            "all": "すべて",
            "search": "🔍 検索",
            "search_placeholder_general": "検索するには入力..."
        },
        "messages": {
            "select_at_least_two_books": "⚠️ 少なくとも2つの書を選択してください。",
            "select_books_to_continue": "📚 書を選択して続行",
            "select_valid_scope": "有効な範囲を選択してください。",
            "generating_questions": "❓ 聖書の質問を生成中...",
            "questions_generated": "✅ 質問が生成され、保存されました！",
            "check_questions_history": "📚 質問履歴タブに移動します。",
            "no_questions_history": "まだ質問は生成されていません。"
        },
        "captions": {
            "questions_description": "聖書の知識に関する質問を生成します。",
            "questions_history_description": "生成されたすべての質問はここに自動保存されます。",
            "questions_found": "❓ {count} 件の質問セットが見つかりました"
        },
        "expanders": {
            "questions_preview": "👁️ 質問のプレビュー"
        }
    },
    
    # Adicionar idiomas restantes com traduções básicas em inglês
    "ko": {  # Coreano
        "headers": {"questions_generator": "❓ 성경 질문 생성기", "chat_scope": "📚 쿼리 범위"},
        "labels": {"specific_book": "특정 책", "multiple_books": "여러 책", "entire_bible": "전체 성경", "scope": "범위", "selected_book_colon": "선택한 책:", "select_books": "책 선택", "selected_books_colon": "선택한 책:", "scope_colon": "범위:", "questions_count": "질문 수", "questions_count_help": "생성할 질문 수", "with_answers": "답변 포함", "only_questions": "질문만", "generation_mode": "생성 모드", "filter_by_mode": "모드별 필터", "all": "모두", "search": "🔍 검색", "search_placeholder_general": "검색하려면 입력..."},
        "messages": {"select_at_least_two_books": "⚠️ 최소 2개의 책을 선택하세요.", "select_books_to_continue": "📚 계속하려면 책을 선택하세요", "select_valid_scope": "유효한 범위를 선택하세요.", "generating_questions": "❓ 성경 질문 생성 중...", "questions_generated": "✅ 질문이 생성되고 저장되었습니다!", "check_questions_history": "📚 '질문 기록' 탭으로 이동합니다.", "no_questions_history": "아직 질문이 생성되지 않았습니다."},
        "captions": {"questions_description": "성경 지식에 대한 질문을 생성합니다.", "questions_history_description": "생성된 모든 질문이 여기에 자동 저장됩니다.", "questions_found": "❓ {count}개의 질문 세트를 찾았습니다"},
        "expanders": {"questions_preview": "👁️ 질문 미리보기"}
    },
    
    # Outros idiomas com traduções similares
    "it": {"headers": {"questions_generator": "❓ Generatore di Domande Bibliche", "chat_scope": "📚 Ambito della Query"}, "labels": {"specific_book": "Libro Specifico", "multiple_books": "Libri Multipli", "entire_bible": "Bibbia Intera", "scope": "Ambito", "selected_book_colon": "Libro selezionato:", "select_books": "Seleziona libri", "selected_books_colon": "Libri selezionati:", "scope_colon": "Ambito:", "questions_count": "Numero di domande", "questions_count_help": "Numero di domande da generare", "with_answers": "Con Risposte", "only_questions": "Solo Domande", "generation_mode": "Modalità di Generazione", "filter_by_mode": "Filtra per modalità", "all": "Tutti", "search": "🔍 Cerca", "search_placeholder_general": "Digita per cercare..."}, "messages": {"select_at_least_two_books": "⚠️ Seleziona almeno 2 libri.", "select_books_to_continue": "📚 Seleziona libri", "select_valid_scope": "Si prega di selezionare un ambito valido.", "generating_questions": "❓ Generazione di domande bibliche...", "questions_generated": "✅ Domande generate e salvate!", "check_questions_history": "📚 Vai alla scheda 'Cronologia Domande'.", "no_questions_history": "Nessuna domanda generata ancora."}, "captions": {"questions_description": "Genera domande sulla conoscenza biblica.", "questions_history_description": "Tutte le domande generate vengono salvate qui automaticamente.", "questions_found": "❓ Trovati {count} set di domande"}, "expanders": {"questions_preview": "👁️ Anteprima Domande"}},
    
    "el": {"headers": {"questions_generator": "❓ Γεννήτρια Βιβλικών Ερωτήσεων", "chat_scope": "📚 Πεδίο Ερωτήματος"}, "labels": {"specific_book": "Συγκεκριμένο Βιβλίο", "multiple_books": "Πολλαπλά Βιβλία", "entire_bible": "Ολόκληρη η Βίβλος", "scope": "Πεδίο", "selected_book_colon": "Επιλεγμένο βιβλίο:", "select_books": "Επιλέξτε βιβλία", "selected_books_colon": "Επιλεγμένα βιβλία:", "scope_colon": "Πεδίο:", "questions_count": "Αριθμός ερωτήσεων", "questions_count_help": "Αριθμός ερωτήσεων προς δημιουργία", "with_answers": "Με Απαντήσεις", "only_questions": "Μόνο Ερωτήσεις", "generation_mode": "Λειτουργία Δημιουργίας", "filter_by_mode": "Φιλτράρισμα κατά λειτουργία", "all": "Όλα", "search": "🔍 Αναζήτηση", "search_placeholder_general": "Πληκτρολογήστε για αναζήτηση..."}, "messages": {"select_at_least_two_books": "⚠️ Επιλέξτε τουλάχιστον 2 βιβλία.", "select_books_to_continue": "📚 Επιλέξτε βιβλία", "select_valid_scope": "Παρακαλώ επιλέξτε έγκυρο πεδίο.", "generating_questions": "❓ Δημιουργία βιβλικών ερωτήσεων...", "questions_generated": "✅ Οι ερωτήσεις δημιουργήθηκαν και αποθηκεύτηκαν!", "check_questions_history": "📚 Μεταβείτε στην καρτέλα 'Ιστορικό Ερωτήσεων'.", "no_questions_history": "Δεν έχουν δημιουργηθεί ερωτήσεις ακόμα."}, "captions": {"questions_description": "Δημιουργήστε ερωτήσεις για βιβλικές γνώσεις.", "questions_history_description": "Όλες οι ερωτήσεις αποθηκεύονται αυτόματα εδώ.", "questions_found": "❓ Βρέθηκαν {count} σύνολα ερωτήσεων"}, "expanders": {"questions_preview": "👁️ Προεπισκόπηση Ερωτήσεων"}},
}

# Idiomas faltantes (usar inglês como fallback)
FALLBACK_LANGS = ["eo", "fa", "fi", "hi", "id", "pl", "ro", "sw", "th", "tr", "vi"]

# Tradução em inglês para fallback
EN_FALLBACK = {
    "headers": {"questions_generator": "❓ Bible Questions Generator", "chat_scope": "📚 Query Scope"},
    "labels": {"specific_book": "Specific Book", "multiple_books": "Multiple Books", "entire_bible": "Entire Bible", "scope": "Scope", "selected_book_colon": "Selected book:", "select_books": "Select books", "selected_books_colon": "Selected books:", "scope_colon": "Scope:", "questions_count": "Number of questions", "questions_count_help": "Number of questions to generate", "with_answers": "With Answers", "only_questions": "Questions Only", "generation_mode": "Generation Mode", "filter_by_mode": "Filter by mode", "all": "All", "search": "🔍 Search", "search_placeholder_general": "Type to search..."},
    "messages": {"select_at_least_two_books": "⚠️ Select at least 2 books.", "select_books_to_continue": "📚 Select books to continue", "select_valid_scope": "Please select a valid scope.", "generating_questions": "❓ Generating Bible questions...", "questions_generated": "✅ Questions generated and saved!", "check_questions_history": "📚 Go to 'Questions History' tab.", "no_questions_history": "No questions generated yet."},
    "captions": {"questions_description": "Generate questions about biblical knowledge.", "questions_history_description": "All generated questions are automatically saved here.", "questions_found": "❓ {count} question set(s) found"},
    "expanders": {"questions_preview": "👁️ Questions Preview"}
}

# Adicionar fallback para idiomas faltantes
for lang in FALLBACK_LANGS:
    TRANSLATIONS[lang] = EN_FALLBACK

def add_translations_to_file(filepath, translations):
    """Adiciona traduções ao arquivo JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Adicionar traduções em cada seção
        for section, items in translations.items():
            if section not in data:
                data[section] = {}
            data[section].update(items)
        
        # Salvar de volta
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")
        return False

def main():
    translations_dir = "translations"
    
    print("🌍 Adicionando traduções em todos os idiomas...")
    print()
    
    success_count = 0
    for lang_code, translations in TRANSLATIONS.items():
        filepath = os.path.join(translations_dir, f"{lang_code}.json")
        if os.path.exists(filepath):
            if add_translations_to_file(filepath, translations):
                print(f"✅ {lang_code}.json atualizado")
                success_count += 1
            else:
                print(f"❌ Erro ao atualizar {lang_code}.json")
        else:
            print(f"⚠️  {lang_code}.json não encontrado")
    
    print()
    print(f"🎉 {success_count}/{len(TRANSLATIONS)} arquivos atualizados com sucesso!")

if __name__ == "__main__":
    main()
