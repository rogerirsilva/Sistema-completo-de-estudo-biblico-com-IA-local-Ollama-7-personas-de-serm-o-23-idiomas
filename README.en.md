<div align="center">

# 📖 Bible Study with AI

### *Your Complete Tool for AI-Assisted Bible Study*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tauri](https://img.shields.io/badge/Tauri-Desktop-24C8DB?logo=tauri&logoColor=white)](https://tauri.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ai&logoColor=white)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[✨ Features](#-features) • [🚀 Installation](#-installation) • [📚 How to Use](#-how-to-use) • [🎭 Personas](#-sermon-personas) • [💝 Support](#-support-the-project)

**Clone the project:**
```bash
git clone https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas.git
cd Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas
```

---

</div>

## 🌟 About the Project

A complete and **100% offline** application for deep Bible study, using local language models (Ollama) for theological analysis, sermon generation, devotionals, and much more. Ideal for pastors, theology students, Bible school teachers, and anyone who wants to deepen their knowledge of Scripture.

### 🎯 Why use this system?

- ✅ **100% Offline**: Your biblical data never leaves your computer
- ✅ **Advanced Artificial Intelligence**: Deep theological analysis using local LLMs
- ✅ **7 Sermon Personas**: Unique preaching styles (Analytical, Narrative, Prophetic, etc.)
- ✅ **Multilingual**: Support for Portuguese, English, Spanish, and other languages
- ✅ **Complete History**: All your analyses, sermons, and devotionals saved automatically
- ✅ **Question Generator**: Create Bible quizzes with up to 50 questions
- ✅ **PDF Export**: Generate professional PDFs of sermons and studies
- ✅ **Multi-Version**: Work with NIV, KJV, ESV, NVI, and other translations

---

## ✨ Features

### 📚 Reading & Exegesis
- 🔍 Interactive selection of books, chapters, and **multiple verses** (e.g., "1-5, 10, 15-20")
- 🧠 Automatic generation of **deep theological explanations**
- 📜 Contextual, historical, and linguistic analysis (Greek/Hebrew)
- 📖 **Study History** with intelligent search and filters
- 📄 Export to PDF with professional formatting

### 🗣️ Sermon Generator (7 Personas)
Create sermons in **7 different preaching styles**:

- **🔍 Analytical-Essence** (The Investigator): Spiritual psychology, hidden motivations
- **📚 Expository-Theological** (The Professor): Historical context, exegesis, doctrine
- **🎬 Narrative-Immersive** (The Storyteller): Atmosphere, emotion, dramatic tension
- **💡 Devotional-Practical** (The Mentor): Daily life, comfort, practical steps
- **✝️ Christocentric-Typological** (The Revealer): Jesus in every text, types and shadows
- **🔥 Prophetic-Confrontational** (The Watchman): Repentance, holiness, urgency
- **🛡️ Apologetic-Philosophical** (The Defender): Logic, reason, defense of the faith

**Features:**
- ✅ Customization by theme, target audience, and preacher's notes
- ✅ Flexible scopes: specific book, multiple books, testament, or entire Bible
- ✅ Selection of multiple verses (e.g., "John 3:1-16, 19, 25-30")
- ✅ Dynamic timeout (up to 10 minutes) for complex sermons
- ✅ Intelligent auto-continuation (up to 5 automatic continuations)
- ✅ Complete history with search and PDF export

### 🧘 Devotional & Meditation
- 🙏 Personalized devotionals by feeling/theme (Gratitude, Peace, Strength, etc.)
- 💭 Deep reflections on chosen passages
- 🌅 Meditations for specific times of the day
- 📚 Support for multiple books and verses
- 🗂️ **Devotional History** with search and filters
- 📄 PDF export

### 💬 Intelligent Theological Chat
- ❓ Questions and answers based on specific verses
- 📖 Deep interpretative and doctrinal analysis
- 🌍 Historical, cultural, and linguistic context
- 📚 Various scopes: verse, multiple books, testament, or entire Bible
- 💾 **Conversation History** for previous queries
- 📄 PDF export

### ❓ Bible Question Generator
- 🎯 Generate from 1 to **50 questions** about any book or scope
- ✅ **With Answers** or **Questions Only** mode (for quizzes)
- 📚 Scopes: specific book, multiple books, or entire Bible
- 🧠 Short and direct answers (1-2 sentences) with balanced theological language
- 💾 Complete history with filters by mode
- 📄 Formatted PDF export

### 📥 Import Bible Data
- 🌐 Organization by language (pt/, en/, es/, etc.)
- 📦 Automatic import of multiple Bible versions
- ✅ Support for NVI, ACF, AA, KJV, NIV, RV1960, and others
- 🔄 Intelligent merging with existing versions
- 📁 Organized folder system: `Dados_Json/{language}/`

---

## 🚀 Installation

### For End Users (Recommended)

👉 **[Download Latest Version](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/releases/latest)**

1. **Download the Installer** and run the `.exe` file.
2. **Install Ollama** from [ollama.com](https://ollama.com/) and start it.
3. **Download the AI model** in terminal: `ollama pull llama3.2:1b`
4. **Open the app** from the Desktop shortcut!

### For Developers

1. Install: **Python 3.11+**, **Node.js LTS**, **Rust & Cargo**, **Ollama**
2. `git clone` the repo and enter the folder
3. `python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`
4. `cd tauri-launcher && npm install && npm run tauri:dev`
5. To build installer: `tauri_build_installers.bat` (in root folder)

👉 **[Detailed Installation Guide](INSTALL.en.md)**

---

## 🎭 Sermon Personas

Each persona has **unique tone, method, and structure**:

| Persona | Focus | Ideal For |
|---------|------|-----------|
| 🔍 **Analytical-Essence** | Spiritual psychology, hidden motivations | Deep studies, growth groups |
| 📚 **Expository-Theological** | Historical context, exegesis, doctrine | Bible schools, seminaries |
| 🎬 **Narrative-Immersive** | Atmosphere, emotion, dramatic tension | Revival services, evangelistic |
| 💡 **Devotional-Practical** | Daily life, comfort, practical steps | Small groups, devotionals |
| ✝️ **Christocentric-Typological** | Jesus in every text, types and shadows | Communion services, Easter |
| 🔥 **Prophetic-Confrontational** | Repentance, holiness, urgency | Campaigns, spiritual retreats |
| 🛡️ **Apologetic-Philosophical** | Logic, reason, defense of faith | Debates, intellectual evangelism |

---

## 🛠️ Technologies Used

| Technology | Version | Function |
|------------|--------|--------|
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) | 3.11+ | Main language |
| ![Tauri](https://img.shields.io/badge/Tauri-Desktop-24C8DB?logo=tauri&logoColor=white) | 1.x | Native desktop UI |
| ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white) | 0.100+ | Local backend |
| ![Ollama](https://img.shields.io/badge/Ollama-Latest-000000?logo=ollama&logoColor=white) | Latest | Local LLM (offline) |
| ![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4+-FF6B6B?logo=database&logoColor=white) | 0.4+ | Vector database for history |
| ![ReportLab](https://img.shields.io/badge/ReportLab-4.0+-green?logo=adobe-acrobat-reader&logoColor=white) | 4.0+ | PDF generation |

**Supported LLM models:** `llama3.2:1b`, `llama3.2:3b`, `mistral`, `llama3.1:8b`, `qwen2.5` and any compatible Ollama model.

---

## 📁 Project Structure

```
Biblia/
├── 📄 bible_data_importer.py          # Bible data importer
├── 📄 requirements.txt                # Python dependencies
├── 📄 bible_data.json                 # Consolidated Bible data
├── 📂 backend/                        # FastAPI backend
│   ├── main.py                        # API routes
│   └── services/                      # Services (bible, ollama, etc.)
├── 📂 tauri-launcher/                 # Tauri Desktop frontend
│   ├── src/                           # Frontend source
│   ├── src-tauri/                     # Rust/Tauri config
│   └── python_app/                    # Embedded backend in installer
├── 📂 Dados_Json/                     # Bible versions by language
│   ├── pt/                            # Portuguese (NVI, ACF, AA)
│   ├── en/                            # English (KJV, NIV, ESV)
│   └── es/                            # Spanish (RV1960, RV1995)
├── 📂 chroma_db/                      # Vector database (histories)
├── 📂 translations/                   # UI translations
├── 📂 tools/                          # Utility scripts
└── 📂 .venv/                          # Python virtual environment
```

---

## 🔧 Troubleshooting

### ❌ Ollama not connecting

```bash
# Check status
curl http://localhost:11434/api/version

# Start manually
ollama serve

# Windows: check if running
tasklist | findstr ollama
```

### ❌ Model not found

```bash
# List installed models
ollama list

# Download recommended model
ollama pull llama3.2:1b

# Test model
ollama run llama3.2:1b "Hello"
```

### ❌ Error importing versions

```bash
# Activate virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check folder structure
dir Dados_Json\en
```

---

## 🤝 Contributing

Contributions are **very welcome**! Follow these steps:

1. **Fork** the repository
2. Create a **branch** for your feature (`git checkout -b feature/NewFeature`)
3. **Commit** your changes (`git commit -m 'Add new feature'`)
4. **Push** to the branch (`git push origin feature/NewFeature`)
5. Open a **Pull Request**

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Report Bugs

Found a bug? Open an [Issue](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/issues) with:

- ✅ Clear description of the problem
- ✅ Steps to reproduce
- ✅ Expected vs actual behavior
- ✅ Screenshots (if applicable)
- ✅ System information (Windows, Python, Ollama)

---

<div align="center">

## 💝 Support the Project

This project is **free and open-source**, maintained with dedication to help pastors, theology students, and Christians in studying God's Word.

If this system has been useful to you, consider supporting development with a contribution:

### ☕ **[Donate via PayPal](https://www.paypal.com/donate/?business=9SNHLWN6MUJAQ&no_recurring=0&item_name=Made+with+dedication.+If+you+can,+support+the+time+and+costs+of+creating+this+project.&currency_code=BRL)**

<div align="center">

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=9SNHLWN6MUJAQ&no_recurring=0&item_name=Made+with+dedication.+If+you+can,+support+the+time+and+costs+of+creating+this+project.&currency_code=BRL)

</div>

*Your donation helps to:*
- ⚡ Keep the project active and updated
- 🚀 Develop new features
- 📚 Add more theological resources
- 🌍 Expand support to more languages
- 💻 Improve infrastructure and hosting

---

**Every contribution is greatly appreciated! 🙏**

---

### 📧 Contact

Questions or suggestions? Get in touch:

- 🐛 Issues: [GitHub Issues](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/issues)
- 🌐 Repository: [GitHub](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas)

---

### ⭐ Like the Project?

If this system was useful to you:
- ⭐ Give a **star** on GitHub
- 🔄 **Share** with other pastors and students
- 🐛 **Report bugs** so we can improve
- 💝 **Contribute** with code or ideas

---

**Made with ❤️ and dedication for the glory of God**

*"Your word is a lamp to my feet and a light to my path." - Psalm 119:105*

---

[![GitHub Stars](https://img.shields.io/github/stars/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas?style=social)](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas?style=social)](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas)](https://github.com/rogerirsilva/Sistema-completo-de-estudo-biblico-com-IA-local-Ollama-7-personas-de-serm-o-23-idiomas/issues)

</div>
