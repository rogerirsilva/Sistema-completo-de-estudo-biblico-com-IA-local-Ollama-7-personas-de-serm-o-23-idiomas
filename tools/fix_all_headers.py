#!/usr/bin/env python3
"""Traduz TODOS os headers para 100% nativos em TODOS os 23 idiomas."""

import json
from pathlib import Path

# Traduções completas e nativas de headers para TODOS os idiomas
NATIVE_HEADERS = {
    "ar": {
        "bible_studies_history": "📚 تاريخ الدراسات الكتابية",
        "sermon_generator": "مولد العظات",
        "sermon_scope": "📚 نطاق العظة",
        "devotional_meditation": "التأمل والتفكر",
        "devotional_scope": "📚 نطاق التأمل",
        "theological_chat": "محادثة لاهوتية",
        "sermons_history": "📋 تاريخ العظات",
        "devotionals_history": "🕊️ تاريخ التأملات",
        "conversations_history": "💭 تاريخ المحادثات"
    },
    "de": {
        "bible_studies_history": "📚 Geschichte der Bibelstudien",
        "sermon_generator": "Predigtgenerator",
        "sermon_scope": "📚 Predigtbereich",
        "devotional_meditation": "Andacht und Meditation",
        "devotional_scope": "📚 Andachtsbereich",
        "theological_chat": "Theologischer Chat",
        "sermons_history": "📋 Predigthistorie",
        "devotionals_history": "🕊️ Andachtshistorie",
        "conversations_history": "💭 Gesprächshistorie"
    },
    "fr": {
        "bible_studies_history": "📚 Historique des Études Bibliques",
        "sermon_generator": "Générateur de Sermons",
        "sermon_scope": "📚 Portée du Sermon",
        "devotional_meditation": "Dévotion et Méditation",
        "devotional_scope": "📚 Portée de la Dévotion",
        "theological_chat": "Chat Théologique",
        "sermons_history": "📋 Historique des Sermons",
        "devotionals_history": "🕊️ Historique des Dévotions",
        "conversations_history": "💭 Historique des Conversations"
    },
    "it": {
        "bible_studies_history": "📚 Cronologia degli Studi Biblici",
        "sermon_generator": "Generatore di Sermoni",
        "sermon_scope": "📚 Ambito del Sermone",
        "devotional_meditation": "Devozionale e Meditazione",
        "devotional_scope": "📚 Ambito del Devozionale",
        "theological_chat": "Chat Teologica",
        "sermons_history": "📋 Cronologia dei Sermoni",
        "devotionals_history": "🕊️ Cronologia dei Devozionali",
        "conversations_history": "💭 Cronologia delle Conversazioni"
    },
    "ru": {
        "bible_studies_history": "📚 История Библейских Исследований",
        "sermon_generator": "Генератор Проповедей",
        "sermon_scope": "📚 Область Проповеди",
        "devotional_meditation": "Размышление и Медитация",
        "devotional_scope": "📚 Область Размышления",
        "theological_chat": "Богословский Чат",
        "sermons_history": "📋 История Проповедей",
        "devotionals_history": "🕊️ История Размышлений",
        "conversations_history": "💭 История Бесед"
    },
    "zh": {
        "bible_studies_history": "📚 圣经研究历史",
        "sermon_generator": "讲道生成器",
        "sermon_scope": "📚 讲道范围",
        "devotional_meditation": "灵修与冥想",
        "devotional_scope": "📚 灵修范围",
        "theological_chat": "神学聊天",
        "sermons_history": "📋 讲道历史",
        "devotionals_history": "🕊️ 灵修历史",
        "conversations_history": "💭 对话历史"
    },
    "es": {
        "bible_studies_history": "📚 Historial de Estudios Bíblicos",
        "sermon_generator": "Generador de Sermones",
        "sermon_scope": "📚 Alcance del Sermón",
        "devotional_meditation": "Devocional y Meditación",
        "devotional_scope": "📚 Alcance del Devocional",
        "theological_chat": "Chat Teológico",
        "sermons_history": "📋 Historial de Sermones",
        "devotionals_history": "🕊️ Historial de Devocionales",
        "conversations_history": "💭 Historial de Conversaciones"
    },
    "th": {
        "bible_studies_history": "📚 ประวัติการศึกษาพระคัมภีร์",
        "sermon_generator": "ตัวสร้างคำเทศนา",
        "sermon_scope": "📚 ขอบเขตคำเทศนา",
        "devotional_meditation": "คำภาวนาและการใคร่ครวญ",
        "devotional_scope": "📚 ขอบเขตคำภาวนา",
        "theological_chat": "แชทเทววิทยา",
        "sermons_history": "📋 ประวัติคำเทศนา",
        "devotionals_history": "🕊️ ประวัติคำภาวนา",
        "conversations_history": "💭 ประวัติบทสนทนา"
    },
    "el": {
        "bible_studies_history": "📚 Ιστορικό Βιβλικών Μελετών",
        "sermon_generator": "Γεννήτρια Κηρυγμάτων",
        "sermon_scope": "📚 Εύρος Κηρύγματος",
        "devotional_meditation": "Αφιέρωμα και Διαλογισμός",
        "devotional_scope": "📚 Εύρος Αφιερώματος",
        "theological_chat": "Θεολογική Συνομιλία",
        "sermons_history": "📋 Ιστορικό Κηρυγμάτων",
        "devotionals_history": "🕊️ Ιστορικό Αφιερωμάτων",
        "conversations_history": "💭 Ιστορικό Συνομιλιών"
    },
    "eo": {
        "bible_studies_history": "📚 Historio de Bibliaj Studoj",
        "sermon_generator": "Predika Generilo",
        "sermon_scope": "📚 Amplekso de Prediko",
        "devotional_meditation": "Dediĉo kaj Meditado",
        "devotional_scope": "📚 Amplekso de Dediĉo",
        "theological_chat": "Teologia Babilado",
        "sermons_history": "📋 Historio de Predikoj",
        "devotionals_history": "🕊️ Historio de Dediĉoj",
        "conversations_history": "💭 Historio de Konversacioj"
    },
    "fi": {
        "bible_studies_history": "📚 Raamatuntutkimuksen Historia",
        "sermon_generator": "Saarnan Luoja",
        "sermon_scope": "📚 Saarnan Laajuus",
        "devotional_meditation": "Hartaus ja Meditaatio",
        "devotional_scope": "📚 Hartauden Laajuus",
        "theological_chat": "Teologinen Keskustelu",
        "sermons_history": "📋 Saarnojen Historia",
        "devotionals_history": "🕊️ Hartauksien Historia",
        "conversations_history": "💭 Keskustelujen Historia"
    },
    "ko": {
        "bible_studies_history": "📚 성경 연구 기록",
        "sermon_generator": "설교 생성기",
        "sermon_scope": "📚 설교 범위",
        "devotional_meditation": "묵상과 명상",
        "devotional_scope": "📚 묵상 범위",
        "theological_chat": "신학 채팅",
        "sermons_history": "📋 설교 기록",
        "devotionals_history": "🕊️ 묵상 기록",
        "conversations_history": "💭 대화 기록"
    },
    "ro": {
        "bible_studies_history": "📚 Istoric Studii Biblice",
        "sermon_generator": "Generator de Predici",
        "sermon_scope": "📚 Domeniul Predicii",
        "devotional_meditation": "Devoțional și Meditație",
        "devotional_scope": "📚 Domeniul Devoționalului",
        "theological_chat": "Chat Teologic",
        "sermons_history": "📋 Istoric Predici",
        "devotionals_history": "🕊️ Istoric Devoționale",
        "conversations_history": "💭 Istoric Conversații"
    },
    "vi": {
        "bible_studies_history": "📚 Lịch Sử Nghiên Cứu Kinh Thánh",
        "sermon_generator": "Trình Tạo Bài Giảng",
        "sermon_scope": "📚 Phạm Vi Bài Giảng",
        "devotional_meditation": "Suy Gẫm và Thiền Định",
        "devotional_scope": "📚 Phạm Vi Suy Gẫm",
        "theological_chat": "Trò Chuyện Thần Học",
        "sermons_history": "📋 Lịch Sử Bài Giảng",
        "devotionals_history": "🕊️ Lịch Sử Suy Gẫm",
        "conversations_history": "💭 Lịch Sử Trò Chuyện"
    },
    "id": {
        "bible_studies_history": "📚 Riwayat Studi Alkitab",
        "sermon_generator": "Pembuat Khotbah",
        "sermon_scope": "📚 Ruang Lingkup Khotbah",
        "devotional_meditation": "Renungan dan Meditasi",
        "devotional_scope": "📚 Ruang Lingkup Renungan",
        "theological_chat": "Obrolan Teologi",
        "sermons_history": "📋 Riwayat Khotbah",
        "devotionals_history": "🕊️ Riwayat Renungan",
        "conversations_history": "💭 Riwayat Percakapan"
    },
    "pl": {
        "bible_studies_history": "📚 Historia Studiów Biblijnych",
        "sermon_generator": "Generator Kazań",
        "sermon_scope": "📚 Zakres Kazania",
        "devotional_meditation": "Nabożeństwo i Medytacja",
        "devotional_scope": "📚 Zakres Nabożeństwa",
        "theological_chat": "Czat Teologiczny",
        "sermons_history": "📋 Historia Kazań",
        "devotionals_history": "🕊️ Historia Nabożeństw",
        "conversations_history": "💭 Historia Rozmów"
    },
    "fa": {
        "bible_studies_history": "📚 تاریخچه مطالعات کتاب مقدس",
        "sermon_generator": "سازنده موعظه",
        "sermon_scope": "📚 محدوده موعظه",
        "devotional_meditation": "تأمل و مراقبه",
        "devotional_scope": "📚 محدوده تأمل",
        "theological_chat": "گفتگوی الهیاتی",
        "sermons_history": "📋 تاریخچه موعظه‌ها",
        "devotionals_history": "🕊️ تاریخچه تأملات",
        "conversations_history": "💭 تاریخچه مکالمات"
    },
    "sw": {
        "bible_studies_history": "📚 Historia ya Masomo ya Biblia",
        "sermon_generator": "Mtengenezaji wa Hotuba",
        "sermon_scope": "📚 Upeo wa Hotuba",
        "devotional_meditation": "Ibada na Tafakari",
        "devotional_scope": "📚 Upeo wa Ibada",
        "theological_chat": "Mazungumzo ya Kiteolojia",
        "sermons_history": "📋 Historia ya Hotuba",
        "devotionals_history": "🕊️ Historia ya Ibada",
        "conversations_history": "💭 Historia ya Mazungumzo"
    },
    "tr": {
        "bible_studies_history": "📚 İncil Çalışmaları Geçmişi",
        "sermon_generator": "Vaaz Oluşturucu",
        "sermon_scope": "📚 Vaaz Kapsamı",
        "devotional_meditation": "İbadet ve Meditasyon",
        "devotional_scope": "📚 İbadet Kapsamı",
        "theological_chat": "Teolojik Sohbet",
        "sermons_history": "📋 Vaaz Geçmişi",
        "devotionals_history": "🕊️ İbadet Geçmişi",
        "conversations_history": "💭 Konuşma Geçmişi"
    }
}

def update_all_headers():
    """Atualiza os headers em TODOS os idiomas para traduções 100% nativas."""
    
    translations_dir = Path("translations")
    updated = 0
    
    print("🌍 Atualizando headers para 100% nativos em todos os idiomas...\n")
    
    for lang_code, headers in NATIVE_HEADERS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ {lang_code}.json não encontrado")
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Criar seção headers se não existir
            if "headers" not in data:
                data["headers"] = {}
            
            # Atualizar headers
            changes = 0
            for key, value in headers.items():
                old_value = data["headers"].get(key, "")
                if old_value != value:
                    data["headers"][key] = value
                    changes += 1
            
            # Salvar se houve mudanças
            if changes > 0:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {lang_code}.json - {changes} headers atualizados")
                updated += 1
            else:
                print(f"⏭️ {lang_code}.json - headers já nativos")
        
        except Exception as e:
            print(f"❌ Erro em {lang_code}.json: {e}")
    
    return updated

if __name__ == "__main__":
    total = update_all_headers()
    print(f"\n✨ {total} arquivos atualizados! Todos os headers agora são 100% nativos!")
