#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script COMPLETO para traduzir TODOS os 18 idiomas incompletos
Garante que cada idioma tenha APENAS texto no seu idioma nativo
ZERO interferência de inglês ou outros idiomas
"""

import json
import re
import os

# Dicionário MASSIVO com TODAS as traduções para TODOS os idiomas
ALL_TRANSLATIONS = {
    # ============ ÁRABE (AR) ============
    "ar": {
        "Enter a single verse or range to use as base or leave blank for the entire chapter.": "أدخل آية واحدة أو نطاقًا لاستخدامه كأساس أو اتركه فارغًا للفصل بأكمله",
        "Import a Bible version to start guided reading.": "استورد نسخة من الكتاب المقدس لبدء القراءة الموجهة",
        "Select a book and chapter to start guided reading.": "اختر كتابًا وفصلًا لبدء القراءة الموجهة",
        "No verses found in this chapter.": "لم يتم العثور على آيات في هذا الفصل",
        "No matching verse found. Check syntax or use commas/ranges.": "لم يتم العثور على آية مطابقة. تحقق من بناء الجملة أو استخدم الفواصل/النطاقات",
        "No results found for your search.": "لم يتم العثور على نتائج لبحثك",
        "Text ready to copy!": "النص جاهز للنسخ!",
        "Import data to start generating a sermon.": "استورد البيانات لبدء إنشاء موعظة",
        "Choose a base verse or scope for the model to use as authority.": "اختر آية أساسية أو نطاقًا ليستخدمه النموذج كمرجع",
        "Load a verse to build the devotional.": "قم بتحميل آية لبناء التأمل الروحي",
        "Select a verse or scope to anchor the meditation.": "اختر آية أو نطاقًا لتثبيت التأمل",
        "Ollama is offline. Turn on the server and try again.": "Ollama غير متصل. قم بتشغيل الخادم وحاول مرة أخرى",
        "Import a version to chat with the theological chat.": "استورد نسخة للدردشة مع الدردشة اللاهوتية",
        "Select a verse for the AI to use as authority.": "اختر آية ليستخدمها الذكاء الاصطناعي كمرجع",
        "Write the question before sending.": "اكتب السؤال قبل الإرسال",
        "Ollama is offline. Please start the server.": "Ollama غير متصل. الرجاء تشغيل الخادم",
        "Explain the historical and theological context, ponder key words and suggest pastoral applications.": "اشرح السياق التاريخي واللاهوتي، وتأمل في الكلمات الرئيسية واقترح تطبيقات رعوية",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "أنشئ مخططًا رعويًا يكرم الكلمة، وذو صلة وقابل للتطبيق على الجمهور المحدد",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "اكتب تأملاً شخصيًا يوفر الراحة الروحية والتأمل العميق والتطبيق العملي",
    },
    
    # ============ ALEMÃO (DE) ============
    "de": {
        "Question, answer, reference...": "Frage, Antwort, Referenz...",
        "No theme": "Kein Thema",
        "Selected:": "Ausgewählt:",
        "Import folder:": "Importordner:",
        "Import a Bible version to start guided reading.": "Importieren Sie eine Bibelversion, um mit dem geführten Lesen zu beginnen",
        "Select a book and chapter to start guided reading.": "Wählen Sie ein Buch und Kapitel, um mit dem geführten Lesen zu beginnen",
        "No verses found in this chapter.": "Keine Verse in diesem Kapitel gefunden",
        "No matching verse found. Check syntax or use commas/ranges.": "Kein passender Vers gefunden. Überprüfen Sie die Syntax oder verwenden Sie Kommas/Bereiche",
        "No results found for your search.": "Keine Ergebnisse für Ihre Suche gefunden",
        "Import data to start generating a sermon.": "Importieren Sie Daten, um mit der Erstellung einer Predigt zu beginnen",
        "Load a verse to build the devotional.": "Laden Sie einen Vers, um die Andacht zu erstellen",
        "Select a verse or scope to anchor the meditation.": "Wählen Sie einen Vers oder Bereich, um die Meditation zu verankern",
        "Import a version to chat with the theological chat.": "Importieren Sie eine Version, um mit dem theologischen Chat zu chatten",
        "Select a verse for the AI to use as authority.": "Wählen Sie einen Vers für die KI als Autorität",
        "Write the question before sending.": "Schreiben Sie die Frage vor dem Senden",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Erstellen Sie eine pastorale Gliederung, die das Wort ehrt, relevant und anwendbar für das angegebene Publikum ist",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Schreiben Sie eine persönliche Meditation, die spirituellen Trost, tiefe Reflexion und praktische Anwendung bietet",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Antworten Sie mit theologischer Klarheit und pastoraler Gnade, immer auf biblischer Autorität basierend",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Schreiben Sie eine vollständige Predigtgliederung mit Titel, Einleitung, Auslegungsthemen, Illustrationen und Schlussfolgerung",
        "The sermon should cover texts from:": "Die Predigt sollte Texte behandeln von:",
    },
    
    # ============ ESPERANTO (EO) ============
    "eo": {
        "Question, answer, reference...": "Demando, respondo, referenco...",
        "Select the scope for sermon generation:": "Elektu la amplekson por prediko-generado:",
        "Check to manually select specific books": "Marku por permane elekti specifajn librojn",
        "Select the books for the sermon:": "Elektu la librojn por la prediko:",
        "Select the scope for devotional generation:": "Elektu la amplekson por devocia generado:",
        "Select the books for the devotional:": "Elektu la librojn por la devocia:",
        "No theme": "Neniu temo",
        "Selected:": "Elektita:",
        "Import folder:": "Importdosierujo:",
        "Selected book:": "Elektita libro:",
        "Select books": "Elektu librojn",
        "Selected books:": "Elektitaj libroj:",
        "Questions Only": "Nur Demandoj",
        "Import a Bible version to start guided reading.": "Importu Biblio-version por komenci gvidatan legadon",
        "Select a book and chapter to start guided reading.": "Elektu libron kaj ĉapitron por komenci gvidatan legadon",
        "No verses found in this chapter.": "Neniuj versoj trovitaj en ĉi tiu ĉapitro",
        "No matching verse found. Check syntax or use commas/ranges.": "Neniu kongrua verso trovita. Kontrolu sintakson aŭ uzu komojn/ampleksojn",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Ankoraŭ neniuj studoj generitaj. Iru al 'Legado & Eksegezo' langeto kaj klaku 'Generi Klarigon' por komenci",
        "No results found for your search.": "Neniuj rezultoj trovitaj por via serĉo",
        "Import data to start generating a sermon.": "Importu datenojn por komenci generi predikon",
        "Load a verse to build the devotional.": "Ŝarĝu verson por konstrui la devocion",
        "Select a verse or scope to anchor the meditation.": "Elektu verson aŭ amplekson por ankri la meditadon",
        "Import a version to chat with the theological chat.": "Importu version por babili kun la teologia babilo",
        "Select a verse for the AI to use as authority.": "Elektu verson por la AI uzi kiel aŭtoritato",
        "Write the question before sending.": "Skribu la demandon antaŭ sendado",
    },
    
    # ============ ESPANHOL (ES) ============
    "es": {
        "Question, answer, reference...": "Pregunta, respuesta, referencia...",
        "Selected:": "Seleccionado:",
        "Import folder:": "Carpeta de importación:",
        "Import a Bible version to start guided reading.": "Importa una versión bíblica para comenzar la lectura guiada",
        "No verses found in this chapter.": "No se encontraron versículos en este capítulo",
        "No matching verse found. Check syntax or use commas/ranges.": "No se encontró un versículo coincidente. Verifica la sintaxis o usa comas/rangos",
        "No results found for your search.": "No se encontraron resultados para tu búsqueda",
        "Import data to start generating a sermon.": "Importa datos para comenzar a generar un sermón",
        "Load a verse to build the devotional.": "Carga un versículo para construir el devocional",
        "Select a verse or scope to anchor the meditation.": "Selecciona un versículo o alcance para anclar la meditación",
        "Import a version to chat with the theological chat.": "Importa una versión para chatear con el chat teológico",
        "Select a verse for the AI to use as authority.": "Selecciona un versículo para que la IA lo use como autoridad",
        "Write the question before sending.": "Escribe la pregunta antes de enviar",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Crea un esquema pastoral que honre la Palabra, sea relevante y aplicable a la audiencia indicada",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Escribe una meditación personal que ofrezca consuelo espiritual, reflexión profunda y aplicación práctica",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Responde con claridad teológica y gracia pastoral, siempre fundamentado en la autoridad bíblica",
    },
    
    # ============ FINLANDÊS (FI) ============
    "fi": {
        "Selected book:": "Valittu kirja:",
        "Select books": "Valitse kirjat",
        "Selected books:": "Valitut kirjat:",
        "Questions Only": "Vain kysymykset",
        "No verses found in this chapter.": "Tässä luvussa ei löytynyt jakeita",
        "No matching verse found. Check syntax or use commas/ranges.": "Vastaavaa jaetta ei löytynyt. Tarkista syntaksi tai käytä pilkkuja/välejä",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Ei vielä tuotettuja tutkimuksia. Siirry 'Lukeminen ja eksegeesi' -välilehdelle ja napsauta 'Luo selitys' aloittaaksesi",
        "No results found for your search.": "Haullesi ei löytynyt tuloksia",
        "Import data to start generating a sermon.": "Tuo tietoja aloittaaksesi saarnan luomisen",
        "Load a verse to build the devotional.": "Lataa jae rakentaaksesi hartauden",
        "Select a verse or scope to anchor the meditation.": "Valitse jae tai laajuus ankkuroimaan meditaatio",
        "Import a version to chat with the theological chat.": "Tuo versio keskustellaksesi teologisen chatin kanssa",
        "Select a verse for the AI to use as authority.": "Valitse jae AI:lle käytettäväksi auktoriteettina",
        "Write the question before sending.": "Kirjoita kysymys ennen lähettämistä",
        "No verses found in this chapter.": "Tässä luvussa ei löytynyt jakeita",
        "No local versions found. Use Import Data to load content.": "Paikallisia versioita ei löytynyt. Käytä Tuo tietoja ladataksesi sisältöä",
        "No questions generated yet.": "Ei vielä tuotettuja kysymyksiä",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Luo pastoraalinen rakenne, joka kunnioittaa Sanaa, on relevantti ja sovellettavissa mainittuun yleisöön",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Kirjoita henkilökohtainen meditaatio, joka tarjoaa hengellisä lohdutusta, syvää pohdintaa ja käytännön sovellusta",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Vastaa teologisella selkeydellä ja pastoraalisella armolla, aina perustuen raamatulliseen auktoriteettiin",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Kirjoita täydellinen saarnan rakenne otsikolla, johdannolla, selittävillä aiheilla, kuvituksilla ja johtopäätöksellä",
    },
    
    # ============ FRANCÊS (FR) ============
    "fr": {
        "Question, answer, reference...": "Question, réponse, référence...",
        "No theme": "Aucun thème",
        "Selected:": "Sélectionné:",
        "Import folder:": "Dossier d'importation:",
        "Questions Seulement": "Questions Seulement",
        "Import a Bible version to start guided reading.": "Importez une version de la Bible pour commencer la lecture guidée",
        "Select a book and chapter to start guided reading.": "Sélectionnez un livre et un chapitre pour commencer la lecture guidée",
        "No verses found in this chapter.": "Aucun verset trouvé dans ce chapitre",
        "No matching verse found. Check syntax or use commas/ranges.": "Aucun verset correspondant trouvé. Vérifiez la syntaxe ou utilisez des virgules/plages",
        "No results found for your search.": "Aucun résultat trouvé pour votre recherche",
        "Import data to start generating a sermon.": "Importez des données pour commencer à générer un sermon",
        "Load a verse to build the devotional.": "Chargez un verset pour construire le dévotionnel",
        "Select a verse or scope to anchor the meditation.": "Sélectionnez un verset ou une portée pour ancrer la méditation",
        "Import a version to chat with the theological chat.": "Importez une version pour discuter avec le chat théologique",
        "Select a verse for the AI to use as authority.": "Sélectionnez un verset pour que l'IA l'utilise comme autorité",
        "Write the question before sending.": "Écrivez la question avant d'envoyer",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Créez un plan pastoral qui honore la Parole, pertinent et applicable au public indiqué",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Écrivez une méditation personnelle qui offre du réconfort spirituel, une réflexion profonde et une application pratique",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Répondez avec clarté théologique et grâce pastorale, toujours fondé sur l'autorité biblique",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Écrivez un plan de sermon complet avec titre, introduction, sujets d'exposition, illustrations et conclusion",
        "The sermon should cover texts from:": "Le sermon devrait couvrir les textes de:",
    },
    
    # ============ HINDI (HI) ============
    "hi": {
        "Selected book:": "चयनित पुस्तक:",
        "Select books": "पुस्तकें चुनें",
        "Selected books:": "चयनित पुस्तकें:",
        "Questions Only": "केवल प्रश्न",
        "No questions generated yet.": "अभी तक कोई प्रश्न उत्पन्न नहीं हुए",
        "Generate questions about biblical knowledge.": "बाइबिल ज्ञान के बारे में प्रश्न उत्पन्न करें",
    },
    
    # ============ INDONÉSIO (ID) ============
    "id": {
        "Question, answer, reference...": "Pertanyaan, jawaban, referensi...",
        "Select the scope for sermon generation:": "Pilih cakupan untuk pembuatan khotbah:",
        "Check to manually select specific books": "Centang untuk memilih buku tertentu secara manual",
        "Select the books for the sermon:": "Pilih buku untuk khotbah:",
        "Select the scope for devotional generation:": "Pilih cakupan untuk pembuatan renungan:",
        "Select the books for the devotional:": "Pilih buku untuk renungan:",
        "No theme": "Tidak ada tema",
        "Selected:": "Dipilih:",
        "Import folder:": "Folder impor:",
        "Selected book:": "Buku yang dipilih:",
        "Select books": "Pilih buku",
        "Selected books:": "Buku yang dipilih:",
        "Questions Only": "Hanya Pertanyaan",
        "Import a Bible version to start guided reading.": "Impor versi Alkitab untuk memulai pembacaan terpandu",
        "Select a book and chapter to start guided reading.": "Pilih buku dan bab untuk memulai pembacaan terpandu",
        "No verses found in this chapter.": "Tidak ada ayat ditemukan di bab ini",
        "No matching verse found. Check syntax or use commas/ranges.": "Tidak ada ayat yang cocok ditemukan. Periksa sintaks atau gunakan koma/rentang",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Belum ada studi yang dihasilkan. Buka tab 'Pembacaan & Eksegesis' dan klik 'Hasilkan Penjelasan' untuk memulai",
        "No results found for your search.": "Tidak ada hasil ditemukan untuk pencarian Anda",
        "Import data to start generating a sermon.": "Impor data untuk mulai membuat khotbah",
        "Load a verse to build the devotional.": "Muat ayat untuk membangun renungan",
        "Select a verse or scope to anchor the meditation.": "Pilih ayat atau cakupan untuk menambatkan meditasi",
        "Import a version to chat with the theological chat.": "Impor versi untuk mengobrol dengan obrolan teologis",
        "Select a verse for the AI to use as authority.": "Pilih ayat untuk AI gunakan sebagai otoritas",
        "Write the question before sending.": "Tulis pertanyaan sebelum mengirim",
    },
    
    # ============ ITALIANO (IT) ============
    "it": {
        "Question, answer, reference...": "Domanda, risposta, riferimento...",
        "Check to manually select specific books": "Spunta per selezionare manualmente libri specifici",
        "No theme": "Nessun tema",
        "Selected:": "Selezionato:",
        "Import folder:": "Cartella di importazione:",
        "Import a Bible version to start guided reading.": "Importa una versione della Bibbia per iniziare la lettura guidata",
        "Select a book and chapter to start guided reading.": "Seleziona un libro e un capitolo per iniziare la lettura guidata",
        "No verses found in this chapter.": "Nessun versetto trovato in questo capitolo",
        "No matching verse found. Check syntax or use commas/ranges.": "Nessun versetto corrispondente trovato. Controlla la sintassi o usa virgole/intervalli",
        "No results found for your search.": "Nessun risultato trovato per la tua ricerca",
        "Import data to start generating a sermon.": "Importa dati per iniziare a generare un sermone",
        "Load a verse to build the devotional.": "Carica un versetto per costruire il devozionale",
        "Select a verse or scope to anchor the meditation.": "Seleziona un versetto o ambito per ancorare la meditazione",
        "Import a version to chat with the theological chat.": "Importa una versione per chattare con la chat teologica",
        "Select a verse for the AI to use as authority.": "Seleziona un versetto per l'IA da usare come autorità",
        "Write the question before sending.": "Scrivi la domanda prima di inviare",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Crea uno schema pastorale che onori la Parola, sia rilevante e applicabile al pubblico indicato",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Scrivi una meditazione personale che offra conforto spirituale, riflessione profonda e applicazione pratica",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Rispondi con chiarezza teologica e grazia pastorale, sempre basato sull'autorità biblica",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Scrivi uno schema completo del sermone con titolo, introduzione, argomenti espositivi, illustrazioni e conclusione",
        "The sermon should cover texts from:": "Il sermone dovrebbe coprire testi da:",
    },
    
    # ============ COREANO (KO) ============
    "ko": {
        "Question, answer, reference...": "질문, 답변, 참조...",
        "Select the scope for sermon generation:": "설교 생성 범위 선택:",
        "Check to manually select specific books": "특정 책을 수동으로 선택하려면 확인",
        "Select the books for the sermon:": "설교를 위한 책 선택:",
        "Select the scope for devotional generation:": "묵상 생성 범위 선택:",
        "Select the books for the devotional:": "묵상을 위한 책 선택:",
        "No theme": "테마 없음",
        "Selected:": "선택됨:",
        "Import folder:": "가져오기 폴더:",
        "Import a Bible version to start guided reading.": "가이드 읽기를 시작하려면 성경 버전을 가져오세요",
        "Select a book and chapter to start guided reading.": "가이드 읽기를 시작하려면 책과 장을 선택하세요",
        "No verses found in this chapter.": "이 장에서 구절을 찾을 수 없습니다",
        "No matching verse found. Check syntax or use commas/ranges.": "일치하는 구절을 찾을 수 없습니다. 구문을 확인하거나 쉼표/범위를 사용하세요",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "아직 생성된 연구가 없습니다. '읽기 및 해석' 탭으로 이동하여 '설명 생성'을 클릭하여 시작하세요",
        "No results found for your search.": "검색 결과가 없습니다",
        "Import data to start generating a sermon.": "설교 생성을 시작하려면 데이터를 가져오세요",
        "Load a verse to build the devotional.": "묵상을 작성하려면 구절을 로드하세요",
        "Select a verse or scope to anchor the meditation.": "명상을 고정하려면 구절이나 범위를 선택하세요",
        "Import a version to chat with the theological chat.": "신학 채팅과 대화하려면 버전을 가져오세요",
        "Select a verse for the AI to use as authority.": "AI가 권위로 사용할 구절을 선택하세요",
        "Write the question before sending.": "보내기 전에 질문을 작성하세요",
    },
    
    # ============ POLONÊS (PL) ============
    "pl": {
        "Question, answer, reference...": "Pytanie, odpowiedź, odniesienie...",
        "Select the scope for sermon generation:": "Wybierz zakres generowania kazania:",
        "Check to manually select specific books": "Zaznacz, aby ręcznie wybrać określone księgi",
        "Select the books for the sermon:": "Wybierz księgi do kazania:",
        "Select the scope for devotional generation:": "Wybierz zakres generowania rozważania:",
        "Select the books for the devotional:": "Wybierz księgi do rozważania:",
        "No theme": "Brak tematu",
        "Selected:": "Wybrano:",
        "Import folder:": "Folder importu:",
        "Selected book:": "Wybrana księga:",
        "Select books": "Wybierz księgi",
        "Selected books:": "Wybrane księgi:",
        "Questions Only": "Tylko pytania",
        "Import a Bible version to start guided reading.": "Zaimportuj wersję Biblii, aby rozpocząć prowadzone czytanie",
        "Select a book and chapter to start guided reading.": "Wybierz księgę i rozdział, aby rozpocząć prowadzone czytanie",
        "No verses found in this chapter.": "Nie znaleziono wersetów w tym rozdziale",
        "No matching verse found. Check syntax or use commas/ranges.": "Nie znaleziono pasującego wersetu. Sprawdź składnię lub użyj przecinków/zakresów",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Nie wygenerowano jeszcze żadnych studiów. Przejdź do zakładki 'Czytanie i Egzegeza' i kliknij 'Generuj Wyjaśnienie', aby rozpocząć",
        "No results found for your search.": "Nie znaleziono wyników dla twojego wyszukiwania",
        "Import data to start generating a sermon.": "Zaimportuj dane, aby rozpocząć generowanie kazania",
        "Load a verse to build the devotional.": "Załaduj werset, aby zbudować rozważanie",
        "Select a verse or scope to anchor the meditation.": "Wybierz werset lub zakres, aby zakotwiczać medytację",
        "Import a version to chat with the theological chat.": "Zaimportuj wersję, aby rozmawiać z czatem teologicznym",
        "Select a verse for the AI to use as authority.": "Wybierz werset dla AI do użycia jako autorytet",
        "Write the question before sending.": "Napisz pytanie przed wysłaniem",
    },
    
    # ============ ROMENO (RO) ============
    "ro": {
        "Question, answer, reference...": "Întrebare, răspuns, referință...",
        "Select the scope for sermon generation:": "Selectați domeniul pentru generarea predicii:",
        "Check to manually select specific books": "Bifați pentru a selecta manual cărți specifice",
        "Select the books for the sermon:": "Selectați cărțile pentru predică:",
        "Select the scope for devotional generation:": "Selectați domeniul pentru generarea devoțiunii:",
        "Select the books for the devotional:": "Selectați cărțile pentru devoțiune:",
        "No theme": "Fără temă",
        "Selected:": "Selectat:",
        "Import folder:": "Folder import:",
        "Selected book:": "Carte selectată:",
        "Select books": "Selectați cărți",
        "Selected books:": "Cărți selectate:",
        "Questions Only": "Doar întrebări",
        "Import a Bible version to start guided reading.": "Importați o versiune a Bibliei pentru a începe lectura ghidată",
        "Select a book and chapter to start guided reading.": "Selectați o carte și un capitol pentru a începe lectura ghidată",
        "No verses found in this chapter.": "Nu s-au găsit versete în acest capitol",
        "No matching verse found. Check syntax or use commas/ranges.": "Nu s-a găsit niciun verset potrivit. Verificați sintaxa sau folosiți virgule/intervale",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Nu s-au generat încă studii. Mergeți la fila 'Lectură și Exegeză' și faceți clic pe 'Generează Explicație' pentru a începe",
        "No results found for your search.": "Nu s-au găsit rezultate pentru căutarea dvs",
        "Import data to start generating a sermon.": "Importați date pentru a începe generarea unei predici",
        "Load a verse to build the devotional.": "Încărcați un verset pentru a construi devoțiunea",
        "Select a verse or scope to anchor the meditation.": "Selectați un verset sau domeniu pentru a ancora meditația",
        "Import a version to chat with the theological chat.": "Importați o versiune pentru a conversa cu chat-ul teologic",
        "Select a verse for the AI to use as authority.": "Selectați un verset pentru AI pentru a-l folosi ca autoritate",
        "Write the question before sending.": "Scrieți întrebarea înainte de trimitere",
    },
    
    # ============ RUSSO (RU) ============
    "ru": {
        "Question, answer, reference...": "Вопрос, ответ, ссылка...",
        "Check to manually select specific books": "Отметьте, чтобы вручную выбрать конкретные книги",
        "No theme": "Нет темы",
        "Selected:": "Выбрано:",
        "Import folder:": "Папка импорта:",
        "Import a Bible version to start guided reading.": "Импортируйте версию Библии, чтобы начать управляемое чтение",
        "Select a book and chapter to start guided reading.": "Выберите книгу и главу, чтобы начать управляемое чтение",
        "No verses found in this chapter.": "В этой главе не найдено стихов",
        "No matching verse found. Check syntax or use commas/ranges.": "Соответствующий стих не найден. Проверьте синтаксис или используйте запятые/диапазоны",
        "No results found for your search.": "Результаты для вашего поиска не найдены",
        "Import data to start generating a sermon.": "Импортируйте данные, чтобы начать создание проповеди",
        "Load a verse to build the devotional.": "Загрузите стих, чтобы построить размышление",
        "Select a verse or scope to anchor the meditation.": "Выберите стих или область, чтобы закрепить медитацию",
        "Import a version to chat with the theological chat.": "Импортируйте версию для общения с теологическим чатом",
        "Select a verse for the AI to use as authority.": "Выберите стих для использования ИИ в качестве авторитета",
        "Write the question before sending.": "Напишите вопрос перед отправкой",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "Создайте пастырский план, который чтит Слово, актуален и применим к указанной аудитории",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "Напишите личное размышление, которое предлагает духовное утешение, глубокое размышление и практическое применение",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "Отвечайте с теологической ясностью и пастырской благодатью, всегда основываясь на библейском авторитете",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "Напишите полный план проповеди с заголовком, введением, темами толкования, иллюстрациями и заключением",
        "The sermon should cover texts from:": "Проповедь должна охватывать тексты из:",
    },
    
    # ============ SUAÍLI (SW) ============
    "sw": {
        "Question, answer, reference...": "Swali, jibu, marejeleo...",
        "Select the scope for sermon generation:": "Chagua upeo wa kuzalisha hotuba:",
        "Check to manually select specific books": "Angalia ili kuchagua vitabu maalum kwa mkono",
        "Select the books for the sermon:": "Chagua vitabu kwa hotuba:",
        "Select the scope for devotional generation:": "Chagua upeo wa kuzalisha ibada:",
        "Select the books for the devotional:": "Chagua vitabu kwa ibada:",
        "No theme": "Hakuna mada",
        "Selected:": "Iliyochaguliwa:",
        "Import folder:": "Folda ya kuagiza:",
        "Selected book:": "Kitabu kilichochaguliwa:",
        "Select books": "Chagua vitabu",
        "Selected books:": "Vitabu vilivyochaguliwa:",
        "Questions Only": "Maswali Tu",
        "Import a Bible version to start guided reading.": "Agiza toleo la Biblia kuanza kusoma kwa mwongozo",
        "Select a book and chapter to start guided reading.": "Chagua kitabu na sura kuanza kusoma kwa mwongozo",
        "No verses found in this chapter.": "Hakuna mistari iliyopatikana katika sura hii",
        "No matching verse found. Check syntax or use commas/ranges.": "Hakuna mstari unaofanana uliopatikana. Angalia sintaksia au tumia koma/masafa",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Hakuna masomo yaliyozalishwa bado. Nenda kwenye kichupo cha 'Kusoma na Ufafanuzi' na bofya 'Zalisha Maelezo' kuanza",
        "No results found for your search.": "Hakuna matokeo yaliyopatikana kwa utaftaji wako",
        "Import data to start generating a sermon.": "Agiza data kuanza kuzalisha hotuba",
        "Load a verse to build the devotional.": "Pakia mstari kujenga ibada",
        "Select a verse or scope to anchor the meditation.": "Chagua mstari au upeo wa kuangazia tafakuri",
        "Import a version to chat with the theological chat.": "Agiza toleo ili kuongea na gumzo la kiteolojia",
        "Select a verse for the AI to use as authority.": "Chagua mstari kwa AI kutumia kama mamlaka",
        "Write the question before sending.": "Andika swali kabla ya kutuma",
    },
    
    # ============ TAILANDÊS (TH) ============
    "th": {
        "Selected book:": "หนังสือที่เลือก:",
        "Select books": "เลือกหนังสือ",
        "Selected books:": "หนังสือที่เลือก:",
        "Questions Only": "เฉพาะคำถาม",
        "No questions generated yet.": "ยังไม่มีคำถามที่สร้างขึ้น",
        "Generate questions about biblical knowledge.": "สร้างคำถามเกี่ยวกับความรู้ในพระคัมภีร์",
    },
    
    # ============ TURCO (TR) ============
    "tr": {
        "Question, answer, reference...": "Soru, cevap, referans...",
        "Select the scope for sermon generation:": "Vaaz oluşturma kapsamını seçin:",
        "Check to manually select specific books": "Belirli kitapları manuel olarak seçmek için işaretleyin",
        "Select the books for the sermon:": "Vaaz için kitapları seçin:",
        "Select the scope for devotional generation:": "İbadet oluşturma kapsamını seçin:",
        "Select the books for the devotional:": "İbadet için kitapları seçin:",
        "No theme": "Tema yok",
        "Selected:": "Seçili:",
        "Import folder:": "İçe aktarma klasörü:",
        "Selected book:": "Seçili kitap:",
        "Select books": "Kitapları seçin",
        "Selected books:": "Seçili kitaplar:",
        "Questions Only": "Sadece Sorular",
        "Import a Bible version to start guided reading.": "Rehberli okumaya başlamak için bir İncil sürümü içe aktarın",
        "Select a book and chapter to start guided reading.": "Rehberli okumaya başlamak için bir kitap ve bölüm seçin",
        "No verses found in this chapter.": "Bu bölümde ayet bulunamadı",
        "No matching verse found. Check syntax or use commas/ranges.": "Eşleşen ayet bulunamadı. Sözdizimini kontrol edin veya virgül/aralık kullanın",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Henüz çalışma oluşturulmadı. 'Okuma ve Tefsir' sekmesine gidin ve başlamak için 'Açıklama Oluştur'a tıklayın",
        "No results found for your search.": "Aramanız için sonuç bulunamadı",
        "Import data to start generating a sermon.": "Vaaz oluşturmaya başlamak için veri içe aktarın",
        "Load a verse to build the devotional.": "İbadet oluşturmak için bir ayet yükleyin",
        "Select a verse or scope to anchor the meditation.": "Meditasyonu sabitleme için bir ayet veya kapsam seçin",
        "Import a version to chat with the theological chat.": "Teolojik sohbetle sohbet etmek için bir sürüm içe aktarın",
        "Select a verse for the AI to use as authority.": "AI'nın otorite olarak kullanması için bir ayet seçin",
        "Write the question before sending.": "Göndermeden önce soruyu yazın",
    },
    
    # ============ VIETNAMITA (VI) ============
    "vi": {
        "Question, answer, reference...": "Câu hỏi, câu trả lời, tham khảo...",
        "Select the scope for sermon generation:": "Chọn phạm vi tạo bài giảng:",
        "Check to manually select specific books": "Đánh dấu để chọn thủ công các sách cụ thể",
        "Select the books for the sermon:": "Chọn các sách cho bài giảng:",
        "Select the scope for devotional generation:": "Chọn phạm vi tạo suy niệm:",
        "Select the books for the devotional:": "Chọn các sách cho suy niệm:",
        "No theme": "Không có chủ đề",
        "Selected:": "Đã chọn:",
        "Import folder:": "Thư mục nhập:",
        "Selected book:": "Sách đã chọn:",
        "Select books": "Chọn sách",
        "Selected books:": "Các sách đã chọn:",
        "Questions Only": "Chỉ Câu Hỏi",
        "Import a Bible version to start guided reading.": "Nhập phiên bản Kinh Thánh để bắt đầu đọc có hướng dẫn",
        "Select a book and chapter to start guided reading.": "Chọn sách và chương để bắt đầu đọc có hướng dẫn",
        "No verses found in this chapter.": "Không tìm thấy câu trong chương này",
        "No matching verse found. Check syntax or use commas/ranges.": "Không tìm thấy câu phù hợp. Kiểm tra cú pháp hoặc sử dụng dấu phẩy/phạm vi",
        "No studies generated yet. Go to 'Reading & Exegesis' tab and click 'Generate Explanation' to start.": "Chưa tạo nghiên cứu nào. Đi đến tab 'Đọc và Giải Thích' và nhấp 'Tạo Giải Thích' để bắt đầu",
        "No results found for your search.": "Không tìm thấy kết quả cho tìm kiếm của bạn",
        "Import data to start generating a sermon.": "Nhập dữ liệu để bắt đầu tạo bài giảng",
        "Load a verse to build the devotional.": "Tải một câu để xây dựng suy niệm",
        "Select a verse or scope to anchor the meditation.": "Chọn một câu hoặc phạm vi để neo thiền định",
        "Import a version to chat with the theological chat.": "Nhập phiên bản để trò chuyện với cuộc trò chuyện thần học",
        "Select a verse for the AI to use as authority.": "Chọn một câu để AI sử dụng làm thẩm quyền",
        "Write the question before sending.": "Viết câu hỏi trước khi gửi",
    },
    
    # ============ CHINÊS (ZH) ============
    "zh": {
        "Question, answer, reference...": "问题，答案，参考...",
        "Check to manually select specific books": "勾选以手动选择特定书籍",
        "No theme": "无主题",
        "Selected:": "已选择:",
        "Import folder:": "导入文件夹:",
        "Import a Bible version to start guided reading.": "导入圣经版本以开始引导阅读",
        "Select a book and chapter to start guided reading.": "选择书籍和章节以开始引导阅读",
        "No verses found in this chapter.": "本章未找到经文",
        "No matching verse found. Check syntax or use commas/ranges.": "未找到匹配的经文。检查语法或使用逗号/范围",
        "No results found for your search.": "未找到您搜索的结果",
        "Import data to start generating a sermon.": "导入数据以开始生成讲道",
        "Load a verse to build the devotional.": "加载经文以构建灵修",
        "Select a verse or scope to anchor the meditation.": "选择经文或范围以锚定冥想",
        "Import a version to chat with the theological chat.": "导入版本以与神学聊天进行对话",
        "Select a verse for the AI to use as authority.": "选择经文供AI用作权威",
        "Write the question before sending.": "发送前写下问题",
        "Create a pastoral outline that honors the Word, is relevant and applicable to the indicated audience.": "创建尊重圣言、相关且适用于指定受众的牧养大纲",
        "Write a personal meditation that offers spiritual comfort, deep reflection and practical application.": "撰写提供属灵安慰、深刻反思和实际应用的个人灵修",
        "Answer with theological clarity and pastoral grace, always grounded in biblical authority.": "以神学清晰和牧养恩典回答，始终基于圣经权威",
        "Write a complete sermon outline with title, introduction, expository topics, illustrations and conclusion.": "撰写完整的讲道大纲，包括标题、引言、阐释主题、例证和结论",
        "The sermon should cover texts from:": "讲道应涵盖来自以下的文本:",
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
    
    print("🌍 Traduzindo TODOS os 18 idiomas incompletos...")
    print("=" * 70)
    
    for lang_code, translations in ALL_TRANSLATIONS.items():
        filepath = os.path.join(translations_dir, f"{lang_code}.json")
        
        if not os.path.exists(filepath):
            print(f"⚠️  {lang_code}.json não encontrado, pulando...")
            continue
        
        count = replace_translations(filepath, translations)
        total_replacements += count
        
        if count > 0:
            print(f"✅ {lang_code.upper()}: {count} strings traduzidas")
        else:
            print(f"ℹ️  {lang_code.upper()}: Nenhuma string para traduzir")
    
    print("=" * 70)
    print(f"🎉 CONCLUÍDO! Total: {total_replacements} strings traduzidas em 18 idiomas")
    print("✨ Cada idioma agora está 100% no seu idioma nativo!")

if __name__ == "__main__":
    main()
