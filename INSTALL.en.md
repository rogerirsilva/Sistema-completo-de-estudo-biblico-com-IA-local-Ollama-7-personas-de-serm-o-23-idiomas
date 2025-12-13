# 📖 Bible Study with AI - Installation Guide

## 🚀 Automatic Installation (Recommended)

### Windows

1. **Run the installer with administrator privileges:**
   - Right-click on `setup.bat`
   - Select "Run as administrator"
   - Wait for installation to complete

2. **Start the application:**
   - Double-click on `start_app.bat`
   - The application will automatically open in the browser

### What does `setup.bat` do?

✅ Checks and installs Python 3.11.9  
✅ Checks and installs Git  
✅ Creates Python virtual environment  
✅ Installs all dependencies from `requirements.txt`  
✅ Checks and installs Ollama  
✅ Downloads `llama3.2:1b` model  
✅ Configures `.env` file with default variables  

---

## 🛠️ Manual Installation

### Prerequisites

- **Python 3.11+**: [Download](https://www.python.org/downloads/)
- **Git** (optional): [Download](https://git-scm.com/downloads)
- **Ollama**: [Download](https://ollama.com/download)

### Step by Step

1. **Clone or download the project**
   ```bash
   git clone https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama.git
   cd Biblia-em-23-Idiomas-Local-Com-IA-Ollama
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Ollama**
   ```bash
   # Start the server
   ollama serve
   
   # In another terminal, download the model
   ollama pull llama3.2:1b
   ```

6. **Configure .env file**
   ```env
   OLLAMA_BASE=http://127.0.0.1:11434
   OLLAMA_GENERATE_PATHS=/api/generate
   OLLAMA_MODEL_DEFAULT=llama3.2:1b
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=localhost
   ```

7. **Start the application**
   ```bash
   streamlit run app.py
   ```

---

## 🎯 Using the Application

### 1️⃣ Import Bible Data

- Access the **"📥 Import Data"** tab
- The application supports importing Bible versions from JSON files
- Place JSON files in the `Dados_Json/{language}/` folder
- Click **"🔄 Import Versions from Folder"**

**Recommended Bible JSON sources:**
- **Portuguese**: [github.com/thiagobodruk/bible](https://github.com/thiagobodruk/bible)
- **English**: [github.com/scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)
- **Spanish**: [github.com/thiagobodruk/bible (branch es)](https://github.com/thiagobodruk/bible)

### 2️⃣ Reading & Exegesis

- Select Bible version
- Choose book, chapter, and verses
- Click **"✨ Generate Explanation"**
- The study will be automatically saved in history

### 3️⃣ Sermon Generator

- Choose one of 7 sermon personas
- Define theme, audience, and notes
- Select scope (book, multiple books, testament, or entire Bible)
- Select specific verses
- Click **"✨ Generate Sermon"**
- Export to PDF when ready

### 4️⃣ Devotional & Meditation

- Choose feeling/theme (Gratitude, Peace, Strength, etc.)
- Select book and verses
- Generate personalized devotional
- Access history to review previous devotionals

### 5️⃣ Theological Chat

- Ask questions about specific verses
- Get deep theological, historical, and cultural analysis
- All conversations are saved in history

### 6️⃣ Question Generator

- Generate from 1 to 50 Bible questions
- Choose mode: With Answers or Questions Only
- Perfect for Bible schools and study groups
- Export to PDF

---

## 🔧 Troubleshooting

### ❌ Python not recognized

**Solution:**
- Make sure Python is installed
- Add Python to PATH:
  - During installation, check "Add Python to PATH"
  - Or add manually: `C:\Users\{User}\AppData\Local\Programs\Python\Python311`

### ❌ Ollama not connecting

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Start Ollama manually
ollama serve

# Windows: Check if running
tasklist | findstr ollama
```

### ❌ Model not found

**Solution:**
```bash
# List installed models
ollama list

# Download recommended model
ollama pull llama3.2:1b

# Test model
ollama run llama3.2:1b "Hello, how are you?"
```

### ❌ Error importing Bible versions

**Solution:**
```bash
# Activate virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check folder structure
dir Dados_Json\en
```

### ❌ ChromaDB not saving data

**Solution:**
```bash
# Check chroma_db folder permissions
icacls chroma_db

# Recreate database
rmdir /s /q chroma_db
python -c "import chromadb; chromadb.Client()"
```

### ❌ Port 8501 already in use

**Solution:**
```bash
# Kill process using port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or change port in .env
STREAMLIT_SERVER_PORT=8502
```

---

## 🐛 Common Errors

### ImportError: No module named 'streamlit'

**Solution:**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate

# Reinstall Streamlit
pip install streamlit --upgrade
```

### Connection refused to Ollama

**Solution:**
1. Check if Ollama is installed: `ollama --version`
2. Start Ollama service: `ollama serve`
3. Test connection: `curl http://localhost:11434/api/version`

### Timeout when generating sermon

**Solution:**
- ✅ System now uses **dynamic timeout** (up to 10 minutes)
- ✅ Automatic continuation for complex sermons
- If still timing out, try a smaller model: `llama3.2:1b`

---

## 📦 System Requirements

### Minimum

- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4 GB
- **Storage**: 10 GB free
- **Internet**: Only for initial download of models

### Recommended

- **OS**: Windows 11 or Linux
- **RAM**: 8 GB or more
- **Storage**: 20 GB free (for multiple Bible versions)
- **GPU**: NVIDIA GPU for better performance (optional)

---

## 🚀 Performance Tips

### 1. Choose the right model

```bash
# Faster (2GB RAM)
ollama pull llama3.2:1b

# Balanced (5GB RAM)
ollama pull llama3.2:3b

# Better quality (8GB RAM)
ollama pull mistral

# Best quality (16GB RAM)
ollama pull llama3.1:8b
```

### 2. Enable GPU (NVIDIA only)

```bash
# Check if GPU is detected
ollama run llama3.2:1b --verbose

# Install CUDA drivers if needed
# https://developer.nvidia.com/cuda-downloads
```

### 3. Adjust timeout

In `app.py`, adjust timeout values if needed:
```python
OLLAMA_REQUEST_TIMEOUT = 600  # 10 minutes
```

---

## 🆘 Getting Help

- 🐛 **Report bugs**: [GitHub Issues](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/discussions)
- 📧 **Contact**: Open an issue on GitHub

---

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)

---

**Made with ❤️ for the glory of God**

*"Your word is a lamp to my feet and a light to my path." - Psalm 119:105*
