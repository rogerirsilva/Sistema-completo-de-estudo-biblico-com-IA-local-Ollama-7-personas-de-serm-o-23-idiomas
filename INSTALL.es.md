# 📖 Estudio Bíblico con IA - Guía de Instalación

## 🚀 Instalación Automática (Recomendado)

### Windows

1. **Ejecuta el instalador con privilegios de administrador:**
   - Haz clic derecho en `setup.bat`
   - Selecciona "Ejecutar como administrador"
   - Espera a que finalice la instalación

2. **Inicia la aplicación:**
   - Haz doble clic en `start_app.bat`
   - La aplicación se abrirá automáticamente en el navegador

### ¿Qué hace `setup.bat`?

✅ Verifica e instala Python 3.11.9  
✅ Verifica e instala Git  
✅ Crea entorno virtual Python  
✅ Instala todas las dependencias de `requirements.txt`  
✅ Verifica e instala Ollama  
✅ Descarga el modelo `llama3.2:1b`  
✅ Configura archivo `.env` con variables predeterminadas  

---

## 🛠️ Instalación Manual

### Prerrequisitos

- **Python 3.11+**: [Descargar](https://www.python.org/downloads/)
- **Git** (opcional): [Descargar](https://git-scm.com/downloads)
- **Ollama**: [Descargar](https://ollama.com/download)

### Paso a Paso

1. **Clona o descarga el proyecto**
   ```bash
   git clone https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama.git
   cd Biblia-em-23-Idiomas-Local-Com-IA-Ollama
   ```

2. **Crea el entorno virtual**
   ```bash
   python -m venv .venv
   ```

3. **Activa el entorno virtual**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configura Ollama**
   ```bash
   # Inicia el servidor
   ollama serve
   
   # En otra terminal, descarga el modelo
   ollama pull llama3.2:1b
   ```

6. **Configura el archivo .env**
   ```env
   OLLAMA_BASE=http://127.0.0.1:11434
   OLLAMA_GENERATE_PATHS=/api/generate
   OLLAMA_MODEL_DEFAULT=llama3.2:1b
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=localhost
   ```

7. **Inicia la aplicación**
   ```bash
   streamlit run app.py
   ```

---

## 🎯 Usando la Aplicación

### 1️⃣ Importar Datos Bíblicos

- Accede a la pestaña **"📥 Importar Datos"**
- La aplicación soporta importar versiones bíblicas desde archivos JSON
- Coloca archivos JSON en la carpeta `Dados_Json/{idioma}/`
- Haz clic en **"🔄 Importar Versiones de la Carpeta"**

**Fuentes recomendadas de Biblias JSON:**
- **Portugués**: [github.com/thiagobodruk/bible](https://github.com/thiagobodruk/bible)
- **Inglés**: [github.com/scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)
- **Español**: [github.com/thiagobodruk/bible (rama es)](https://github.com/thiagobodruk/bible)

### 2️⃣ Lectura y Exégesis

- Selecciona la versión de la Biblia
- Elige libro, capítulo y versículos
- Haz clic en **"✨ Generar Explicación"**
- El estudio se guardará automáticamente en el historial

### 3️⃣ Generador de Sermones

- Elige una de las 7 personas de sermón
- Define tema, audiencia y notas
- Selecciona alcance (libro, múltiples libros, testamento o Biblia completa)
- Selecciona versículos específicos
- Haz clic en **"✨ Generar Sermón"**
- Exporta a PDF cuando esté listo

### 4️⃣ Devocional y Meditación

- Elige sentimiento/tema (Gratitud, Paz, Fuerza, etc.)
- Selecciona libro y versículos
- Genera devocional personalizado
- Accede al historial para revisar devocionales anteriores

### 5️⃣ Chat Teológico

- Haz preguntas sobre versículos específicos
- Obtén análisis teológico, histórico y cultural profundo
- Todas las conversaciones se guardan en el historial

### 6️⃣ Generador de Preguntas

- Genera de 1 a 50 preguntas bíblicas
- Elige modo: Con Respuestas o Solo Preguntas
- Perfecto para escuelas bíblicas y grupos de estudio
- Exporta a PDF

---

## 🔧 Solución de Problemas

### ❌ Python no reconocido

**Solución:**
- Asegúrate de que Python esté instalado
- Agrega Python al PATH:
  - Durante la instalación, marca "Add Python to PATH"
  - O agrega manualmente: `C:\Users\{Usuario}\AppData\Local\Programs\Python\Python311`

### ❌ Ollama no conecta

**Solución:**
```bash
# Verifica si Ollama está ejecutándose
curl http://localhost:11434/api/version

# Inicia Ollama manualmente
ollama serve

# Windows: Verifica si está ejecutándose
tasklist | findstr ollama
```

### ❌ Modelo no encontrado

**Solución:**
```bash
# Lista modelos instalados
ollama list

# Descarga modelo recomendado
ollama pull llama3.2:1b

# Prueba el modelo
ollama run llama3.2:1b "Hola, ¿cómo estás?"
```

### ❌ Error al importar versiones bíblicas

**Solución:**
```bash
# Activa el entorno virtual
.venv\Scripts\activate

# Reinstala dependencias
pip install -r requirements.txt --force-reinstall

# Verifica estructura de carpetas
dir Dados_Json\es
```

### ❌ ChromaDB no guarda datos

**Solución:**
```bash
# Verifica permisos de carpeta chroma_db
icacls chroma_db

# Recrea base de datos
rmdir /s /q chroma_db
python -c "import chromadb; chromadb.Client()"
```

### ❌ Puerto 8501 ya en uso

**Solución:**
```bash
# Termina proceso usando puerto 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# O cambia puerto en .env
STREAMLIT_SERVER_PORT=8502
```

---

## 🐛 Errores Comunes

### ImportError: No module named 'streamlit'

**Solución:**
```bash
# Asegúrate de que el entorno virtual esté activado
.venv\Scripts\activate

# Reinstala Streamlit
pip install streamlit --upgrade
```

### Connection refused to Ollama

**Solución:**
1. Verifica si Ollama está instalado: `ollama --version`
2. Inicia servicio Ollama: `ollama serve`
3. Prueba conexión: `curl http://localhost:11434/api/version`

### Timeout al generar sermón

**Solución:**
- ✅ El sistema ahora usa **timeout dinámico** (hasta 10 minutos)
- ✅ Continuación automática para sermones complejos
- Si sigue fallando, prueba un modelo más pequeño: `llama3.2:1b`

---

## 📦 Requisitos del Sistema

### Mínimo

- **SO**: Windows 10/11, Linux, macOS
- **RAM**: 4 GB
- **Almacenamiento**: 10 GB libres
- **Internet**: Solo para descarga inicial de modelos

### Recomendado

- **SO**: Windows 11 o Linux
- **RAM**: 8 GB o más
- **Almacenamiento**: 20 GB libres (para múltiples versiones bíblicas)
- **GPU**: GPU NVIDIA para mejor rendimiento (opcional)

---

## 🚀 Consejos de Rendimiento

### 1. Elige el modelo adecuado

```bash
# Más rápido (2GB RAM)
ollama pull llama3.2:1b

# Balanceado (5GB RAM)
ollama pull llama3.2:3b

# Mejor calidad (8GB RAM)
ollama pull mistral

# Máxima calidad (16GB RAM)
ollama pull llama3.1:8b
```

### 2. Habilitar GPU (solo NVIDIA)

```bash
# Verifica si GPU es detectada
ollama run llama3.2:1b --verbose

# Instala drivers CUDA si es necesario
# https://developer.nvidia.com/cuda-downloads
```

### 3. Ajustar timeout

En `app.py`, ajusta valores de timeout si es necesario:
```python
OLLAMA_REQUEST_TIMEOUT = 600  # 10 minutos
```

---

## 🆘 Obtener Ayuda

- 🐛 **Reportar errores**: [GitHub Issues](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/rogerirsilva/Biblia-em-23-Idiomas-Local-Com-IA-Ollama/discussions)
- 📧 **Contacto**: Abre un issue en GitHub

---

## 📚 Recursos Adicionales

- [Documentación Ollama](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [Documentación Streamlit](https://docs.streamlit.io/)
- [Documentación ChromaDB](https://docs.trychroma.com/)
- [Documentación ReportLab](https://www.reportlab.com/docs/)

---

**Hecho con ❤️ para la gloria de Dios**

*"Lámpara es a mis pies tu palabra, y lumbrera a mi camino." - Salmos 119:105*
