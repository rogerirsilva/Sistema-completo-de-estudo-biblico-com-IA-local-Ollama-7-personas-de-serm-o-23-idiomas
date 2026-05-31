#!/usr/bin/env python3
"""Completa as traduções faltantes nos 12 novos idiomas com traduções nativas."""

import json
from pathlib import Path

# Traduções nativas completas para completar os headers e outras keys faltantes
COMPLETE_TRANSLATIONS = {
    "th": {  # Tailandês
        "headers": {
            "bible_studies_history": "📚 ประวัติการศึกษาพระคัมภีร์",
            "sermon_generator": "ตัวสร้างคำเทศนา",
            "sermon_scope": "📚 ขอบเขตคำเทศนา",
            "devotional_meditation": "คำภาวนาและการใคร่ครวญ",
            "devotional_scope": "📚 ขอบเขตคำภาวนา",
            "theological_chat": "แชทเทววิทยา",
            "sermons_history": "📋 ประวัติคำเทศนา",
            "devotionals_history": "🕊️ ประวัติคำภาวนา",
            "conversations_history": "💭 ประวัติบทสนทนา"
        }
    },
    "el": {  # Grego
        "headers": {
            "bible_studies_history": "📚 Ιστορικό Βιβλικών Μελετών",
            "sermon_generator": "Γεννήτρια Κηρυγμάτων",
            "sermon_scope": "📚 Εύρος Κηρύγματος",
            "devotional_meditation": "Αφιέρωμα και Διαλογισμός",
            "devotional_scope": "📚 Εύρος Αφιερώματος",
            "theological_chat": "Θεολογική Συνομιλία",
            "sermons_history": "📋 Ιστορικό Κηρυγμάτων",
            "devotionals_history": "🕊️ Ιστορικό Αφιερωμάτων",
            "conversations_history": "💭 Ιστορικό Συνομιλιών"
        }
    },
    "eo": {  # Esperanto
        "headers": {
            "bible_studies_history": "📚 Historio de Bibliaj Studoj",
            "sermon_generator": "Predika Generilo",
            "sermon_scope": "📚 Amplekso de Prediko",
            "devotional_meditation": "Dediĉo kaj Meditado",
            "devotional_scope": "📚 Amplekso de Dediĉo",
            "theological_chat": "Teologia Babilado",
            "sermons_history": "📋 Historio de Predikoj",
            "devotionals_history": "🕊️ Historio de Dediĉoj",
            "conversations_history": "💭 Historio de Konversacioj"
        }
    },
    "fi": {  # Finlandês
        "headers": {
            "bible_studies_history": "📚 Raamatuntutkimuksen Historia",
            "sermon_generator": "Saarnan Luoja",
            "sermon_scope": "📚 Saarnan Laajuus",
            "devotional_meditation": "Hartaus ja Meditaatio",
            "devotional_scope": "📚 Hartauden Laajuus",
            "theological_chat": "Teologinen Keskustelu",
            "sermons_history": "📋 Saarnojen Historia",
            "devotionals_history": "🕊️ Hartauksien Historia",
            "conversations_history": "💭 Keskustelujen Historia"
        }
    },
    "ko": {  # Coreano
        "headers": {
            "bible_studies_history": "📚 성경 연구 기록",
            "sermon_generator": "설교 생성기",
            "sermon_scope": "📚 설교 범위",
            "devotional_meditation": "묵상과 명상",
            "devotional_scope": "📚 묵상 범위",
            "theological_chat": "신학 채팅",
            "sermons_history": "📋 설교 기록",
            "devotionals_history": "🕊️ 묵상 기록",
            "conversations_history": "💭 대화 기록"
        }
    },
    "ro": {  # Romeno
        "headers": {
            "bible_studies_history": "📚 Istoric Studii Biblice",
            "sermon_generator": "Generator de Predici",
            "sermon_scope": "📚 Domeniul Predicii",
            "devotional_meditation": "Devoțional și Meditație",
            "devotional_scope": "📚 Domeniul Devoționalului",
            "theological_chat": "Chat Teologic",
            "sermons_history": "📋 Istoric Predici",
            "devotionals_history": "🕊️ Istoric Devoționale",
            "conversations_history": "💭 Istoric Conversații"
        }
    },
    "vi": {  # Vietnamita
        "headers": {
            "bible_studies_history": "📚 Lịch Sử Nghiên Cứu Kinh Thánh",
            "sermon_generator": "Trình Tạo Bài Giảng",
            "sermon_scope": "📚 Phạm Vi Bài Giảng",
            "devotional_meditation": "Suy Gẫm và Thiền Định",
            "devotional_scope": "📚 Phạm Vi Suy Gẫm",
            "theological_chat": "Trò Chuyện Thần Học",
            "sermons_history": "📋 Lịch Sử Bài Giảng",
            "devotionals_history": "🕊️ Lịch Sử Suy Gẫm",
            "conversations_history": "💭 Lịch Sử Trò Chuyện"
        }
    },
    "id": {  # Indonésio
        "headers": {
            "bible_studies_history": "📚 Riwayat Studi Alkitab",
            "sermon_generator": "Pembuat Khotbah",
            "sermon_scope": "📚 Ruang Lingkup Khotbah",
            "devotional_meditation": "Renungan dan Meditasi",
            "devotional_scope": "📚 Ruang Lingkup Renungan",
            "theological_chat": "Obrolan Teologi",
            "sermons_history": "📋 Riwayat Khotbah",
            "devotionals_history": "🕊️ Riwayat Renungan",
            "conversations_history": "💭 Riwayat Percakapan"
        }
    },
    "pl": {  # Polonês
        "headers": {
            "bible_studies_history": "📚 Historia Studiów Biblijnych",
            "sermon_generator": "Generator Kazań",
            "sermon_scope": "📚 Zakres Kazania",
            "devotional_meditation": "Nabożeństwo i Medytacja",
            "devotional_scope": "📚 Zakres Nabożeństwa",
            "theological_chat": "Czat Teologiczny",
            "sermons_history": "📋 Historia Kazań",
            "devotionals_history": "🕊️ Historia Nabożeństw",
            "conversations_history": "💭 Historia Rozmów"
        }
    },
    "fa": {  # Persa
        "headers": {
            "bible_studies_history": "📚 تاریخچه مطالعات کتاب مقدس",
            "sermon_generator": "سازنده موعظه",
            "sermon_scope": "📚 محدوده موعظه",
            "devotional_meditation": "تأمل و مراقبه",
            "devotional_scope": "📚 محدوده تأمل",
            "theological_chat": "گفتگوی الهیاتی",
            "sermons_history": "📋 تاریخچه موعظه‌ها",
            "devotionals_history": "🕊️ تاریخچه تأملات",
            "conversations_history": "💭 تاریخچه مکالمات"
        }
    },
    "sw": {  # Suaíli
        "headers": {
            "bible_studies_history": "📚 Historia ya Masomo ya Biblia",
            "sermon_generator": "Mtengenezaji wa Hotuba",
            "sermon_scope": "📚 Upeo wa Hotuba",
            "devotional_meditation": "Ibada na Tafakari",
            "devotional_scope": "📚 Upeo wa Ibada",
            "theological_chat": "Mazungumzo ya Kiteolojia",
            "sermons_history": "📋 Historia ya Hotuba",
            "devotionals_history": "🕊️ Historia ya Ibada",
            "conversations_history": "💭 Historia ya Mazungumzo"
        }
    },
    "tr": {  # Turco
        "headers": {
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
}

def update_translations():
    """Atualiza os arquivos de tradução com traduções nativas completas."""
    
    translations_dir = Path("translations")
    updated_count = 0
    
    for lang_code, new_translations in COMPLETE_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ {lang_code}.json não encontrado")
            continue
        
        try:
            # Carregar arquivo
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Aplicar traduções
            changes = 0
            for section, translations in new_translations.items():
                if section not in data:
                    data[section] = {}
                
                for key, value in translations.items():
                    old_value = data[section].get(key, "")
                    if old_value != value:
                        data[section][key] = value
                        changes += 1
            
            # Salvar arquivo
            if changes > 0:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {lang_code}.json - {changes} traduções atualizadas")
                updated_count += 1
            else:
                print(f"⏭️ {lang_code}.json - já completo")
        
        except Exception as e:
            print(f"❌ Erro ao processar {lang_code}.json: {e}")
    
    return updated_count

if __name__ == "__main__":
    print("🌍 Completando traduções nativas para os 12 novos idiomas...\n")
    total = update_translations()
    print(f"\n✨ {total} arquivos atualizados com traduções nativas completas!")
