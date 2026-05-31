#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script FINAL - Últimas strings que faltaram
"""

import json
import re
import os

FINAL_MISSING = {
    # Strings comuns em TODOS os idiomas
    "common": {
        "Theme or feeling to meditate on": {
            "ar": "الموضوع أو الشعور للتأمل فيه",
            "de": "Thema oder Gefühl zum Meditieren",
            "eo": "Temo aŭ sento por mediti pri",
            "es": "Tema o sentimiento para meditar",
            "fi": "Teema tai tunne meditointiin",
            "fr": "Thème ou sentiment sur lequel méditer",
            "hi": "ध्यान करने के लिए विषय या भावना",
            "id": "Tema atau perasaan untuk direnungkan",
            "it": "Tema o sentimento su cui meditare",
            "ko": "명상할 주제 또는 감정",
            "pl": "Temat lub uczucie do medytacji",
            "ro": "Temă sau sentiment pentru meditație",
            "ru": "Тема или чувство для медитации",
            "sw": "Mada au hisia ya kutafakari",
            "th": "หัวข้อหรือความรู้สึกที่จะนั่งสมาธิ",
            "tr": "Meditasyon için tema veya duygu",
            "vi": "Chủ đề hoặc cảm giác để suy ngẫm",
            "zh": "要冥想的主题或感受",
        },
        "Merge with existing versions instead of replacing": {
            "ar": "دمج مع الإصدارات الموجودة بدلاً من الاستبدال",
            "de": "Mit vorhandenen Versionen zusammenführen statt ersetzen",
            "eo": "Kunfandi kun ekzistantaj versioj anstataŭ anstataŭigi",
            "es": "Fusionar con versiones existentes en lugar de reemplazar",
            "fi": "Yhdistä olemassa oleviin versioihin korvaamisen sijaan",
            "fr": "Fusionner avec les versions existantes au lieu de remplacer",
            "hi": "प्रतिस्थापन के बजाय मौजूदा संस्करणों के साथ विलय करें",
            "id": "Gabungkan dengan versi yang ada alih-alih mengganti",
            "it": "Unisci con le versioni esistenti invece di sostituire",
            "ko": "교체 대신 기존 버전과 병합",
            "pl": "Scal z istniejącymi wersjami zamiast zastępować",
            "ro": "Îmbină cu versiunile existente în loc să înlocuiești",
            "ru": "Объединить с существующими версиями вместо замены",
            "sw": "Unganisha na matoleo yaliyopo badala ya kubadilisha",
            "th": "รวมกับเวอร์ชันที่มีอยู่แทนการแทนที่",
            "tr": "Değiştirmek yerine mevcut sürümlerle birleştir",
            "vi": "Hợp nhất với các phiên bản hiện có thay vì thay thế",
            "zh": "与现有版本合并而不是替换",
        },
        "Set as default version on startup": {
            "ar": "تعيين كإصدار افتراضي عند بدء التشغيل",
            "de": "Als Standardversion beim Start festlegen",
            "eo": "Agordi kiel defaŭlta versio ĉe starto",
            "es": "Establecer como versión predeterminada al iniciar",
            "fi": "Aseta oletusversioksi käynnistettäessä",
            "fr": "Définir comme version par défaut au démarrage",
            "hi": "स्टार्टअप पर डिफ़ॉल्ट संस्करण के रूप में सेट करें",
            "id": "Tetapkan sebagai versi default saat startup",
            "it": "Imposta come versione predefinita all'avvio",
            "ko": "시작 시 기본 버전으로 설정",
            "pl": "Ustaw jako wersję domyślną przy uruchomieniu",
            "ro": "Setează ca versiune implicită la pornire",
            "ru": "Установить как версию по умолчанию при запуске",
            "sw": "Weka kama toleo chaguo-msingi kwenye uanzishaji",
            "th": "ตั้งเป็นเวอร์ชันเริ่มต้นเมื่อเริ่มต้น",
            "tr": "Başlangıçta varsayılan sürüm olarak ayarla",
            "vi": "Đặt làm phiên bản mặc định khi khởi động",
            "zh": "设置为启动时的默认版本",
        },
        "Number of questions to generate": {
            "ar": "عدد الأسئلة التي سيتم إنشاؤها",
            "de": "Anzahl der zu generierenden Fragen",
            "eo": "Nombro de demandoj por generi",
            "es": "Número de preguntas a generar",
            "fi": "Tuotettavien kysymysten määrä",
            "fr": "Nombre de questions à générer",
            "hi": "उत्पन्न करने के लिए प्रश्नों की संख्या",
            "id": "Jumlah pertanyaan yang akan dihasilkan",
            "it": "Numero di domande da generare",
            "ko": "생성할 질문 수",
            "pl": "Liczba pytań do wygenerowania",
            "ro": "Număr de întrebări de generat",
            "ru": "Количество вопросов для генерации",
            "sw": "Idadi ya maswali ya kuzalisha",
            "th": "จำนวนคำถามที่จะสร้าง",
            "tr": "Oluşturulacak soru sayısı",
            "vi": "Số lượng câu hỏi cần tạo",
            "zh": "要生成的问题数量",
        },
        "Explain the historical and theological context, ponder key words and suggest pastoral applications.": {
            "ar": "اشرح السياق التاريخي واللاهوتي، وتأمل في الكلمات الرئيسية واقترح تطبيقات رعوية",
            "de": "Erklären Sie den historischen und theologischen Kontext, überdenken Sie Schlüsselwörter und schlagen Sie pastorale Anwendungen vor",
            "eo": "Klarigu la historian kaj teologian kuntekston, pripensu ĉefajn vortojn kaj sugesti pastrajn aplikojn",
            "es": "Explica el contexto histórico y teológico, reflexiona sobre palabras clave y sugiere aplicaciones pastorales",
            "fi": "Selitä historiallinen ja teologinen konteksti, pohdi avainsanoja ja ehdota pastoraalisia sovelluksia",
            "fr": "Expliquez le contexte historique et théologique, réfléchissez aux mots-clés et suggérez des applications pastorales",
            "hi": "ऐतिहासिक और धर्मशास्त्रीय संदर्भ को समझाएं, मुख्य शब्दों पर विचार करें और पादरी अनुप्रयोगों का सुझाव दें",
            "id": "Jelaskan konteks historis dan teologis, renungkan kata kunci dan sarankan aplikasi pastoral",
            "it": "Spiega il contesto storico e teologico, rifletti su parole chiave e suggerisci applicazioni pastorali",
            "ko": "역사적, 신학적 맥락을 설명하고 핵심 단어를 숙고하며 목회적 적용을 제안하세요",
            "pl": "Wyjaśnij kontekst historyczny i teologiczny, zastanów się nad kluczowymi słowami i zasugeruj aplikacje pastoralne",
            "ro": "Explică contextul istoric și teologic, meditează la cuvinte cheie și sugerează aplicații pastorale",
            "ru": "Объясните исторический и теологический контекст, обдумайте ключевые слова и предложите пастырские применения",
            "sw": "Eleza muktadha wa kihistoria na wa kiteolojia, tafakari maneno muhimu na upendekeze matumizi ya kichungaji",
            "th": "อธิบายบริบททางประวัติศาสตร์และเทววิทยา ไตร่ตรองคำสำคัญ และเสนอแนะการประยุกต์ใช้ด้านอภิบาล",
            "tr": "Tarihsel ve teolojik bağlamı açıklayın, anahtar kelimeleri düşünün ve pastoral uygulamalar önerin",
            "vi": "Giải thích bối cảnh lịch sử và thần học, suy ngẫm về các từ khóa và đề xuất các ứng dụng mục vụ",
            "zh": "解释历史和神学背景，思考关键词并提出牧养应用",
        },
        "All generated questions are automatically saved here.": {
            "ar": "يتم حفظ جميع الأسئلة المولدة تلقائيًا هنا",
            "de": "Alle generierten Fragen werden automatisch hier gespeichert",
            "eo": "Ĉiuj generitaj demandoj estas aŭtomate konservitaj ĉi tie",
            "es": "Todas las preguntas generadas se guardan automáticamente aquí",
            "fi": "Kaikki tuotetut kysymykset tallennetaan automaattisesti tänne",
            "fr": "Toutes les questions générées sont automatiquement enregistrées ici",
            "hi": "सभी उत्पन्न प्रश्न स्वचालित रूप से यहाँ सहेजे जाते हैं",
            "id": "Semua pertanyaan yang dihasilkan secara otomatis disimpan di sini",
            "it": "Tutte le domande generate vengono automaticamente salvate qui",
            "ko": "생성된 모든 질문이 자동으로 여기에 저장됩니다",
            "pl": "Wszystkie wygenerowane pytania są automatycznie zapisywane tutaj",
            "ro": "Toate întrebările generate sunt salvate automat aici",
            "ru": "Все созданные вопросы автоматически сохраняются здесь",
            "sw": "Maswali yote yaliyozalishwa yanasekwa hapa kiotomatiki",
            "th": "คำถามที่สร้างทั้งหมดจะถูกบันทึกที่นี่โดยอัตโนมัติ",
            "tr": "Oluşturulan tüm sorular otomatik olarak burada kaydedilir",
            "vi": "Tất cả câu hỏi được tạo đều được lưu tự động ở đây",
            "zh": "所有生成的问题都会自动保存在这里",
        },
        "Leave empty to import all available versions from the folder": {
            "ar": "اتركه فارغًا لاستيراد جميع الإصدارات المتاحة من المجلد",
            "de": "Leer lassen, um alle verfügbaren Versionen aus dem Ordner zu importieren",
            "eo": "Lasu malplena por importi ĉiujn disponeblajn versiojn el la dosierujo",
            "es": "Dejar vacío para importar todas las versiones disponibles de la carpeta",
            "fi": "Jätä tyhjäksi tuodaksesi kaikki saatavilla olevat versiot kansiosta",
            "fr": "Laissez vide pour importer toutes les versions disponibles du dossier",
            "hi": "फ़ोल्डर से सभी उपलब्ध संस्करणों को आयात करने के लिए खाली छोड़ दें",
            "id": "Biarkan kosong untuk mengimpor semua versi yang tersedia dari folder",
            "it": "Lascia vuoto per importare tutte le versioni disponibili dalla cartella",
            "ko": "폴더에서 사용 가능한 모든 버전을 가져오려면 비워 두세요",
            "pl": "Pozostaw puste, aby zaimportować wszystkie dostępne wersje z folderu",
            "ro": "Lasă gol pentru a importa toate versiunile disponibile din folder",
            "ru": "Оставьте пустым, чтобы импортировать все доступные версии из папки",
            "sw": "Acha tupu ili uagize matoleo yote yaliyopo kutoka kwa folda",
            "th": "เว้นว่างไว้เพื่อนำเข้าเวอร์ชันที่มีอยู่ทั้งหมดจากโฟลเดอร์",
            "tr": "Klasördeki tüm mevcut sürümleri içe aktarmak için boş bırakın",
            "vi": "Để trống để nhập tất cả các phiên bản có sẵn từ thư mục",
            "zh": "留空以从文件夹导入所有可用版本",
        },
    }
}

def apply_final_translations():
    translations_dir = "translations"
    total = 0
    
    print("🎯 Aplicando ÚLTIMAS traduções faltantes...")
    print("=" * 70)
    
    for english_text, translations in FINAL_MISSING["common"].items():
        for lang_code, native_text in translations.items():
            filepath = os.path.join(translations_dir, f"{lang_code}.json")
            
            if not os.path.exists(filepath):
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            english_escaped = re.escape(english_text)
            pattern = f'"{english_escaped}"'
            
            if re.search(pattern, content):
                content = re.sub(pattern, f'"{native_text}"', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                total += 1
                print(f"✅ {lang_code.upper()}: Traduzido \"{english_text[:40]}...\"")
    
    print("=" * 70)
    print(f"🎉 {total} traduções finais aplicadas!")
    return total

if __name__ == "__main__":
    apply_final_translations()
