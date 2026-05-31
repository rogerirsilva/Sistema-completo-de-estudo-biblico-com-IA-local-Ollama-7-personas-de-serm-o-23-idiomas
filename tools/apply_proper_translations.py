#!/usr/bin/env python3
"""Script para traduzir strings que foram copiadas do inglês."""

import json
from pathlib import Path

# Traduções corretas para cada idioma
PROPER_TRANSLATIONS = {
    "es": {
        "messages": {
            "no_sermons_yet": "🎤 Aún no se han generado sermones. ¡Use la pestaña 'Generador de Sermones' para crear su primer sermón!",
            "no_devotionals_yet": "🧘 Aún no se han generado devocionales. ¡Use la pestaña 'Devocional y Meditación' para crear su primera meditación!",
            "no_studies_yet": "Aún no se han generado estudios. Vaya a la pestaña 'Lectura y Exégesis' y haga clic en 'Generar Explicación' para comenzar.",
            "page_will_reload": "🔄 La página se recargará...",
            "add_json_files": "💡 Agregue archivos .json de versiones bíblicas en esta carpeta y haga clic en 'Importar'.",
            "create_folder_add_json": "💡 Cree la carpeta y agregue archivos JSON de versiones bíblicas.",
            "add_json_retry": "💡 Agregue archivos JSON en la carpeta e intente nuevamente."
        },
        "sections": {
            "import_data": "Importar datos bíblicos",
            "folder_structure": "📁 Estructura de Carpetas por Idioma"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ Cómo Agregar Versiones Bíblicas"
        }
    },
    "fr": {
        "messages": {
            "no_sermons_yet": "🎤 Aucun sermon généré pour le moment. Utilisez l'onglet 'Générateur de Sermons' pour créer votre premier sermon!",
            "no_devotionals_yet": "🧘 Aucun dévotion généré pour le moment. Utilisez l'onglet 'Dévotion et Méditation' pour créer votre première méditation!",
            "no_studies_yet": "Aucune étude générée pour le moment. Allez dans l'onglet 'Lecture et Exégèse' et cliquez sur 'Générer une Explication' pour commencer.",
            "page_will_reload": "🔄 La page va se recharger...",
            "add_json_files": "💡 Ajoutez des fichiers .json de versions bibliques dans ce dossier et cliquez sur 'Importer'.",
            "create_folder_add_json": "💡 Créez le dossier et ajoutez des fichiers JSON de versions bibliques.",
            "add_json_retry": "💡 Ajoutez des fichiers JSON dans le dossier et réessayez."
        },
        "sections": {
            "import_data": "Importer des données bibliques",
            "folder_structure": "📁 Structure des Dossiers par Langue"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ Comment Ajouter des Versions Bibliques"
        }
    },
    "de": {
        "messages": {
            "no_sermons_yet": "🎤 Noch keine Predigten generiert. Verwenden Sie die Registerkarte 'Predigtgenerator', um Ihre erste Predigt zu erstellen!",
            "no_devotionals_yet": "🧘 Noch keine Andachten generiert. Verwenden Sie die Registerkarte 'Andacht und Meditation', um Ihre erste Meditation zu erstellen!",
            "no_studies_yet": "Noch keine Studien generiert. Gehen Sie zur Registerkarte 'Lesen und Exegese' und klicken Sie auf 'Erklärung generieren', um zu beginnen.",
            "page_will_reload": "🔄 Die Seite wird neu geladen...",
            "add_json_files": "💡 Fügen Sie .json-Dateien von Bibelversionen in diesen Ordner ein und klicken Sie auf 'Importieren'.",
            "create_folder_add_json": "💡 Erstellen Sie den Ordner und fügen Sie JSON-Dateien von Bibelversionen hinzu.",
            "add_json_retry": "💡 Fügen Sie JSON-Dateien im Ordner hinzu und versuchen Sie es erneut."
        },
        "sections": {
            "import_data": "Bibeldaten importieren",
            "folder_structure": "📁 Ordnerstruktur nach Sprache"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ Wie man Bibelversionen hinzufügt"
        }
    },
    "ar": {
        "messages": {
            "no_sermons_yet": "🎤 لم يتم إنشاء عظات بعد. استخدم علامة التبويب 'مولد العظات' لإنشاء أول عظة!",
            "no_devotionals_yet": "🧘 لم يتم إنشاء تأملات بعد. استخدم علامة التبويب 'التأمل والتفكر' لإنشاء أول تأمل!",
            "no_studies_yet": "لم يتم إنشاء دراسات بعد. انتقل إلى علامة التبويب 'القراءة والتفسير' وانقر على 'إنشاء تفسير' للبدء.",
            "page_will_reload": "🔄 سيتم إعادة تحميل الصفحة...",
            "add_json_files": "💡 أضف ملفات .json من إصدارات الكتاب المقدس في هذا المجلد وانقر على 'استيراد'.",
            "create_folder_add_json": "💡 أنشئ المجلد وأضف ملفات JSON من إصدارات الكتاب المقدس.",
            "add_json_retry": "💡 أضف ملفات JSON في المجلد وحاول مرة أخرى."
        },
        "sections": {
            "import_data": "استيراد بيانات الكتاب المقدس",
            "folder_structure": "📁 هيكل المجلدات حسب اللغة"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ كيفية إضافة إصدارات الكتاب المقدس"
        }
    },
    "ru": {
        "messages": {
            "no_sermons_yet": "🎤 Проповеди еще не созданы. Используйте вкладку 'Генератор проповедей', чтобы создать свою первую проповедь!",
            "no_devotionals_yet": "🧘 Размышления еще не созданы. Используйте вкладку 'Размышление и медитация', чтобы создать свое первое размышление!",
            "no_studies_yet": "Исследования еще не созданы. Перейдите на вкладку 'Чтение и экзегеза' и нажмите 'Создать объяснение', чтобы начать.",
            "page_will_reload": "🔄 Страница будет перезагружена...",
            "add_json_files": "💡 Добавьте файлы .json версий Библии в эту папку и нажмите 'Импорт'.",
            "create_folder_add_json": "💡 Создайте папку и добавьте файлы JSON версий Библии.",
            "add_json_retry": "💡 Добавьте файлы JSON в папку и попробуйте снова."
        },
        "sections": {
            "import_data": "Импорт библейских данных",
            "folder_structure": "📁 Структура папок по языкам"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ Как добавить версии Библии"
        }
    },
    "zh": {
        "messages": {
            "no_sermons_yet": "🎤 尚未生成讲道。使用'讲道生成器'选项卡创建您的第一篇讲道！",
            "no_devotionals_yet": "🧘 尚未生成灵修。使用'灵修和冥想'选项卡创建您的第一次冥想！",
            "no_studies_yet": "尚未生成研究。转到'阅读和释经'选项卡，然后单击'生成说明'开始。",
            "page_will_reload": "🔄 页面将重新加载...",
            "add_json_files": "💡 在此文件夹中添加圣经版本的.json文件，然后单击'导入'。",
            "create_folder_add_json": "💡 创建文件夹并添加圣经版本的JSON文件。",
            "add_json_retry": "💡 在文件夹中添加JSON文件并重试。"
        },
        "sections": {
            "import_data": "导入圣经数据",
            "folder_structure": "📁 按语言的文件夹结构"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ 如何添加圣经版本"
        }
    },
    "it": {
        "messages": {
            "no_sermons_yet": "🎤 Nessun sermone generato ancora. Usa la scheda 'Generatore di Sermoni' per creare il tuo primo sermone!",
            "no_devotionals_yet": "🧘 Nessun devozionale generato ancora. Usa la scheda 'Devozionale e Meditazione' per creare la tua prima meditazione!",
            "no_studies_yet": "Nessuno studio generato ancora. Vai alla scheda 'Lettura ed Esegesi' e clicca su 'Genera Spiegazione' per iniziare.",
            "page_will_reload": "🔄 La pagina verrà ricaricata...",
            "add_json_files": "💡 Aggiungi file .json di versioni bibliche in questa cartella e fai clic su 'Importa'.",
            "create_folder_add_json": "💡 Crea la cartella e aggiungi file JSON di versioni bibliche.",
            "add_json_retry": "💡 Aggiungi file JSON nella cartella e riprova."
        },
        "sections": {
            "import_data": "Importa dati biblici",
            "folder_structure": "📁 Struttura delle Cartelle per Lingua"
        },
        "expanders": {
            "how_to_add_versions": "ℹ️ Come Aggiungere Versioni Bibliche"
        }
    }
}

def apply_proper_translations():
    translations_dir = Path("translations")
    
    for lang_code, sections in PROPER_TRANSLATIONS.items():
        json_file = translations_dir / f"{lang_code}.json"
        
        if not json_file.exists():
            print(f"⚠️ {lang_code}.json não encontrado")
            continue
        
        print(f"🔧 Atualizando {lang_code}.json...")
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            changed = False
            
            for section, translations in sections.items():
                if section not in data:
                    data[section] = {}
                
                for key, value in translations.items():
                    old_value = data[section].get(key, "")
                    if old_value != value:
                        data[section][key] = value
                        changed = True
                        print(f"   ✅ {section}.{key}")
            
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ {lang_code}.json atualizado!\n")
            else:
                print(f"⏭️ {lang_code}.json já está correto\n")
        
        except Exception as e:
            print(f"❌ Erro: {e}\n")

if __name__ == "__main__":
    print("🌍 Aplicando traduções corretas...\n")
    apply_proper_translations()
    print("\n✨ Traduções corrigidas!")
