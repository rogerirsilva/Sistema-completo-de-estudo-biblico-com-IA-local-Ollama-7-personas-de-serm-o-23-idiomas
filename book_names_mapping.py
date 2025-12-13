"""
Mapeamento de nomes de livros bíblicos em diferentes idiomas.
Baseado nas abreviações padrão e nomes traduzidos.
"""

BOOK_NAMES = {
    # Velho Testamento
    "gn": {
        "pt": "Gênesis", "en": "Genesis", "es": "Génesis", "fr": "Genèse", "de": "Genesis",
        "it": "Genesi", "ru": "Бытие", "zh": "创世记", "ja": "創世記", "ar": "التكوين",
        "el": "Γένεση", "eo": "Genezo", "fi": "Ensimmäinen Mooseksen", "ko": "창세기",
        "ro": "Geneza", "vi": "Sáng Thế Ký", "hi": "उत्पत्ति", "id": "Kejadian",
        "pl": "Rodzaju", "fa": "پیدایش", "sw": "Mwanzo", "th": "ปฐมกาล", "tr": "Tekvin"
    },
    "ex": {
        "pt": "Êxodo", "en": "Exodus", "es": "Éxodo", "fr": "Exode", "de": "Exodus",
        "it": "Esodo", "ru": "Исход", "zh": "出埃及记", "ja": "出エジプト記", "ar": "الخروج",
        "el": "Έξοδος", "eo": "Eliro", "fi": "Toinen Mooseksen", "ko": "출애굽기",
        "ro": "Exodul", "vi": "Xuất Hành", "hi": "निर्गमन", "id": "Keluaran",
        "pl": "Wyjścia", "fa": "خروج", "sw": "Kutoka", "th": "อพยพ", "tr": "Çıkış"
    },
    "lv": {
        "pt": "Levítico", "en": "Leviticus", "es": "Levítico", "fr": "Lévitique", "de": "Levitikus",
        "it": "Levitico", "ru": "Левит", "zh": "利未记", "ja": "レビ記", "ar": "اللاويين",
        "el": "Λευιτικό", "eo": "Levidoj", "fi": "Kolmas Mooseksen", "ko": "레위기",
        "ro": "Levitic", "vi": "Lê-vi Ký", "hi": "लैव्यव्यवस्था", "id": "Imamat",
        "pl": "Kapłańska", "fa": "لاویان", "sw": "Walawi", "th": "เลวีนิติ", "tr": "Levililer"
    },
    "nm": {
        "pt": "Números", "en": "Numbers", "es": "Números", "fr": "Nombres", "de": "Numeri",
        "it": "Numeri", "ru": "Числа", "zh": "民数记", "ja": "民数記", "ar": "العدد",
        "el": "Αριθμοί", "eo": "Nombroj", "fi": "Neljäs Mooseksen", "ko": "민수기",
        "ro": "Numeri", "vi": "Dân Số Ký", "hi": "गिनती", "id": "Bilangan",
        "pl": "Liczb", "fa": "اعداد", "sw": "Hesabu", "th": "กันดารวิถี", "tr": "Sayılar"
    },
    "dt": {
        "pt": "Deuteronômio", "en": "Deuteronomy", "es": "Deuteronomio", "fr": "Deutéronome", "de": "Deuteronomium",
        "it": "Deuteronomio", "ru": "Второзаконие", "zh": "申命记", "ja": "申命記", "ar": "التثنية",
        "el": "Δευτερονόμιο", "eo": "Readmono", "fi": "Viides Mooseksen", "ko": "신명기",
        "ro": "Deuteronom", "vi": "Phục Truyền", "hi": "व्यवस्थाविवरण", "id": "Ulangan",
        "pl": "Powtórzonego Prawa", "fa": "تثنیه", "sw": "Kumbukumbu la Torati", "th": "เฉลยธรรมบัญญัติ", "tr": "Tesniye"
    },
    "js": {
        "pt": "Josué", "en": "Joshua", "es": "Josué", "fr": "Josué", "de": "Josua",
        "it": "Giosué", "ru": "Иисус Навин", "zh": "约书亚记", "ja": "ヨシュア記", "ar": "يشوع",
        "el": "Ιησούς του Ναυή", "eo": "Josuo", "fi": "Joosua", "ko": "여호수아",
        "ro": "Iosua", "vi": "Giô-suê", "hi": "यहोशू", "id": "Yosua",
        "pl": "Jozuego", "fa": "یوشع", "sw": "Yoshua", "th": "โยชูวา", "tr": "Yeşu"
    },
    "jz": {
        "pt": "Juízes", "en": "Judges", "es": "Jueces", "fr": "Juges", "de": "Richter",
        "it": "Giudici", "ru": "Судей", "zh": "士师记", "ja": "士師記", "ar": "القضاة",
        "el": "Κριτές", "eo": "Juĝistoj", "fi": "Tuomarien kirja", "ko": "사사기",
        "ro": "Judecători", "vi": "Thủ Lĩnh", "hi": "न्यायियों", "id": "Hakim-hakim",
        "pl": "Sędziów", "fa": "داوران", "sw": "Waamuzi", "th": "ผู้วินิจฉัย", "tr": "Hakimler"
    },
    "rt": {
        "pt": "Rute", "en": "Ruth", "es": "Rut", "fr": "Ruth", "de": "Rut",
        "it": "Rut", "ru": "Руфь", "zh": "路得记", "ja": "ルツ記", "ar": "راعوث",
        "el": "Ρουθ", "eo": "Rut", "fi": "Ruut", "ko": "룻기",
        "ro": "Rut", "vi": "Ru-tơ", "hi": "रूत", "id": "Rut",
        "pl": "Rut", "fa": "روت", "sw": "Ruthu", "th": "นางรูธ", "tr": "Rut"
    },
    "1sm": {
        "pt": "1 Samuel", "en": "1 Samuel", "es": "1 Samuel", "fr": "1 Samuel", "de": "1 Samuel",
        "it": "1 Samuele", "ru": "1 Царств", "zh": "撒母耳记上", "ja": "サムエル記上", "ar": "صموئيل الأول",
        "el": "Α' Σαμουήλ", "eo": "1 Samuel", "fi": "1 Samuel", "ko": "사무엘상",
        "ro": "1 Samuel", "vi": "1 Sa-mu-ên", "hi": "1 शमूएल", "id": "1 Samuel",
        "pl": "1 Samuela", "fa": "اول سموئیل", "sw": "1 Samweli", "th": "1 ซามูเอล", "tr": "1 Samuel"
    },
    "2sm": {
        "pt": "2 Samuel", "en": "2 Samuel", "es": "2 Samuel", "fr": "2 Samuel", "de": "2 Samuel",
        "it": "2 Samuele", "ru": "2 Царств", "zh": "撒母耳记下", "ja": "サムエル記下", "ar": "صموئيل الثاني",
        "el": "Β' Σαμουήλ", "eo": "2 Samuel", "fi": "2 Samuel", "ko": "사무엘하",
        "ro": "2 Samuel", "vi": "2 Sa-mu-ên", "hi": "2 शमूएल", "id": "2 Samuel",
        "pl": "2 Samuela", "fa": "دوم سموئیل", "sw": "2 Samweli", "th": "2 ซามูเอล", "tr": "2 Samuel"
    },
    "1rs": {
        "pt": "1 Reis", "en": "1 Kings", "es": "1 Reyes", "fr": "1 Rois", "de": "1 Könige",
        "it": "1 Re", "ru": "3 Царств", "zh": "列王纪上", "ja": "列王記上", "ar": "الملوك الأول",
        "el": "Α' Βασιλέων", "eo": "1 Reĝoj", "fi": "1 Kuninkaiden", "ko": "열왕기상",
        "ro": "1 Regi", "vi": "1 Các Vua", "hi": "1 राजा", "id": "1 Raja-raja",
        "pl": "1 Królewska", "fa": "اول پادشاهان", "sw": "1 Wafalme", "th": "1 พงศ์กษัตริย์", "tr": "1 Krallar"
    },
    "2rs": {
        "pt": "2 Reis", "en": "2 Kings", "es": "2 Reyes", "fr": "2 Rois", "de": "2 Könige",
        "it": "2 Re", "ru": "4 Царств", "zh": "列王纪下", "ja": "列王記下", "ar": "الملوك الثاني",
        "el": "Β' Βασιλέων", "eo": "2 Reĝoj", "fi": "2 Kuninkaiden", "ko": "열왕기하",
        "ro": "2 Regi", "vi": "2 Các Vua", "hi": "2 राजा", "id": "2 Raja-raja",
        "pl": "2 Królewska", "fa": "دوم پادشاهان", "sw": "2 Wafalme", "th": "2 พงศ์กษัตริย์", "tr": "2 Krallar"
    },
    
    # Novo Testamento
    "mt": {
        "pt": "Mateus", "en": "Matthew", "es": "Mateo", "fr": "Matthieu", "de": "Matthäus",
        "it": "Matteo", "ru": "От Матфея", "zh": "马太福音", "ja": "マタイによる福音書", "ar": "متى",
        "el": "Κατά Ματθαίον", "eo": "Mateo", "fi": "Matteuksen evankeliumi", "ko": "마태복음",
        "ro": "Matei", "vi": "Ma-thi-ơ", "hi": "मत्ती", "id": "Matius",
        "pl": "Mateusza", "fa": "متی", "sw": "Mathayo", "th": "มัทธิว", "tr": "Matta"
    },
    "mc": {
        "pt": "Marcos", "en": "Mark", "es": "Marcos", "fr": "Marc", "de": "Markus",
        "it": "Marco", "ru": "От Марка", "zh": "马可福音", "ja": "マルコによる福音書", "ar": "مرقس",
        "el": "Κατά Μάρκον", "eo": "Marko", "fi": "Markuksen evankeliumi", "ko": "마가복음",
        "ro": "Marcu", "vi": "Mác", "hi": "मरकुस", "id": "Markus",
        "pl": "Marka", "fa": "مرقس", "sw": "Marko", "th": "มาระโก", "tr": "Markos"
    },
    "lc": {
        "pt": "Lucas", "en": "Luke", "es": "Lucas", "fr": "Luc", "de": "Lukas",
        "it": "Luca", "ru": "От Луки", "zh": "路加福音", "ja": "ルカによる福音書", "ar": "لوقا",
        "el": "Κατά Λουκάν", "eo": "Luko", "fi": "Luukkaan evankeliumi", "ko": "누가복음",
        "ro": "Luca", "vi": "Lu-ca", "hi": "लूका", "id": "Lukas",
        "pl": "Łukasza", "fa": "لوقا", "sw": "Luka", "th": "ลูกา", "tr": "Luka"
    },
    "jo": {
        "pt": "João", "en": "John", "es": "Juan", "fr": "Jean", "de": "Johannes",
        "it": "Giovanni", "ru": "От Иоанна", "zh": "约翰福音", "ja": "ヨハネによる福音書", "ar": "يوحنا",
        "el": "Κατά Ιωάννην", "eo": "Johano", "fi": "Johanneksen evankeliumi", "ko": "요한복음",
        "ro": "Ioan", "vi": "Giăng", "hi": "यूहन्ना", "id": "Yohanes",
        "pl": "Jana", "fa": "یوحنا", "sw": "Yohana", "th": "ยอห์น", "tr": "Yuhanna"
    },
    "at": {
        "pt": "Atos", "en": "Acts", "es": "Hechos", "fr": "Actes", "de": "Apostelgeschichte",
        "it": "Atti", "ru": "Деяния", "zh": "使徒行传", "ja": "使徒行伝", "ar": "أعمال الرسل",
        "el": "Πράξεις", "eo": "Agoj", "fi": "Apostolien teot", "ko": "사도행전",
        "ro": "Faptele Apostolilor", "vi": "Công Vụ", "hi": "प्रेरितों के काम", "id": "Kisah Para Rasul",
        "pl": "Dzieje Apostolskie", "fa": "اعمال رسولان", "sw": "Matendo", "th": "กิจการ", "tr": "Elçilerin İşleri"
    },
    "rm": {
        "pt": "Romanos", "en": "Romans", "es": "Romanos", "fr": "Romains", "de": "Römer",
        "it": "Romani", "ru": "К Римлянам", "zh": "罗马书", "ja": "ローマ人への手紙", "ar": "رومية",
        "el": "Προς Ρωμαίους", "eo": "Romanoj", "fi": "Roomalaiskirje", "ko": "로마서",
        "ro": "Romani", "vi": "Rô-ma", "hi": "रोमियों", "id": "Roma",
        "pl": "Rzymian", "fa": "رومیان", "sw": "Warumi", "th": "โรม", "tr": "Romalılar"
    },
    "1co": {
        "pt": "1 Coríntios", "en": "1 Corinthians", "es": "1 Corintios", "fr": "1 Corinthiens", "de": "1 Korinther",
        "it": "1 Corinzi", "ru": "1 Коринфянам", "zh": "哥林多前书", "ja": "コリント人への第一の手紙", "ar": "كورنثوس الأولى",
        "el": "Α' Κορινθίους", "eo": "1 Korintanoj", "fi": "1 Korinttilaiskirje", "ko": "고린도전서",
        "ro": "1 Corinteni", "vi": "1 Cô-rinh-tô", "hi": "1 कुरिन्थियों", "id": "1 Korintus",
        "pl": "1 Koryntian", "fa": "اول قرنتیان", "sw": "1 Wakorintho", "th": "1 โครินธ์", "tr": "1 Korintliler"
    },
    "2co": {
        "pt": "2 Coríntios", "en": "2 Corinthians", "es": "2 Corintios", "fr": "2 Corinthiens", "de": "2 Korinther",
        "it": "2 Corinzi", "ru": "2 Коринфянам", "zh": "哥林多后书", "ja": "コリント人への第二の手紙", "ar": "كورنثوس الثانية",
        "el": "Β' Κορινθίους", "eo": "2 Korintanoj", "fi": "2 Korinttilaiskirje", "ko": "고린도후서",
        "ro": "2 Corinteni", "vi": "2 Cô-rinh-tô", "hi": "2 कुरिन्थियों", "id": "2 Korintus",
        "pl": "2 Koryntian", "fa": "دوم قرنتیان", "sw": "2 Wakorintho", "th": "2 โครินธ์", "tr": "2 Korintliler"
    },
    "gl": {
        "pt": "Gálatas", "en": "Galatians", "es": "Gálatas", "fr": "Galates", "de": "Galater",
        "it": "Galati", "ru": "К Галатам", "zh": "加拉太书", "ja": "ガラテヤ人への手紙", "ar": "غلاطية",
        "el": "Προς Γαλάτας", "eo": "Galatoj", "fi": "Galatalaiskirje", "ko": "갈라디아서",
        "ro": "Galateni", "vi": "Ga-la-ti", "hi": "गलातियों", "id": "Galatia",
        "pl": "Galatów", "fa": "غلاطیان", "sw": "Wagalatia", "th": "กาลาเทีย", "tr": "Galatyalılar"
    },
    "ef": {
        "pt": "Efésios", "en": "Ephesians", "es": "Efesios", "fr": "Éphésiens", "de": "Epheser",
        "it": "Efesini", "ru": "К Ефесянам", "zh": "以弗所书", "ja": "エペソ人への手紙", "ar": "أفسس",
        "el": "Προς Εφεσίους", "eo": "Efesanoj", "fi": "Efesolaiskirje", "ko": "에베소서",
        "ro": "Efeseni", "vi": "Ê-phê-sô", "hi": "इफिसियों", "id": "Efesus",
        "pl": "Efezjan", "fa": "افسسیان", "sw": "Waefeso", "th": "เอเฟซัส", "tr": "Efesliler"
    },
    "fp": {
        "pt": "Filipenses", "en": "Philippians", "es": "Filipenses", "fr": "Philippiens", "de": "Philipper",
        "it": "Filippesi", "ru": "К Филиппийцам", "zh": "腓立比书", "ja": "ピリピ人への手紙", "ar": "فيلبي",
        "el": "Προς Φιλιππησίους", "eo": "Filipianoj", "fi": "Filippiläiskirje", "ko": "빌립보서",
        "ro": "Filipeni", "vi": "Phi-líp", "hi": "फिलिप्पियों", "id": "Filipi",
        "pl": "Filipian", "fa": "فیلیپیان", "sw": "Wafilipi", "th": "ฟีลิปปี", "tr": "Filipililer"
    },
    "cl": {
        "pt": "Colossenses", "en": "Colossians", "es": "Colosenses", "fr": "Colossiens", "de": "Kolosser",
        "it": "Colossesi", "ru": "К Колоссянам", "zh": "歌罗西书", "ja": "コロサイ人への手紙", "ar": "كولوسي",
        "el": "Προς Κολοσσαείς", "eo": "Koloseanoj", "fi": "Kolossalaiskirje", "ko": "골로새서",
        "ro": "Coloseni", "vi": "Cô-lô-se", "hi": "कुलुस्सियों", "id": "Kolose",
        "pl": "Kolosan", "fa": "کولسیان", "sw": "Wakolosai", "th": "โคโลสี", "tr": "Koloseliler"
    },
    "1cr": {
        "pt": "1 Crônicas", "en": "1 Chronicles", "es": "1 Crónicas", "fr": "1 Chroniques", "de": "1 Chronik",
        "it": "1 Cronache", "ru": "1 Паралипоменон", "zh": "历代志上", "ja": "歴代誌上", "ar": "أخبار الأيام الأول",
        "el": "Α' Παραλειπομένων", "eo": "1 Kroniko", "fi": "1 Aikakirja", "ko": "역대상",
        "ro": "1 Cronici", "vi": "1 Sử Ký", "hi": "1 इतिहास", "id": "1 Tawarikh",
        "pl": "1 Kronik", "fa": "اول تواریخ", "sw": "1 Mambo ya Nyakati", "th": "1 พงศาวดาร", "tr": "1 Tarihler"
    },
    "2cr": {
        "pt": "2 Crônicas", "en": "2 Chronicles", "es": "2 Crónicas", "fr": "2 Chroniques", "de": "2 Chronik",
        "it": "2 Cronache", "ru": "2 Паралипоменон", "zh": "历代志下", "ja": "歴代誌下", "ar": "أخبار الأيام الثاني",
        "el": "Β' Παραλειπομένων", "eo": "2 Kroniko", "fi": "2 Aikakirja", "ko": "역대하",
        "ro": "2 Cronici", "vi": "2 Sử Ký", "hi": "2 इतिहास", "id": "2 Tawarikh",
        "pl": "2 Kronik", "fa": "دوم تواریخ", "sw": "2 Mambo ya Nyakati", "th": "2 พงศาวดาร", "tr": "2 Tarihler"
    },
    "ed": {
        "pt": "Esdras", "en": "Ezra", "es": "Esdras", "fr": "Esdras", "de": "Esra",
        "it": "Esdra", "ru": "Ездра", "zh": "以斯拉记", "ja": "エズラ記", "ar": "عزرا",
        "el": "Έσδρας", "eo": "Ezra", "fi": "Esra", "ko": "에스라",
        "ro": "Ezra", "vi": "Ê-xơ-ra", "hi": "एज्रा", "id": "Ezra",
        "pl": "Ezdrasza", "fa": "عزرا", "sw": "Ezra", "th": "เอสรา", "tr": "Ezra"
    },
    "ne": {
        "pt": "Neemias", "en": "Nehemiah", "es": "Nehemías", "fr": "Néhémie", "de": "Nehemia",
        "it": "Neemia", "ru": "Неемия", "zh": "尼希米记", "ja": "ネヘミヤ記", "ar": "نحميا",
        "el": "Νεεμίας", "eo": "Neĥemja", "fi": "Nehemia", "ko": "느헤미야",
        "ro": "Neemia", "vi": "Nê-hê-mi", "hi": "नहेम्याह", "id": "Nehemia",
        "pl": "Nehemiasza", "fa": "نحمیا", "sw": "Nehemia", "th": "เนหะมีย์", "tr": "Nehemya"
    },
    "et": {
        "pt": "Ester", "en": "Esther", "es": "Ester", "fr": "Esther", "de": "Ester",
        "it": "Ester", "ru": "Есфирь", "zh": "以斯帖记", "ja": "エステル記", "ar": "أستير",
        "el": "Εσθήρ", "eo": "Ester", "fi": "Ester", "ko": "에스더",
        "ro": "Estera", "vi": "Ê-xơ-tê", "hi": "एस्तेर", "id": "Ester",
        "pl": "Estery", "fa": "استر", "sw": "Esta", "th": "เอสเธอร์", "tr": "Ester"
    },
    "job": {
        "pt": "Jó", "en": "Job", "es": "Job", "fr": "Job", "de": "Hiob",
        "it": "Giobbe", "ru": "Иов", "zh": "约伯记", "ja": "ヨブ記", "ar": "أيوب",
        "el": "Ιώβ", "eo": "Ijob", "fi": "Job", "ko": "욥기",
        "ro": "Iov", "vi": "Gióp", "hi": "अय्यूब", "id": "Ayub",
        "pl": "Hioba", "fa": "ایوب", "sw": "Ayubu", "th": "โยบ", "tr": "Eyüp"
    },
    "sl": {
        "pt": "Salmos", "en": "Psalms", "es": "Salmos", "fr": "Psaumes", "de": "Psalmen",
        "it": "Salmi", "ru": "Псалтирь", "zh": "诗篇", "ja": "詩篇", "ar": "المزامير",
        "el": "Ψαλμοί", "eo": "Psalmoj", "fi": "Psalmit", "ko": "시편",
        "ro": "Psalmi", "vi": "Thi Thiên", "hi": "भजन संहिता", "id": "Mazmur",
        "pl": "Psalmów", "fa": "مزامیر", "sw": "Zaburi", "th": "สดุดี", "tr": "Mezmurlar"
    },
    "pv": {
        "pt": "Provérbios", "en": "Proverbs", "es": "Proverbios", "fr": "Proverbes", "de": "Sprüche",
        "it": "Proverbi", "ru": "Притчи", "zh": "箴言", "ja": "箴言", "ar": "الأمثال",
        "el": "Παροιμίες", "eo": "Proverboj", "fi": "Sananlaskut", "ko": "잠언",
        "ro": "Proverbe", "vi": "Châm Ngôn", "hi": "नीतिवचन", "id": "Amsal",
        "pl": "Przysłów", "fa": "امثال", "sw": "Mithali", "th": "สุภาษิต", "tr": "Süleyman'ın Özdeyişleri"
    },
    "ec": {
        "pt": "Eclesiastes", "en": "Ecclesiastes", "es": "Eclesiastés", "fr": "Ecclésiaste", "de": "Prediger",
        "it": "Ecclesiaste", "ru": "Екклесиаст", "zh": "传道书", "ja": "伝道の書", "ar": "الجامعة",
        "el": "Εκκλησιαστής", "eo": "Kohelet", "fi": "Saarnaaja", "ko": "전도서",
        "ro": "Ecclesiast", "vi": "Truyền Đạo", "hi": "सभोपदेशक", "id": "Pengkhotbah",
        "pl": "Kaznodziei Salomona", "fa": "جامعه", "sw": "Mhubiri", "th": "ปัญญาจารย์", "tr": "Vaiz"
    },
    "ct": {
        "pt": "Cânticos", "en": "Song of Solomon", "es": "Cantares", "fr": "Cantique", "de": "Hohelied",
        "it": "Cantico", "ru": "Песня Песней", "zh": "雅歌", "ja": "雅歌", "ar": "نشيد الأنشاد",
        "el": "Άσμα Ασμάτων", "eo": "Kanto de Kantoj", "fi": "Laulujen laulu", "ko": "아가",
        "ro": "Cântarea Cântărilor", "vi": "Nhã Ca", "hi": "श्रेष्ठगीत", "id": "Kidung Agung",
        "pl": "Pieśń nad Pieśniami", "fa": "غزل غزلها", "sw": "Wimbo Ulio Bora", "th": "เพลงซาโลมอน", "tr": "Ezgiler Ezgisi"
    },
    "is": {
        "pt": "Isaías", "en": "Isaiah", "es": "Isaías", "fr": "Ésaïe", "de": "Jesaja",
        "it": "Isaia", "ru": "Исаия", "zh": "以赛亚书", "ja": "イザヤ書", "ar": "إشعياء",
        "el": "Ησαΐας", "eo": "Jesaja", "fi": "Jesaja", "ko": "이사야",
        "ro": "Isaia", "vi": "Ê-sai", "hi": "यशायाह", "id": "Yesaya",
        "pl": "Izajasza", "fa": "اشعیا", "sw": "Isaya", "th": "อิสยาห์", "tr": "Yeşaya"
    },
    "jr": {
        "pt": "Jeremias", "en": "Jeremiah", "es": "Jeremías", "fr": "Jérémie", "de": "Jeremia",
        "it": "Geremia", "ru": "Иеремия", "zh": "耶利米书", "ja": "エレミヤ書", "ar": "إرميا",
        "el": "Ιερεμίας", "eo": "Jeremia", "fi": "Jeremia", "ko": "예레미야",
        "ro": "Ieremia", "vi": "Giê-rê-mi", "hi": "यिर्मयाह", "id": "Yeremia",
        "pl": "Jeremiasza", "fa": "ارمیا", "sw": "Yeremia", "th": "เยเรมีย์", "tr": "Yeremya"
    },
    "lm": {
        "pt": "Lamentações", "en": "Lamentations", "es": "Lamentaciones", "fr": "Lamentations", "de": "Klagelieder",
        "it": "Lamentazioni", "ru": "Плач Иеремии", "zh": "耶利米哀歌", "ja": "哀歌", "ar": "مراثي إرميا",
        "el": "Θρήνοι", "eo": "Lamentoj", "fi": "Valitusvirret", "ko": "예레미야애가",
        "ro": "Plângerile lui Ieremia", "vi": "Ca Thương", "hi": "विलापगीत", "id": "Ratapan",
        "pl": "Lamentacji", "fa": "مراثی", "sw": "Maombolezo", "th": "เพลงคร่ำครวญ", "tr": "Ağıtlar"
    },
    "ez": {
        "pt": "Ezequiel", "en": "Ezekiel", "es": "Ezequiel", "fr": "Ézéchiel", "de": "Hesekiel",
        "it": "Ezechiele", "ru": "Иезекииль", "zh": "以西结书", "ja": "エゼキエル書", "ar": "حزقيال",
        "el": "Ιεζεκιήλ", "eo": "Jeĥezkel", "fi": "Hesekiel", "ko": "에스겔",
        "ro": "Ezechiel", "vi": "Ê-xê-chi-ên", "hi": "यहेजकेल", "id": "Yehezkiel",
        "pl": "Ezechiela", "fa": "حزقیال", "sw": "Ezekieli", "th": "เอเสเคียล", "tr": "Hezekiel"
    },
    "dn": {
        "pt": "Daniel", "en": "Daniel", "es": "Daniel", "fr": "Daniel", "de": "Daniel",
        "it": "Daniele", "ru": "Даниил", "zh": "但以理书", "ja": "ダニエル書", "ar": "دانيال",
        "el": "Δανιήλ", "eo": "Daniel", "fi": "Daniel", "ko": "다니엘",
        "ro": "Daniel", "vi": "Đa-ni-ên", "hi": "दानिय्येल", "id": "Daniel",
        "pl": "Daniela", "fa": "دانیال", "sw": "Danieli", "th": "ดาเนียล", "tr": "Daniel"
    },
    "os": {
        "pt": "Oséias", "en": "Hosea", "es": "Oseas", "fr": "Osée", "de": "Hosea",
        "it": "Osea", "ru": "Осия", "zh": "何西阿书", "ja": "ホセア書", "ar": "هوشع",
        "el": "Ωσηέ", "eo": "Hoŝea", "fi": "Hoosea", "ko": "호세아",
        "ro": "Osea", "vi": "Ô-sê", "hi": "होशे", "id": "Hosea",
        "pl": "Ozeasza", "fa": "هوشع", "sw": "Hosea", "th": "โฮเชยา", "tr": "Hoşea"
    },
    "jl": {
        "pt": "Joel", "en": "Joel", "es": "Joel", "fr": "Joël", "de": "Joel",
        "it": "Gioele", "ru": "Иоиль", "zh": "约珥书", "ja": "ヨエル書", "ar": "يوئيل",
        "el": "Ιωήλ", "eo": "Joel", "fi": "Joel", "ko": "요엘",
        "ro": "Ioel", "vi": "Giô-ên", "hi": "योएल", "id": "Yoel",
        "pl": "Joela", "fa": "یوئیل", "sw": "Yoeli", "th": "โยเอล", "tr": "Yoel"
    },
    "am": {
        "pt": "Amós", "en": "Amos", "es": "Amós", "fr": "Amos", "de": "Amos",
        "it": "Amos", "ru": "Амос", "zh": "阿摩司书", "ja": "アモス書", "ar": "عاموس",
        "el": "Αμώς", "eo": "Amos", "fi": "Aamos", "ko": "아모스",
        "ro": "Amos", "vi": "A-mốt", "hi": "आमोस", "id": "Amos",
        "pl": "Amosa", "fa": "عاموس", "sw": "Amosi", "th": "อาโมส", "tr": "Amos"
    },
    "ob": {
        "pt": "Obadias", "en": "Obadiah", "es": "Abdías", "fr": "Abdias", "de": "Obadja",
        "it": "Abdia", "ru": "Авдий", "zh": "俄巴底亚书", "ja": "オバデヤ書", "ar": "عوبديا",
        "el": "Αβδιού", "eo": "Obadja", "fi": "Obadja", "ko": "오바댜",
        "ro": "Obadia", "vi": "Áp-đia", "hi": "ओबद्याह", "id": "Obaja",
        "pl": "Abdiasza", "fa": "عوبدیا", "sw": "Obadia", "th": "โอบาดีห์", "tr": "Ovadya"
    },
    "jn": {
        "pt": "Jonas", "en": "Jonah", "es": "Jonás", "fr": "Jonas", "de": "Jona",
        "it": "Giona", "ru": "Иона", "zh": "约拿书", "ja": "ヨナ書", "ar": "يونان",
        "el": "Ιωνάς", "eo": "Jona", "fi": "Joona", "ko": "요나",
        "ro": "Iona", "vi": "Giô-na", "hi": "योना", "id": "Yunus",
        "pl": "Jonasza", "fa": "یونس", "sw": "Yona", "th": "โยนาห์", "tr": "Yunus"
    },
    "mq": {
        "pt": "Miquéias", "en": "Micah", "es": "Miqueas", "fr": "Michée", "de": "Micha",
        "it": "Michea", "ru": "Михей", "zh": "弥迦书", "ja": "ミカ書", "ar": "ميخا",
        "el": "Μιχαίας", "eo": "Miĥa", "fi": "Miika", "ko": "미가",
        "ro": "Mica", "vi": "Mi-chê", "hi": "मीका", "id": "Mikha",
        "pl": "Micheasza", "fa": "میکاه", "sw": "Mika", "th": "มีคาห์", "tr": "Mika"
    },
    "na": {
        "pt": "Naum", "en": "Nahum", "es": "Nahúm", "fr": "Nahum", "de": "Nahum",
        "it": "Nahum", "ru": "Наум", "zh": "那鸿书", "ja": "ナホム書", "ar": "ناحوم",
        "el": "Ναούμ", "eo": "Naĥum", "fi": "Nahum", "ko": "나훔",
        "ro": "Naum", "vi": "Na-hum", "hi": "नहूम", "id": "Nahum",
        "pl": "Nahuma", "fa": "ناحوم", "sw": "Nahumu", "th": "นาฮูม", "tr": "Nahum"
    },
    "hc": {
        "pt": "Habacuque", "en": "Habakkuk", "es": "Habacuc", "fr": "Habacuc", "de": "Habakuk",
        "it": "Abacuc", "ru": "Аввакум", "zh": "哈巴谷书", "ja": "ハバクク書", "ar": "حبقوق",
        "el": "Αββακούμ", "eo": "Ĥabakuk", "fi": "Habakuk", "ko": "하박국",
        "ro": "Habacuc", "vi": "Ha-ba-cúc", "hi": "हबक्कूक", "id": "Habakuk",
        "pl": "Habakuka", "fa": "حبقوق", "sw": "Habakuki", "th": "ฮาบากุก", "tr": "Habakkuk"
    },
    "sf": {
        "pt": "Sofonias", "en": "Zephaniah", "es": "Sofonías", "fr": "Sophonie", "de": "Zefanja",
        "it": "Sofonia", "ru": "Софония", "zh": "西番雅书", "ja": "ゼパニヤ書", "ar": "صفنيا",
        "el": "Σοφονίας", "eo": "Cefanja", "fi": "Sefanja", "ko": "스바냐",
        "ro": "Tefania", "vi": "Sô-phô-ni", "hi": "सपन्याह", "id": "Zefanya",
        "pl": "Sofoniasza", "fa": "صفنیا", "sw": "Sefania", "th": "เศฟันยาห์", "tr": "Tsefanya"
    },
    "ag": {
        "pt": "Ageu", "en": "Haggai", "es": "Hageo", "fr": "Aggée", "de": "Haggai",
        "it": "Aggeo", "ru": "Аггей", "zh": "哈该书", "ja": "ハガイ書", "ar": "حجي",
        "el": "Αγγαίος", "eo": "Ĥagaj", "fi": "Haggai", "ko": "학개",
        "ro": "Hagai", "vi": "A-ghê", "hi": "हाग्गै", "id": "Hagai",
        "pl": "Aggeusza", "fa": "حجی", "sw": "Hagai", "th": "ฮักกัย", "tr": "Hagay"
    },
    "zc": {
        "pt": "Zacarias", "en": "Zechariah", "es": "Zacarías", "fr": "Zacharie", "de": "Sacharja",
        "it": "Zaccaria", "ru": "Захария", "zh": "撒迦利亚书", "ja": "ゼカリヤ書", "ar": "زكريا",
        "el": "Ζαχαρίας", "eo": "Zeĥarja", "fi": "Sakarja", "ko": "스가랴",
        "ro": "Zaharia", "vi": "Xa-cha-ri", "hi": "जकर्याह", "id": "Zakharia",
        "pl": "Zachariasza", "fa": "زکریا", "sw": "Zekaria", "th": "เศคาริยาห์", "tr": "Zekeriya"
    },
    "ml": {
        "pt": "Malaquias", "en": "Malachi", "es": "Malaquías", "fr": "Malachie", "de": "Maleachi",
        "it": "Malachia", "ru": "Малахия", "zh": "玛拉基书", "ja": "マラキ書", "ar": "ملاخي",
        "el": "Μαλαχίας", "eo": "Malaĥi", "fi": "Malakia", "ko": "말라기",
        "ro": "Maleahi", "vi": "Ma-la-chi", "hi": "मलाकी", "id": "Maleakhi",
        "pl": "Malachiasza", "fa": "ملاکی", "sw": "Malaki", "th": "มาลาคี", "tr": "Malaki"
    },
    "1ts": {
        "pt": "1 Tessalonicenses", "en": "1 Thessalonians", "es": "1 Tesalonicenses", "fr": "1 Thessaloniciens", "de": "1 Thessalonicher",
        "it": "1 Tessalonicesi", "ru": "1 Фессалоникийцам", "zh": "帖撒罗尼迦前书", "ja": "テサロニケ人への第一の手紙", "ar": "تسالونيكي الأولى",
        "el": "Α' Θεσσαλονικείς", "eo": "1 Tesalonikanoj", "fi": "1 Tessalonikalaiskirje", "ko": "데살로니가전서",
        "ro": "1 Tesaloniceni", "vi": "1 Tê-sa-lô-ni-ca", "hi": "1 थिस्सलुनीकियों", "id": "1 Tesalonika",
        "pl": "1 Tesaloniczan", "fa": "اول تسالونیکیان", "sw": "1 Wathesalonike", "th": "1 เธสะโลนิกา", "tr": "1 Selanikl iler"
    },
    "2ts": {
        "pt": "2 Tessalonicenses", "en": "2 Thessalonians", "es": "2 Tesalonicenses", "fr": "2 Thessaloniciens", "de": "2 Thessalonicher",
        "it": "2 Tessalonicesi", "ru": "2 Фессалоникийцам", "zh": "帖撒罗尼迦后书", "ja": "テサロニケ人への第二の手紙", "ar": "تسالونيكي الثانية",
        "el": "Β' Θεσσαλονικείς", "eo": "2 Tesalonikanoj", "fi": "2 Tessalonikalaiskirje", "ko": "데살로니가후서",
        "ro": "2 Tesaloniceni", "vi": "2 Tê-sa-lô-ni-ca", "hi": "2 थिस्सलुनीकियों", "id": "2 Tesalonika",
        "pl": "2 Tesaloniczan", "fa": "دوم تسالونیکیان", "sw": "2 Wathesalonike", "th": "2 เธสะโลนิกา", "tr": "2 Selanikliler"
    },
    "1tm": {
        "pt": "1 Timóteo", "en": "1 Timothy", "es": "1 Timoteo", "fr": "1 Timothée", "de": "1 Timotheus",
        "it": "1 Timoteo", "ru": "1 Тимофею", "zh": "提摩太前书", "ja": "テモテへの第一の手紙", "ar": "تيموثاوس الأولى",
        "el": "Α' Τιμόθεον", "eo": "1 Timoteo", "fi": "1 Timoteuskirje", "ko": "디모데전서",
        "ro": "1 Timotei", "vi": "1 Ti-mô-thê", "hi": "1 तीमुथियुस", "id": "1 Timotius",
        "pl": "1 Tymoteusza", "fa": "اول تیموتائوس", "sw": "1 Timotheo", "th": "1 ทิโมธี", "tr": "1 Timoteos"
    },
    "2tm": {
        "pt": "2 Timóteo", "en": "2 Timothy", "es": "2 Timoteo", "fr": "2 Timothée", "de": "2 Timotheus",
        "it": "2 Timoteo", "ru": "2 Тимофею", "zh": "提摩太后书", "ja": "テモテへの第二の手紙", "ar": "تيموثاوس الثانية",
        "el": "Β' Τιμόθεον", "eo": "2 Timoteo", "fi": "2 Timoteuskirje", "ko": "디모데후서",
        "ro": "2 Timotei", "vi": "2 Ti-mô-thê", "hi": "2 तीमुथियुस", "id": "2 Timotius",
        "pl": "2 Tymoteusza", "fa": "دوم تیموتائوس", "sw": "2 Timotheo", "th": "2 ทิโมธี", "tr": "2 Timoteos"
    },
    "tt": {
        "pt": "Tito", "en": "Titus", "es": "Tito", "fr": "Tite", "de": "Titus",
        "it": "Tito", "ru": "К Титу", "zh": "提多书", "ja": "テトスへの手紙", "ar": "تيطس",
        "el": "Τίτον", "eo": "Tito", "fi": "Titus", "ko": "디도서",
        "ro": "Tit", "vi": "Tít", "hi": "तीतुस", "id": "Titus",
        "pl": "Tytusa", "fa": "تیطس", "sw": "Tito", "th": "ทิตัส", "tr": "Titus"
    },
    "fm": {
        "pt": "Filemom", "en": "Philemon", "es": "Filemón", "fr": "Philémon", "de": "Philemon",
        "it": "Filemone", "ru": "К Филимону", "zh": "腓利门书", "ja": "ピレモンへの手紙", "ar": "فليمون",
        "el": "Φιλήμονα", "eo": "Filemon", "fi": "Filemon", "ko": "빌레몬서",
        "ro": "Filimon", "vi": "Phi-lê-môn", "hi": "फिलेमोन", "id": "Filemon",
        "pl": "Filemona", "fa": "فیلیمون", "sw": "Filemoni", "th": "ฟีเลโมน", "tr": "Filemon"
    },
    "hb": {
        "pt": "Hebreus", "en": "Hebrews", "es": "Hebreos", "fr": "Hébreux", "de": "Hebräer",
        "it": "Ebrei", "ru": "К Евреям", "zh": "希伯来书", "ja": "ヘブル人への手紙", "ar": "العبرانيين",
        "el": "Προς Εβραίους", "eo": "Hebreoj", "fi": "Heprealaiskirje", "ko": "히브리서",
        "ro": "Evrei", "vi": "Hê-bơ-rơ", "hi": "इब्रानियों", "id": "Ibrani",
        "pl": "Hebrajczyków", "fa": "عبرانیان", "sw": "Waebrania", "th": "ฮีบรู", "tr": "İbraniler"
    },
    "tg": {
        "pt": "Tiago", "en": "James", "es": "Santiago", "fr": "Jacques", "de": "Jakobus",
        "it": "Giacomo", "ru": "Иакова", "zh": "雅各书", "ja": "ヤコブの手紙", "ar": "يعقوب",
        "el": "Ιακώβου", "eo": "Jakobo", "fi": "Jaakobin kirje", "ko": "야고보서",
        "ro": "Iacov", "vi": "Gia-cơ", "hi": "याकूब", "id": "Yakobus",
        "pl": "Jakuba", "fa": "یعقوب", "sw": "Yakobo", "th": "ยากอบ", "tr": "Yakup"
    },
    "1pe": {
        "pt": "1 Pedro", "en": "1 Peter", "es": "1 Pedro", "fr": "1 Pierre", "de": "1 Petrus",
        "it": "1 Pietro", "ru": "1 Петра", "zh": "彼得前书", "ja": "ペテロの第一の手紙", "ar": "بطرس الأولى",
        "el": "Α' Πέτρου", "eo": "1 Petro", "fi": "1 Pietarin kirje", "ko": "베드로전서",
        "ro": "1 Petru", "vi": "1 Phi-e-rơ", "hi": "1 पतरस", "id": "1 Petrus",
        "pl": "1 Piotra", "fa": "اول پطرس", "sw": "1 Petro", "th": "1 เปโตร", "tr": "1 Petrus"
    },
    "2pe": {
        "pt": "2 Pedro", "en": "2 Peter", "es": "2 Pedro", "fr": "2 Pierre", "de": "2 Petrus",
        "it": "2 Pietro", "ru": "2 Петра", "zh": "彼得后书", "ja": "ペテロの第二の手紙", "ar": "بطرس الثانية",
        "el": "Β' Πέτρου", "eo": "2 Petro", "fi": "2 Pietarin kirje", "ko": "베드로후서",
        "ro": "2 Petru", "vi": "2 Phi-e-rơ", "hi": "2 पतरस", "id": "2 Petrus",
        "pl": "2 Piotra", "fa": "دوم پطرس", "sw": "2 Petro", "th": "2 เปโตร", "tr": "2 Petrus"
    },
    "1jo": {
        "pt": "1 João", "en": "1 John", "es": "1 Juan", "fr": "1 Jean", "de": "1 Johannes",
        "it": "1 Giovanni", "ru": "1 Иоанна", "zh": "约翰一书", "ja": "ヨハネの第一の手紙", "ar": "يوحنا الأولى",
        "el": "Α' Ιωάννου", "eo": "1 Johano", "fi": "1 Johanneksen kirje", "ko": "요한일서",
        "ro": "1 Ioan", "vi": "1 Giăng", "hi": "1 यूहन्ना", "id": "1 Yohanes",
        "pl": "1 Jana", "fa": "اول یوحنا", "sw": "1 Yohana", "th": "1 ยอห์น", "tr": "1 Yuhanna"
    },
    "2jo": {
        "pt": "2 João", "en": "2 John", "es": "2 Juan", "fr": "2 Jean", "de": "2 Johannes",
        "it": "2 Giovanni", "ru": "2 Иоанна", "zh": "约翰二书", "ja": "ヨハネの第二の手紙", "ar": "يوحنا الثانية",
        "el": "Β' Ιωάννου", "eo": "2 Johano", "fi": "2 Johanneksen kirje", "ko": "요한이서",
        "ro": "2 Ioan", "vi": "2 Giăng", "hi": "2 यूहन्ना", "id": "2 Yohanes",
        "pl": "2 Jana", "fa": "دوم یوحنا", "sw": "2 Yohana", "th": "2 ยอห์น", "tr": "2 Yuhanna"
    },
    "3jo": {
        "pt": "3 João", "en": "3 John", "es": "3 Juan", "fr": "3 Jean", "de": "3 Johannes",
        "it": "3 Giovanni", "ru": "3 Иоанна", "zh": "约翰三书", "ja": "ヨハネの第三の手紙", "ar": "يوحنا الثالثة",
        "el": "Γ' Ιωάννου", "eo": "3 Johano", "fi": "3 Johanneksen kirje", "ko": "요한삼서",
        "ro": "3 Ioan", "vi": "3 Giăng", "hi": "3 यूहन्ना", "id": "3 Yohanes",
        "pl": "3 Jana", "fa": "سوم یوحنا", "sw": "3 Yohana", "th": "3 ยอห์น", "tr": "3 Yuhanna"
    },
    "jd": {
        "pt": "Judas", "en": "Jude", "es": "Judas", "fr": "Jude", "de": "Judas",
        "it": "Giuda", "ru": "Иуды", "zh": "犹大书", "ja": "ユダの手紙", "ar": "يهوذا",
        "el": "Ιούδα", "eo": "Jehudo", "fi": "Juudaksen kirje", "ko": "유다서",
        "ro": "Iuda", "vi": "Giu-đe", "hi": "यहूदा", "id": "Yudas",
        "pl": "Judy", "fa": "یهودا", "sw": "Yuda", "th": "ยูดา", "tr": "Yahuda"
    },
    "ap": {
        "pt": "Apocalipse", "en": "Revelation", "es": "Apocalipsis", "fr": "Apocalypse", "de": "Offenbarung",
        "it": "Apocalisse", "ru": "Откровение", "zh": "启示录", "ja": "ヨハネの黙示録", "ar": "الرؤيا",
        "el": "Αποκάλυψη", "eo": "Apokalipso", "fi": "Ilmestyskirja", "ko": "요한계시록",
        "ro": "Apocalipsa", "vi": "Khải Huyền", "hi": "प्रकाशितवाक्य", "id": "Wahyu",
        "pl": "Apokalipsa", "fa": "مکاشفه", "sw": "Ufunuo", "th": "วิวรณ์", "tr": "Vahiy"
    }
}


def get_book_name(abbrev: str, lang_code: str, fallback: str = None) -> str:
    """
    Obtém o nome traduzido de um livro bíblico.
    
    Args:
        abbrev: Abreviação do livro (ex: "gn", "mt")
        lang_code: Código do idioma (ex: "pt", "ar", "ja")
        fallback: Nome alternativo caso não encontre tradução
    
    Returns:
        Nome traduzido do livro ou fallback
    """
    abbrev_lower = abbrev.lower() if abbrev else ""
    
    if abbrev_lower in BOOK_NAMES:
        book_translations = BOOK_NAMES[abbrev_lower]
        if lang_code in book_translations:
            return book_translations[lang_code]
        # Fallback para inglês se o idioma não existir
        if "en" in book_translations:
            return book_translations["en"]
    
    # Se não encontrar, retorna o fallback ou a abreviação capitalizada
    return fallback or abbrev.upper()
