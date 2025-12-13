#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script COMPLEMENTAR para as strings restantes que faltaram
"""

import json
import re
import os

# Traduções COMPLEMENTARES faltantes
ADDITIONAL_TRANSLATIONS = {
    "ar": {
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "أجب بوضوح لاهوتي ولطف رعوي، دائمًا على أساس السلطة الكتابية",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "اكتب مخططًا كاملاً للموعظة مع العنوان والمقدمة والموضوعات التفسيرية والتوضيحات والخاتمة",
        "The sermon should cover texts from:": "يجب أن تغطي الموعظة النصوص من:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "أنشئ قراءة هادئة وتأملاً موجزًا ​​وصلاة نهائية تربط الشعور المحدد بالنص الكتابي",
        "The devotional should consider texts from:": "يجب أن يأخذ التأمل الروحي في الاعتبار النصوص من:",
        "Create the folder manually or the application will create it automatically when importing.": "أنشئ المجلد يدويًا أو سيقوم التطبيق بإنشائه تلقائيًا عند الاستيراد",
    },
    
    "de": {
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Erstellen Sie eine ruhige Lesung, eine kurze Reflexion und ein abschließendes Gebet, das das ausgewählte Gefühl mit dem biblischen Text verbindet",
        "The devotional should consider texts from:": "Die Andacht sollte Texte berücksichtigen von:",
        "Create the folder manually or the application will create it automatically when importing.": "Erstellen Sie den Ordner manuell oder die Anwendung erstellt ihn automatisch beim Importieren",
    },
    
    "eo": {
        "No local versions found. Use Import Data to load content.": "Neniuj lokaj versioj trovitaj. Uzu Importi Datenojn por ŝarĝi enhavon",
        "No questions generated yet.": "Ankoraŭ neniuj demandoj generitaj",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Kreu pastran skizon kiu honoras la Vorton, estas grava kaj aplikebla al la indikita aŭdantaro",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Skribu personan meditadon kiu ofertas spiritan konsolon, profundan reflektadon kaj praktikan aplikon",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Respondu kun teologia klareco kaj pastra graco, ĉiam bazita sur biblia aŭtoritato",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Skribu kompletan predika skizon kun titolo, enkonduko, ekspoziciaj temoj, ilustraĵoj kaj konkludo",
        "The sermon should cover texts from:": "La prediko devus kovri tekstojn de:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Kreu trankvilan legadon, mallongan reflektadon kaj finan preĝon kiu ligas la elektitan senton al la biblia teksto",
        "The devotional should consider texts from:": "La devocia devus konsideri tekstojn de:",
        "Create the folder manually or the application will create it automatically when importing.": "Kreu la dosierujon permane aŭ la aplikaĵo kreos ĝin aŭtomate dum importado",
        "Generate questions about biblical knowledge.": "Generu demandojn pri biblia scio",
        "Selected context:": "Elektita kunteksto:",
    },
    
    "es": {
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Escribe un esquema completo del sermón con título, introducción, temas expositivos, ilustraciones y conclusión",
        "The sermon should cover texts from:": "El sermón debe cubrir textos de:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Crea una lectura tranquila, una breve reflexión y una oración final que conecte el sentimiento seleccionado con el texto bíblico",
        "The devotional should consider texts from:": "El devocional debe considerar textos de:",
    },
    
    "fi": {
        "The sermon should cover texts from:": "Saarnan tulisi käsitellä tekstejä:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Luo rauhallinen lukeminen, lyhyt pohdinta ja lopullinen rukous, joka yhdistää valitun tunteen raamatulliseen tekstiin",
        "The devotional should consider texts from:": "Hartauden tulisi käsitellä tekstejä:",
        "Create the folder manually or the application will create it automatically when importing.": "Luo kansio manuaalisesti tai sovellus luo sen automaattisesti tuotaessa",
        "Generate questions about biblical knowledge.": "Luo kysymyksiä raamatullisesta tiedosta",
        "Selected context:": "Valittu konteksti:",
    },
    
    "fr": {
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Créez une lecture calme, une brève réflexion et une prière finale qui relie le sentiment sélectionné au texte biblique",
        "The devotional should consider texts from:": "Le dévotionnel devrait considérer les textes de:",
        "Create the folder manually or the application will create it automatically when importing.": "Créez le dossier manuellement ou l'application le créera automatiquement lors de l'importation",
        "Generate questions about biblical knowledge.": "Générer des questions sur les connaissances bibliques",
        "Selected context:": "Contexte sélectionné:",
    },
    
    "hi": {
        "Generate questions about biblical knowledge.": "बाइबिल ज्ञान के बारे में प्रश्न उत्पन्न करें",
        "Selected context:": "चयनित संदर्भ:",
        "Create the folder manually or the application will create it automatically when importing.": "फ़ोल्डर मैन्युअल रूप से बनाएं या आयात करते समय एप्लिकेशन इसे स्वचालित रूप से बनाएगा",
        "The devotional should consider texts from:": "भक्ति में इनसे ग्रंथों पर विचार करना चाहिए:",
        "The sermon should cover texts from:": "उपदेश में इनसे ग्रंथों को शामिल करना चाहिए:",
    },
    
    "id": {
        "No local versions found. Use Import Data to load content.": "Tidak ada versi lokal ditemukan. Gunakan Impor Data untuk memuat konten",
        "No questions generated yet.": "Belum ada pertanyaan yang dihasilkan",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Buat garis besar pastoral yang menghormati Firman, relevan dan dapat diterapkan pada audiens yang ditunjukkan",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Tulis meditasi pribadi yang menawarkan kenyamanan spiritual, refleksi mendalam dan aplikasi praktis",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Jawab dengan kejelasan teologis dan rahmat pastoral, selalu berdasarkan otoritas alkitabiah",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Tulis garis besar khotbah lengkap dengan judul, pendahuluan, topik ekspositori, ilustrasi dan kesimpulan",
        "The sermon should cover texts from:": "Khotbah harus mencakup teks dari:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Buat bacaan yang tenang, refleksi singkat dan doa akhir yang menghubungkan perasaan yang dipilih dengan teks alkitabiah",
        "The devotional should consider texts from:": "Renungan harus mempertimbangkan teks dari:",
        "Create the folder manually or the application will create it automatically when importing.": "Buat folder secara manual atau aplikasi akan membuatnya secara otomatis saat mengimpor",
        "Generate questions about biblical knowledge.": "Hasilkan pertanyaan tentang pengetahuan alkitabiah",
        "Selected context:": "Konteks yang dipilih:",
    },
    
    "it": {
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Crea una lettura calma, una breve riflessione e una preghiera finale che collega il sentimento selezionato al testo biblico",
        "The devotional should consider texts from:": "Il devozionale dovrebbe considerare testi da:",
        "Create the folder manually or the application will create it automatically when importing.": "Crea la cartella manualmente o l'applicazione la creerà automaticamente durante l'importazione",
        "Generate questions about biblical knowledge.": "Genera domande sulla conoscenza biblica",
        "Selected context:": "Contesto selezionato:",
    },
    
    "ko": {
        "No local versions found. Use Import Data to load content.": "로컬 버전을 찾을 수 없습니다. 콘텐츠를 로드하려면 데이터 가져오기를 사용하세요",
        "No questions generated yet.": "아직 생성된 질문이 없습니다",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "말씀을 존중하고 지정된 청중에게 관련성 있고 적용 가능한 목회 개요를 만드세요",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "영적 위안, 깊은 성찰 및 실제 적용을 제공하는 개인 묵상을 작성하세요",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "신학적 명확성과 목회적 은혜로 대답하며 항상 성경적 권위에 근거하세요",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "제목, 소개, 해설 주제, 예화 및 결론이 포함된 완전한 설교 개요를 작성하세요",
        "The sermon should cover texts from:": "설교는 다음의 텍스트를 다루어야 합니다:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "선택한 감정을 성경 텍스트와 연결하는 평온한 읽기, 간단한 성찰 및 최종 기도를 만드세요",
        "The devotional should consider texts from:": "묵상은 다음의 텍스트를 고려해야 합니다:",
        "Create the folder manually or the application will create it automatically when importing.": "폴더를 수동으로 만들거나 가져올 때 애플리케이션이 자동으로 만듭니다",
        "Generate questions about biblical knowledge.": "성경 지식에 대한 질문을 생성하세요",
        "Selected context:": "선택된 컨텍스트:",
    },
    
    "pl": {
        "No local versions found. Use Import Data to load content.": "Nie znaleziono lokalnych wersji. Użyj Importuj Dane, aby załadować zawartość",
        "No questions generated yet.": "Nie wygenerowano jeszcze żadnych pytań",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Utwórz pastorski zarys, który honoruje Słowo, jest istotny i możliwy do zastosowania dla wskazanej publiczności",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Napisz osobistą medytację, która oferuje duchową pociechę, głęboką refleksję i praktyczne zastosowanie",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Odpowiadaj z teologiczną jasnością i pastorską łaską, zawsze opartą na biblijnej autorytecie",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Napisz kompletny zarys kazania z tytułem, wstępem, tematami wykładowymi, ilustracjami i zakończeniem",
        "The sermon should cover texts from:": "Kazanie powinno obejmować teksty z:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Utwórz spokojne czytanie, krótką refleksję i końcową modlitwę, która łączy wybrane uczucie z biblijnym tekstem",
        "The devotional should consider texts from:": "Rozważanie powinno uwzględniać teksty z:",
        "Create the folder manually or the application will create it automatically when importing.": "Utwórz folder ręcznie lub aplikacja utworzy go automatycznie podczas importowania",
        "Generate questions about biblical knowledge.": "Generuj pytania dotyczące wiedzy biblijnej",
        "Selected context:": "Wybrany kontekst:",
    },
    
    "ro": {
        "No local versions found. Use Import Data to load content.": "Nu s-au găsit versiuni locale. Utilizați Importați date pentru a încărca conținut",
        "No questions generated yet.": "Nu s-au generat încă întrebări",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Creați un contur pastoral care onorează Cuvântul, este relevant și aplicabil publicului indicat",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Scrieți o meditație personală care oferă confort spiritual, reflecție profundă și aplicație practică",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Răspundeți cu claritate teologică și har pastoral, întotdeauna bazat pe autoritatea biblică",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Scrieți un contur complet al predicii cu titlu, introducere, subiecte expozitive, ilustrații și concluzie",
        "The sermon should cover texts from:": "Predica ar trebui să acopere texte din:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Creați o lectură calmă, o reflecție scurtă și o rugăciune finală care conectează sentimentul selectat la textul biblic",
        "The devotional should consider texts from:": "Devoțiunea ar trebui să ia în considerare texte din:",
        "Create the folder manually or the application will create it automatically when importing.": "Creați folderul manual sau aplicația îl va crea automat la importare",
        "Generate questions about biblical knowledge.": "Generați întrebări despre cunoștințele biblice",
        "Selected context:": "Context selectat:",
    },
    
    "ru": {
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Создайте спокойное чтение, краткое размышление и заключительную молитву, которая связывает выбранное чувство с библейским текстом",
        "The devotional should consider texts from:": "Размышление должно учитывать тексты из:",
        "Create the folder manually or the application will create it automatically when importing.": "Создайте папку вручную или приложение создаст ее автоматически при импорте",
        "Generate questions about biblical knowledge.": "Генерируйте вопросы о библейских знаниях",
        "Selected context:": "Выбранный контекст:",
    },
    
    "sw": {
        "No local versions found. Use Import Data to load content.": "Hakuna matoleo ya ndani yaliyopatikana. Tumia Agiza Data kupakia maudhui",
        "No questions generated yet.": "Hakuna maswali yaliyozalishwa bado",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Unda muhtasari wa kichungaji unaouheshimu Neno, ni muhimu na unatumika kwa hadhira iliyoonyeshwa",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Andika tafakuri ya kibinafsi inayotoa faraja ya kiroho, tafakuri ya kina na matumizi ya vitendo",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Jibu kwa uwazi wa kiteolojia na neema ya kichungaji, daima kulingana na mamlaka ya Biblia",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Andika muhtasari kamili wa hotuba na kichwa, utangulizi, mada za ufafanuzi, mifano na hitimisho",
        "The sermon should cover texts from:": "Hotuba inapaswa kufunika maandishi kutoka:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Unda kusoma kwa utulivu, tafakuri fupi na sala ya mwisho inayounganisha hisia zilizochaguliwa na maandishi ya Biblia",
        "The devotional should consider texts from:": "Ibada inapaswa kuzingatia maandishi kutoka:",
        "Create the folder manually or the application will create it automatically when importing.": "Unda folda kwa mikono au programu itaiunda kiotomatiki wakati wa kuagiza",
        "Generate questions about biblical knowledge.": "Zalisha maswali kuhusu maarifa ya Biblia",
        "Selected context:": "Muktadha uliochaguliwa:",
    },
    
    "th": {
        "Generate questions about biblical knowledge.": "สร้างคำถามเกี่ยวกับความรู้ในพระคัมภีร์",
        "Selected context:": "บริบทที่เลือก:",
        "Create the folder manually or the application will create it automatically when importing.": "สร้างโฟลเดอร์ด้วยตนเองหรือแอปพลิเคชันจะสร้างโดยอัตโนมัติเมื่อนำเข้า",
        "The devotional should consider texts from:": "การภาวนาควรพิจารณาข้อความจาก:",
        "The sermon should cover texts from:": "การเทศนาควรครอบคลุมข้อความจาก:",
    },
    
    "tr": {
        "No local versions found. Use Import Data to load content.": "Yerel sürüm bulunamadı. İçerik yüklemek için Veri İçe Aktar'ı kullanın",
        "No questions generated yet.": "Henüz soru oluşturulmadı",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Tanrı'nın Sözünü onurlandıran, alakalı ve belirtilen kitleye uygulanabilir bir pastoral taslak oluşturun",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Ruhsal rahatlık, derin yansıma ve pratik uygulama sunan kişisel bir meditasyon yazın",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Teolojik netlik ve pastoral zarafetle cevap verin, her zaman İncil otoritesine dayalı",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Başlık, giriş, açıklayıcı konular, örnekler ve sonuçla birlikte eksiksiz bir vaaz taslağı yazın",
        "The sermon should cover texts from:": "Vaaz şu metinleri kapsamalıdır:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Seçilen duyguyu İncil metnine bağlayan sakin bir okuma, kısa bir yansıma ve son bir dua oluşturun",
        "The devotional should consider texts from:": "İbadet şu metinleri dikkate almalıdır:",
        "Create the folder manually or the application will create it automatically when importing.": "Klasörü manuel olarak oluşturun veya uygulama içe aktarırken otomatik olarak oluşturacak",
        "Generate questions about biblical knowledge.": "İncil bilgisi hakkında sorular oluşturun",
        "Selected context:": "Seçili bağlam:",
    },
    
    "vi": {
        "No local versions found. Use Import Data to load content.": "Không tìm thấy phiên bản cục bộ. Sử dụng Nhập Dữ liệu để tải nội dung",
        "No questions generated yet.": "Chưa tạo câu hỏi nào",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Tạo dàn ý mục vụ tôn vinh Lời Chúa, có liên quan và áp dụng được cho đối tượng được chỉ định",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Viết một suy niệm cá nhân mang lại sự an ủi tinh thần, suy ngẫm sâu sắc và ứng dụng thực tế",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Trả lời với sự rõ ràng thần học và ân sủng mục vụ, luôn dựa trên thẩm quyền Kinh Thánh",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Viết dàn ý bài giảng hoàn chỉnh với tiêu đề, giới thiệu, chủ đề giải thích, minh họa và kết luận",
        "The sermon should cover texts from:": "Bài giảng nên bao gồm các văn bản từ:",
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "Tạo một bài đọc bình tĩnh, một suy ngẫm ngắn gọn và một lời cầu nguyện cuối cùng kết nối cảm xúc được chọn với văn bản Kinh Thánh",
        "The devotional should consider texts from:": "Suy niệm nên xem xét các văn bản từ:",
        "Create the folder manually or the application will create it automatically when importing.": "Tạo thư mục thủ công hoặc ứng dụng sẽ tự động tạo khi nhập",
        "Generate questions about biblical knowledge.": "Tạo câu hỏi về kiến thức Kinh Thánh",
        "Selected context:": "Ngữ cảnh đã chọn:",
    },
    
    "zh": {
        "Create a calm reading, a brief reflection and a final prayer that connects the selected feeling to the biblical text.": "创建一个平静的阅读、简短的反思和最后的祷告，将选定的感受与圣经文本联系起来",
        "The devotional should consider texts from:": "灵修应考虑来自以下的文本:",
        "Create the folder manually or the application will create it automatically when importing.": "手动创建文件夹，或应用程序将在导入时自动创建",
        "Generate questions about biblical knowledge.": "生成关于圣经知识的问题",
        "Selected context:": "已选择的上下文:",
    },
}

def replace_translations(filepath, translations_map):
    """Substitui textos em inglês por traduções nativas"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for english, native in translations_map.items():
        english_escaped = re.escape(english)
        pattern = f'"{english_escaped}"'
        if re.search(pattern, content):
            content = re.sub(pattern, f'"{native}"', content)
            count += 1
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return count

def main():
    translations_dir = "translations"
    total_replacements = 0
    
    print("🔧 Aplicando traduções COMPLEMENTARES...")
    print("=" * 70)
    
    for lang_code, translations in ADDITIONAL_TRANSLATIONS.items():
        filepath = os.path.join(translations_dir, f"{lang_code}.json")
        
        if not os.path.exists(filepath):
            print(f"⚠️  {lang_code}.json não encontrado")
            continue
        
        count = replace_translations(filepath, translations)
        total_replacements += count
        
        if count > 0:
            print(f"✅ {lang_code.upper()}: +{count} strings adicionais")
    
    print("=" * 70)
    print(f"🎉 +{total_replacements} strings complementares traduzidas!")

if __name__ == "__main__":
    main()
