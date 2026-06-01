from pathlib import Path
import os

from backend.crypto_utils import decrypt_data, encrypt_data

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

PROVIDERS_CONFIG_PATH = ROOT_DIR / "providers_config.json"


def _default_providers_config() -> dict:
    return {
        "providers": {
            "chatgpt": {"enabled": False, "api_key": "", "model": "gpt-4o-mini", "temperature": 0.2, "max_tokens": 4000},
            "deepseek": {"enabled": False, "api_key": "", "model": "deepseek-chat", "temperature": 0.2, "max_tokens": 4000},
            "grok": {"enabled": False, "api_key": "", "model": "grok-2-latest", "temperature": 0.2, "max_tokens": 4000},
            "openrouter": {"enabled": False, "api_key": "", "model": "openrouter/auto", "temperature": 0.2, "max_tokens": 4000},
            "target_ai": {"enabled": False, "api_key": "", "model": "target-ai-model", "temperature": 0.2, "max_tokens": 4000},
            "nvidia": {"enabled": False, "api_key": "", "model": "meta/llama3-70b-instruct", "temperature": 0.2, "max_tokens": 4000},
            "gemini": {"enabled": False, "api_key": "", "model": "gemini-1.5-flash", "temperature": 0.2, "max_tokens": 4000},
        },
        "active_provider": "ollama",
    }


def load_providers_config() -> dict:
    if not PROVIDERS_CONFIG_PATH.exists():
        return _default_providers_config()
    try:
        encrypted = PROVIDERS_CONFIG_PATH.read_text(encoding="utf-8").strip()
        if not encrypted:
            return _default_providers_config()
        data = decrypt_data(encrypted)
        if data is None:
            return _default_providers_config()
        return data
    except Exception:
        return _default_providers_config()


def save_providers_config(config: dict) -> None:
    encrypted = encrypt_data(config)
    PROVIDERS_CONFIG_PATH.write_text(encrypted, encoding="utf-8")
