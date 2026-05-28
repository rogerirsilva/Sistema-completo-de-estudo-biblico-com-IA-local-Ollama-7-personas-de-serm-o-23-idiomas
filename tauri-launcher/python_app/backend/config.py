from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "bible_data.json"
LOCAL_JSON_DIR = ROOT_DIR / "Dados_Json"
TRANSLATIONS_DIR = ROOT_DIR / "translations"

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
OLLAMA_MODEL_DEFAULT = os.getenv("OLLAMA_MODEL_DEFAULT", "llama3.2:1b")
OLLAMA_GENERATE_PATHS = tuple(
    path.strip()
    for path in os.getenv(
        "OLLAMA_GENERATE_PATHS",
        "api/generate,api/v1/generate,v1/generate",
    ).split(",")
    if path.strip()
)
