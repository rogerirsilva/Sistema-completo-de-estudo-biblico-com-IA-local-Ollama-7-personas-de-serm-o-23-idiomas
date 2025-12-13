import html
import json
import os
import random
import re
import time
import zipfile
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from dotenv import load_dotenv
from datetime import datetime
import base64
from io import BytesIO

import requests
import streamlit as st
from fpdf import FPDF
from bible_data_importer import (
    convert_archive_to_versions,
    convert_payload_to_versions,
    download_github_archive,
    merge_version_maps,
)
from book_names_mapping import get_book_name

load_dotenv()

# =============================================================================
# PERSISTÊNCIA DE DADOS COM CHROMADB
# =============================================================================

CHROMA_DB_DIR = Path("./chroma_db")

# Inicializar ChromaDB globalmente (apenas uma vez)
_CHROMADB_CLIENT = None
_CHROMADB_AVAILABLE = None

def check_chromadb_available():
    """Verifica se ChromaDB está disponível (apenas uma vez)."""
    global _CHROMADB_AVAILABLE
    if _CHROMADB_AVAILABLE is None:
        try:
            import chromadb
            _CHROMADB_AVAILABLE = True
        except ImportError:
            _CHROMADB_AVAILABLE = False
            # Mostrar aviso apenas uma vez
            if 'chromadb_warning_shown' not in st.session_state:
                st.session_state.chromadb_warning_shown = True
                st.warning("⚠️ ChromaDB não está instalado. Execute: start_app.bat")
    return _CHROMADB_AVAILABLE

@st.cache_resource
def init_chromadb():
    """Inicializa o cliente ChromaDB (com cache)."""
    global _CHROMADB_CLIENT
    
    if _CHROMADB_CLIENT is not None:
        return _CHROMADB_CLIENT
    
    if not check_chromadb_available():
        return None
    
    try:
        import chromadb
        from chromadb.config import Settings
        
        # Criar diretório se não existir
        CHROMA_DB_DIR.mkdir(exist_ok=True)
        
        _CHROMADB_CLIENT = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        return _CHROMADB_CLIENT
    except Exception as e:
        if 'chromadb_error_shown' not in st.session_state:
            st.session_state.chromadb_error_shown = True
            st.error(f"❌ Erro ao inicializar ChromaDB: {e}")
        return None

def save_to_chromadb(collection_name: str, entries: List[Dict]):
    """Salva entradas no ChromaDB."""
    try:
        client = init_chromadb()
        if not client:
            return False
        
        # Obter ou criar coleção
        try:
            collection = client.get_collection(name=collection_name)
            # Limpar coleção existente
            existing_ids = collection.get()['ids']
            if existing_ids:
                collection.delete(ids=existing_ids)
        except:
            collection = client.create_collection(name=collection_name)
        
        if not entries:
            return True
        
        # Preparar dados para inserção
        ids = []
        documents = []
        metadatas = []
        
        for idx, entry in enumerate(entries):
            entry_id = f"{collection_name}_{idx}_{int(entry.get('timestamp', time.time()))}"
            ids.append(entry_id)
            
            # Criar documento de texto para busca
            if collection_name == "study_history":
                doc_text = f"{entry.get('book', '')} {entry.get('chapter', '')}:{entry.get('verses', '')} - {entry.get('context', '')[:500]}"
            elif collection_name == "sermon_history":
                doc_text = f"{entry.get('tema', '')} - {entry.get('reference', '')} - {entry.get('sermon', '')[:500]}"
            elif collection_name == "devotional_history":
                doc_text = f"{entry.get('sentimento', '')} - {entry.get('reference', '')} - {entry.get('devotional', '')[:500]}"
            elif collection_name == "chat_history":
                doc_text = f"{entry.get('question', '')} - {entry.get('answer', '')[:500]}"
            else:
                doc_text = json.dumps(entry)
            
            documents.append(doc_text)
            metadatas.append({"data": json.dumps(entry)})
        
        # Adicionar à coleção
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar no ChromaDB: {e}")
        return False

def load_from_chromadb(collection_name: str) -> List[Dict]:
    """Carrega entradas do ChromaDB."""
    try:
        client = init_chromadb()
        if not client:
            return []
        
        try:
            collection = client.get_collection(name=collection_name)
            results = collection.get()
            
            if not results['metadatas']:
                return []
            
            # Extrair dados dos metadados
            entries = []
            for metadata in results['metadatas']:
                try:
                    entry = json.loads(metadata['data'])
                    entries.append(entry)
                except:
                    continue
            
            # Ordenar por timestamp (mais recente primeira)
            entries.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            return entries
            
        except ValueError as e:
            # Coleção não existe ainda - é normal na primeira execução
            if "does not exist" in str(e):
                return []
            raise
            
    except Exception as e:
        # Ignorar erros de coleção não existente (primeira execução)
        if "does not exist" not in str(e):
            st.error(f"❌ Erro ao carregar do ChromaDB: {e}")
        return []

def auto_save_history(collection_name: str, entries: List[Dict]):
    """Salva automaticamente o histórico após mudanças."""
    try:
        save_to_chromadb(collection_name, entries)
    except Exception as e:
        # Falha silenciosa para não interromper o fluxo
        pass

st.set_page_config(
    page_title="Sistema de Estudo Biblico",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
DATA_PATH = Path("bible_data.json")
LOCAL_JSON_DIR = Path("Dados_Json")
CONFIG_PATH = Path("app_config.json")
TRANSLATIONS_DIR = Path("translations")
OLLAMA_MODEL_DEFAULT = os.getenv("OLLAMA_MODEL_DEFAULT", "llama3")
OLLAMA_GENERATE_PATHS = tuple(
    path.strip()
    for path in os.getenv(
        "OLLAMA_GENERATE_PATHS",
        "api/generate,api/v1/generate,v1/generate,generate",
    ).split(",")
    if path.strip()
)

def get_system_prompt(lang_code: str = "pt") -> str:
    """Retorna o system prompt no idioma especificado."""
    prompts = {
        "pt": (
            "Você é um guia teológico cuidadoso que trata as Escrituras como a autoridade suprema. "
            "Responda com graça, profundidade e clareza, sempre citando o texto bíblico fornecido no prompt. "
            "IMPORTANTE: Responda SEMPRE em português, incluindo orações e reflexões."
        ),
        "en": (
            "You are a caring theological guide who treats Scripture as the supreme authority. "
            "Answer with grace, depth, and clarity, always citing the Bible text provided in the prompt. "
            "IMPORTANT: Always respond in English, including prayers and reflections."
        ),
        "es": (
            "Eres un guía teológico cuidadoso que trata las Escrituras como la autoridad suprema. "
            "Responde con gracia, profundidad y claridad, siempre citando el texto bíblico proporcionado en el prompt. "
            "IMPORTANTE: Responde SIEMPRE en español, incluyendo oraciones y reflexiones."
        ),
        "fr": (
            "Vous êtes un guide théologique attentionné qui traite l'Écriture comme l'autorité suprême. "
            "Répondez avec grâce, profondeur et clarté, en citant toujours le texte biblique fourni dans le prompt. "
            "IMPORTANT: Répondez TOUJOURS en français, y compris les prières et réflexions."
        ),
        "de": (
            "Sie sind ein fürsorglicher theologischer Führer, der die Heilige Schrift als höchste Autorität behandelt. "
            "Antworten Sie mit Gnade, Tiefe und Klarheit und zitieren Sie immer den im Prompt bereitgestellten Bibeltext. "
            "WICHTIG: Antworten Sie IMMER auf Deutsch, einschließlich Gebete und Reflexionen."
        ),
        "it": (
            "Sei una guida teologica premurosa che tratta le Scritture come l'autorità suprema. "
            "Rispondi con grazia, profondità e chiarezza, citando sempre il testo biblico fornito nel prompt. "
            "IMPORTANTE: Rispondi SEMPRE in italiano, incluse preghiere e riflessioni."
        ),
        "ru": (
            "Вы заботливый богословский наставник, который относится к Писанию как к высшему авторитету. "
            "Отвечайте с благодатью, глубиной и ясностью, всегда цитируя библейский текст, приведенный в запросе. "
            "ВАЖНО: Всегда отвечайте на русском языке, включая молитвы и размышления."
        ),
        "zh": (
            "你是一位关怀备至的神学向导，将圣经视为至高权威。"
            "以恩典、深度和清晰回答，始终引用提示中提供的圣经文本。"
            "重要：始终用中文回答，包括祷告和反思。"
        ),
        "ja": (
            "あなたは聖書を最高の権威として扱う思いやりのある神学ガイドです。"
            "恵みと深みと明晰さをもって答え、常にプロンプトで提供された聖書のテキストを引用してください。"
            "重要：祈りと考察を含め、常に日本語で回答してください。"
        ),
        "ar": (
            "أنت مرشد لاهوتي رعوي يعامل الكتاب المقدس كسلطة عليا. "
            "أجب بالنعمة والعمق والوضوح، واستشهد دائمًا بالنص الكتابي المقدم في المطالبة. "
            "مهم: أجب دائمًا بالعربية، بما في ذلك الصلوات والتأملات."
        ),
        "ko": (
            "당신은 성경을 최고 권위로 여기는 돌보는 신학 안내자입니다. "
            "은혜와 깊이, 명확함으로 답하며, 항상 프롬프트에 제공된 성경 본문을 인용하십시오. "
            "중요: 기도와 묵상을 포함하여 항상 한국어로 답하십시오."
        ),
    }
    # Fallback para português se o idioma não estiver disponível
    return prompts.get(lang_code, prompts["pt"])

CUSTOM_STYLE = """
<style>
body {
  background: linear-gradient(180deg, #f8fafc, #fefefc);
}
.block-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
}
section.main {
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.87);
  box-shadow: 0 35px 90px rgba(15, 23, 42, 0.08);
}
.sidebar .sidebar-content {
  background: linear-gradient(180deg, #0f172a, #1e223c);
  color: #f8fafc;
  border-radius: 18px;
  padding: 1.5rem;
}
.sidebar .stButton>button {
  background-color: #2563eb;
  color: #fff;
}
</style>
"""


def make_ollama_url(endpoint: str) -> str:
    clean_base = OLLAMA_BASE.rstrip("/")
    clean_endpoint = endpoint.lstrip("/")
    return f"{clean_base}/{clean_endpoint}"


def load_bible_data(path: Path) -> Dict:
    """Carrega dados da Bíblia do arquivo principal (mantido por compatibilidade)."""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        st.warning(f"⚠️ Erro ao carregar bible_data.json: {e}. Usando dados vazios.")
        return {}
    except Exception as e:
        st.error(f"❌ Erro inesperado ao carregar dados: {e}")
        return {}


def load_bible_data_by_language(lang_code: str) -> Dict:
    """Carrega dados da Bíblia do idioma especificado."""
    lang_dir = Path("Dados_Json") / lang_code
    
    if not lang_dir.exists():
        # Fallback: tentar carregar do bible_data.json principal
        return load_bible_data(DATA_PATH)
    
    # Estrutura padronizada: versions -> version_name -> books -> book_name -> chapters
    bible_data = {"versions": {}}
    
    # Carregar todos os arquivos JSON do diretório do idioma
    for json_file in lang_dir.glob("*.json"):
        if json_file.name.lower() == "readme.json":
            continue
        
        try:
            # Ler o arquivo removendo BOM e espaços
            with open(json_file, "r", encoding="utf-8-sig") as f:
                content = f.read().strip()
            
            # Parse JSON do conteúdo limpo
            data = json.loads(content)
            
            # Nome da versão do arquivo
            version_name = json_file.stem.upper()
            
            # Converter formato array [{"abbrev": "gn", "chapters": [...], "name": "Gênesis"}, ...]
            # para formato dict estruturado
            if isinstance(data, list):
                books = {}
                for idx, book in enumerate(data):
                    book_abbrev = book.get("abbrev", "").lower()
                    
                    # Usar o mapeamento de traduções para obter o nome correto no idioma
                    # Se não houver tradução, usa o nome do JSON ou a abreviação
                    book_name_from_json = book.get("name", "")
                    book_name = get_book_name(book_abbrev, lang_code, fallback=book_name_from_json)
                    
                    # Se ainda não tiver nome, usa um fallback genérico
                    if not book_name:
                        book_name = f"Book{idx + 1}"
                    
                    chapters_dict = {}
                    
                    # Converter chapters array para dict com verses
                    for ch_idx, chapter_verses in enumerate(book.get("chapters", [])):
                        ch_num = str(ch_idx + 1)
                        
                        # Converter array de versículos para dict numerado
                        verses_dict = {}
                        if isinstance(chapter_verses, list):
                            for v_idx, verse_text in enumerate(chapter_verses):
                                verses_dict[str(v_idx + 1)] = verse_text
                        
                        chapters_dict[ch_num] = {
                            "verses": verses_dict
                        }
                    
                    # Usar o NOME TRADUZIDO como chave principal para exibição correta
                    # Mantém abbrev para compatibilidade com funções de testamento
                    books[book_name] = {
                        "name": book_name,
                        "abbrev": book_abbrev,
                        "order": idx + 1,
                        "chapters": chapters_dict
                    }
                
                bible_data["versions"][version_name] = {
                    "books": books
                }
            # Se já está no formato estruturado
            elif isinstance(data, dict) and "versions" in data:
                bible_data = data
                break
                
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar {json_file.name}: {e}")
            continue
    
    return bible_data


def load_app_config() -> Dict:
    """Carrega configurações do aplicativo."""
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_app_config(config: Dict) -> None:
    """Salva configurações do aplicativo."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except:
        pass


def get_available_languages() -> Dict[str, str]:
    """Retorna dicionário de idiomas disponíveis {código: nome}."""
    # Mapeamento completo de idiomas com nomes nativos
    all_languages = {
        "pt": "Português",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "it": "Italiano",
        "ru": "Русский",
        "zh": "中文",
        "ja": "日本語",
        "ar": "العربية",
        "el": "Ελληνικά",
        "eo": "Esperanto",
        "fi": "Suomi",
        "ko": "한국어",
        "ro": "Română",
        "vi": "Tiếng Việt",
        "hi": "हिन्दी",
        "id": "Bahasa Indonesia",
        "pl": "Polski",
        "fa": "فارسی",
        "sw": "Kiswahili",
        "th": "ไทย",
        "tr": "Türkçe"
    }
    
    # Verificar quais idiomas têm arquivos de tradução ou Bíblias disponíveis
    available_languages = {}
    
    # Adicionar idiomas com traduções
    if TRANSLATIONS_DIR.exists():
        for file in TRANSLATIONS_DIR.glob("*.json"):
            lang_code = file.stem
            if lang_code in all_languages:
                available_languages[lang_code] = all_languages[lang_code]
    
    # Adicionar idiomas com Bíblias disponíveis (mesmo sem tradução da interface)
    bible_data_dir = Path("Dados_Json")
    if bible_data_dir.exists():
        for lang_dir in bible_data_dir.iterdir():
            if lang_dir.is_dir():
                lang_code = lang_dir.name
                if lang_code in all_languages and lang_code not in available_languages:
                    # Verificar se tem pelo menos um arquivo JSON
                    if list(lang_dir.glob("*.json")):
                        available_languages[lang_code] = all_languages[lang_code]
    
    return available_languages if available_languages else {"pt": "Português"}


@st.cache_data
def load_translation(lang_code: str) -> Dict:
    """Carrega arquivo de tradução para o idioma especificado."""
    trans_file = TRANSLATIONS_DIR / f"{lang_code}.json"
    if not trans_file.exists():
        trans_file = TRANSLATIONS_DIR / "pt.json"  # Fallback para português
    
    try:
        with open(trans_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def t(translations: Dict, key_path: str, default: str = "") -> str:
    """
    Função helper para obter tradução por caminho de chave.
    Exemplo: t(trans, "menu.reading") retorna trans["menu"]["reading"]
    """
    keys = key_path.split(".")
    value = translations
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
    return value if value else default


@st.cache_data
@st.cache_data
def cached_data(path: Path) -> Dict:
    return load_bible_data(path)


@st.cache_data
@st.cache_data
def cached_data_by_language(lang_code: str) -> Dict:
    """Carrega dados da Bíblia do idioma especificado com cache."""
    return load_bible_data_by_language(lang_code)


def parse_version_filter(raw: str) -> Optional[Set[str]]:
    if not raw:
        return None
    parts = {segment.strip().lower() for segment in raw.replace(";", ",").split(",")}
    return {item for item in parts if item}


def persist_versions(new_versions: Dict[str, Dict], merge: bool = True) -> Dict[str, Dict]:
    existing = load_bible_data(DATA_PATH)
    existing_versions = existing.get("versions", {})
    final_versions = new_versions if not merge else merge_version_maps(existing_versions, new_versions)
    payload = {"generated_on": time.time(), "versions": final_versions}
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    cached_data.clear()
    return cached_data(DATA_PATH)


def load_local_json_versions(folder: Path, version_filter: Optional[Set[str]] = None) -> Dict[str, Dict[str, Any]]:
    versions: Dict[str, Dict[str, Any]] = {}
    if not folder.exists():
        return versions
    for entry in folder.glob("*.json"):
        version_hint = entry.stem.lower()
        if version_filter and version_hint not in version_filter:
            continue
        try:
            with entry.open("r", encoding="utf-8-sig") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            continue
        candidate = convert_payload_to_versions(payload, version_hint=version_hint)
        for key, data in candidate.items():
            normalized_key = key.lower()
            if version_filter and normalized_key not in version_filter:
                continue
            target_entry = versions.setdefault(normalized_key, {"version": normalized_key, "books": {}})
            books = target_entry.setdefault("books", {})
            books.update(data.get("books", {}))
    return versions


def list_versions(data: Dict) -> List[str]:
    return sorted(data.get("versions", {}).keys())


def get_books_for_version(data: Dict, version: str) -> List[Tuple[str, Dict]]:
    version_data = data.get("versions", {}).get(version, {})
    books = version_data.get("books", {})
    return sorted(books.items(), key=lambda item: item[1].get("order", 0))


def get_chapters(book_entry: Dict) -> List[str]:
    return sorted(book_entry.get("chapters", {}).keys(), key=lambda key: int(key))


def get_verse(book_entry: Dict, chapter: str, verse: str) -> Optional[str]:
    return book_entry.get("chapters", {}).get(chapter, {}).get("verses", {}).get(verse)


def check_ollama_online() -> Tuple[bool, str]:
    health_paths = (
        "api/version",
        "version",
        "api/health",
        "health",
    )
    base_root = OLLAMA_BASE.rstrip("/")
    base_candidates = [
        base_root,
        f"{base_root}/api",
        f"{base_root}/ollama",
        f"{base_root}/ollama/api",
    ]
    if base_root.endswith("/api"):
        base_candidates.append(base_root[:-4])
    seen: Set[str] = set()
    bases: List[str] = []
    for candidate in base_candidates:
        clean = candidate.rstrip("/")
        if clean and clean not in seen:
            seen.add(clean)
            bases.append(clean)

    attempts: List[str] = []
    for base in bases:
        for path in health_paths:
            url = f"{base}/{path.lstrip('/')}"
            try:
                response = requests.get(url, timeout=8)
                attempts.append(f"{url} -> {response.status_code}")
                if response.status_code == 200:
                    return True, f"Conectado ({url})"
            except requests.RequestException as exc:
                attempts.append(f"{url} -> exception {exc}")
                continue
    if not attempts:
        return False, "Falha ao contatar Ollama (nenhuma tentativa registrada)."
    brief = attempts[:4]
    if len(attempts) > 4:
        brief.append(f"... +{len(attempts) - 4} outras")
    detail = "; ".join(brief)
    return False, f"Falha ao contatar Ollama. Ajuste OLLAMA_BASE/OLLAMA_GENERATE_PATHS. Tentativas: {detail}"


def list_ollama_models() -> List[str]:
    try:
        response = requests.get(make_ollama_url("/api/tags"), timeout=5)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        result: List[str] = []
        for item in models:
            if isinstance(item, dict):
                name = item.get("name") or item.get("model")
                if name:
                    result.append(name)
        return result
    except requests.RequestException:
        return []


def extract_text_from_response(payload: Dict) -> str:
    if not payload:
        return ""
    # Formato Ollama padrão: {"model": "...", "response": "..."}
    if "response" in payload:
        return payload["response"]
    # Fallback para formatos compatíveis com OpenAI
    choices = payload.get("choices")
    if choices and isinstance(choices, list):
        first = choices[0]
        message = first.get("message") if isinstance(first, dict) else first
        if isinstance(message, dict):
            return (
                message.get("content")
                or message.get("text")
                or ""
            )
        return first.get("content") or first.get("text") or ""
    return payload.get("text") or payload.get("message") or ""


def query_ollama(model: str, prompt: str, temperature: float = 0.25, max_tokens: int = 700, timeout: int = 120, auto_continue: bool = False, lang_code: str = "pt", show_progress: bool = False) -> Tuple[bool, str]:
    """
    Consulta o Ollama com suporte a continuação automática de respostas incompletas.
    
    Args:
        model: Nome do modelo Ollama
        prompt: Prompt para o modelo
        temperature: Temperatura de geração (0.0-1.0)
        max_tokens: Número máximo de tokens por chamada (-1 para ilimitado)
        timeout: Timeout em segundos
        auto_continue: Se True, detecta respostas incompletas e continua gerando
        lang_code: Código do idioma para o system prompt
        show_progress: Se True, mostra feedback visual durante continuações
    
    Returns:
        Tupla (sucesso, resposta_completa)
    """
    url = make_ollama_url("/api/generate")
    full_response = ""
    attempts = 0
    max_attempts = 5  # Máximo de continuações para evitar loops infinitos
    system_prompt = get_system_prompt(lang_code)
    progress_placeholder = st.empty() if show_progress else None
    
    while attempts < max_attempts:
        attempts += 1
        
        # Mostrar progresso se habilitado
        if progress_placeholder and attempts > 1:
            progress_placeholder.info(f"🔄 Continuação {attempts}/{max_attempts} - Expandindo conteúdo... ({len(full_response)} caracteres gerados)")
        
        # Construir prompt (incluir contexto anterior se estiver continuando)
        current_prompt = prompt if attempts == 1 else f"{prompt}\n\nContinue de onde parou: {full_response[-200:]}"
        
        # Formato de payload correto para a API do Ollama
        payload = {
            "model": model,
            "prompt": current_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens if max_tokens > 0 else 2048,  # Usar 2048 se -1
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            text = extract_text_from_response(data)
            
            if not text:
                if attempts == 1:
                    return False, f"Resposta vazia do Ollama. Dados recebidos: {data}"
                break  # Se não há mais texto, considera completo
            
            full_response += text
            
            # Verificar se a resposta está completa
            if not auto_continue:
                break  # Não continuar se auto_continue está desabilitado
            
            # Detectar se a resposta foi cortada (indicadores de incompletude)
            is_incomplete = (
                data.get("done", True) == False or  # Ollama indica que não terminou
                not text.rstrip().endswith((".", "!", "?", "\n", "Amém", "amém")) or  # Não termina com pontuação
                text.rstrip().endswith((",", ";", ":", "-", "e", "que", "para"))  # Termina com conectivos
            )
            
            if not is_incomplete:
                break  # Resposta completa, parar
                
        except requests.HTTPError as exc:
            return False, f"Erro HTTP do Ollama: {exc.response.status_code} - {exc.response.text[:200]}"
        except requests.Timeout:
            if full_response:  # Se já temos alguma resposta, retornar o que temos
                return True, full_response.strip()
            return False, f"Timeout ao aguardar resposta do Ollama ({timeout}s). Tente um escopo menor ou aumentar o timeout."
        except requests.RequestException as exc:
            if full_response:  # Se já temos alguma resposta, retornar o que temos
                return True, full_response.strip()
            return False, f"Erro ao conectar com Ollama em {url}: {str(exc)[:200]}"
        except (ValueError, KeyError) as exc:
            if full_response:  # Se já temos alguma resposta, retornar o que temos
                return True, full_response.strip()
            return False, f"Erro ao processar resposta do Ollama: {exc}"
    
    # Limpar placeholder de progresso antes de retornar
    if progress_placeholder:
        progress_placeholder.empty()
    
    return True, full_response.strip()


def build_prompt(context: str, request: str, reference: str = "") -> str:
    if reference:
        return f"Você está analisando o texto bíblico de {reference}. O texto é: {context}\n\nImportante: Sempre se refira a este texto como {reference}. {request}"
    return f"Com base estritamente no texto biblico a seguir: {context}\n{request}"


# =============================================================================
# CLASSES E FUNÇÕES PARA GERAÇÃO DE PDF ELEGANTE
# =============================================================================

class ElegantBiblePDF(FPDF):
    """Classe personalizada para gerar PDFs elegantes com design profissional."""
    
    def __init__(self, title="Documento Bíblico", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        """Cabeçalho elegante com gradiente simulado."""
        # Retângulo de fundo do cabeçalho
        self.set_fill_color(102, 126, 234)  # Azul elegante
        self.rect(0, 0, 210, 30, 'F')
        
        # Borda dourada
        self.set_draw_color(255, 215, 0)  # Dourado
        self.set_line_width(0.8)
        self.line(10, 28, 200, 28)
        
        # Título do documento
        self.set_font('Arial', 'B', 16)
        self.set_xy(25, 10)
        self.cell(0, 10, self.doc_title, 0, 0, 'L')
        
        # Reset cor do texto
        self.set_text_color(0, 0, 0)
        self.ln(25)
        
    def footer(self):
        """Rodapé elegante com número da página."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        
        # Linha decorativa
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Número da página
        page_text = f'Página {self.page_no()}/{{nb}}'
        self.set_y(-12)
        self.cell(0, 10, page_text, 0, 0, 'C')
        
        # Data de geração
        date_text = datetime.now().strftime('%d/%m/%Y')
        self.set_xy(10, -12)
        self.cell(0, 10, f'Gerado em {date_text}', 0, 0, 'L')
        
    def chapter_title(self, title: str, icon: str = ''):
        """Adiciona um título de seção elegante."""
        self.ln(5)
        
        # Fundo do título
        self.set_fill_color(118, 75, 162)  # Roxo
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 14)
        
        full_title = f'{icon} {title}' if icon else title
        self.cell(0, 10, full_title, 0, 1, 'L', fill=True)
        
        # Linha decorativa dourada
        self.set_draw_color(255, 215, 0)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 50, self.get_y())
        
        self.ln(3)
        self.set_text_color(0, 0, 0)
        
    def info_box(self, label: str, value: str):
        """Adiciona uma caixa de informação estilizada."""
        self.set_font('Arial', 'B', 10)
        self.set_text_color(102, 126, 234)
        self.cell(40, 6, f'{label}:', 0, 0)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, value, 0, 1)
        
    def content_box(self, content: str, bg_color=(245, 247, 250)):
        """Adiciona uma caixa de conteúdo com fundo colorido."""
        self.ln(2)
        
        # Salvar posição atual
        x_start = self.get_x()
        y_start = self.get_y()
        
        # Desenhar fundo
        self.set_fill_color(*bg_color)
        
        # Calcular altura necessária
        self.set_font('Arial', '', 10)
        
        # Processar texto com quebra de linha
        effective_width = 190
        lines = content.split('\n')
        
        total_height = 0
        for line in lines:
            if not line.strip():
                total_height += 5
                continue
            # Multi_cell retorna altura usada
            line_height = self.font_size * 1.5
            num_lines = len(self.multi_cell(effective_width, line_height, line, split_only=True))
            total_height += num_lines * line_height
        
        # Desenhar retângulo de fundo
        self.set_xy(x_start, y_start)
        self.rect(x_start, y_start, effective_width, total_height + 10, 'F')
        
        # Adicionar borda
        self.set_draw_color(102, 126, 234)
        self.set_line_width(0.3)
        self.rect(x_start, y_start, effective_width, total_height + 10)
        
        # Escrever texto
        self.set_xy(x_start + 3, y_start + 5)
        for line in lines:
            if not line.strip():
                self.ln(5)
                continue
            self.multi_cell(effective_width - 6, 5, line)
        
        self.ln(5)


def remove_emojis(text: str) -> str:
    """Remove emojis de um texto para compatibilidade com FPDF."""
    # Remove emojis e outros caracteres Unicode especiais
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()


def generate_study_pdf(entry: Dict, trans: Dict) -> BytesIO:
    """Gera PDF elegante para estudo bíblico."""
    title = remove_emojis(trans.get("headers", {}).get("bible_studies_history", "Estudo Bíblico"))
    pdf = ElegantBiblePDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Título principal
    reference = f"{entry['book']} {entry['chapter']}:{entry['verses']}"
    pdf.chapter_title(reference)
    
    # Informações do estudo
    pdf.ln(3)
    timestamp_str = time.strftime(
        trans.get("formatting", {}).get("timestamp_format", "%d/%m/%Y às %H:%M"),
        time.localtime(entry["timestamp"])
    )
    
    version_label = remove_emojis(trans.get("captions", {}).get("version", "Versão"))
    model_label = remove_emojis(trans.get("captions", {}).get("model", "Modelo"))
    
    pdf.info_box('Data', timestamp_str)
    pdf.info_box(version_label, entry.get('version', 'N/A'))
    pdf.info_box(model_label, entry.get('model', 'N/A'))
    
    # Contexto Bíblico
    pdf.ln(5)
    context_label = remove_emojis(trans.get("expanders", {}).get("biblical_context", "Contexto Bíblico"))
    pdf.chapter_title(context_label)
    pdf.content_box(entry['context'], (240, 248, 255))  # Azul claro
    
    # Explicação
    pdf.ln(3)
    explanation_label = remove_emojis(trans.get("expanders", {}).get("full_explanation", "Explicação Completa"))
    pdf.chapter_title(explanation_label)
    pdf.content_box(entry['explanation'], (248, 245, 255))  # Roxo claro
    
    # Salvar PDF em buffer
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer


def generate_sermon_pdf(entry: Dict, trans: Dict) -> BytesIO:
    """Gera PDF elegante para sermão."""
    title = remove_emojis(trans.get("headers", {}).get("sermon_generator", "Sermão"))
    pdf = ElegantBiblePDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Título
    reference = f"{entry.get('book', '')} {entry.get('chapter', '')}:{entry.get('verses', '')}"
    if entry.get('scope'):
        reference = entry['scope']
    
    pdf.chapter_title(reference)
    
    # Informações
    pdf.ln(3)
    timestamp_str = time.strftime(
        trans.get("formatting", {}).get("timestamp_format", "%d/%m/%Y às %H:%M"),
        time.localtime(entry["timestamp"])
    )
    
    theme_label = remove_emojis(trans.get("prompts", {}).get("sermon_theme", "Tema"))
    audience_label = remove_emojis(trans.get("captions", {}).get("audience", "Público"))
    model_label = remove_emojis(trans.get("captions", {}).get("model", "Modelo"))
    
    pdf.info_box('Data', timestamp_str)
    if entry.get('theme'):
        pdf.info_box(theme_label, entry['theme'])
    if entry.get('audience'):
        pdf.info_box(audience_label, entry['audience'])
    pdf.info_box(model_label, entry.get('model', 'N/A'))
    
    # Conteúdo do Sermão
    pdf.ln(5)
    sermon_title = remove_emojis(trans.get("headers", {}).get("sermon_generator", "Esboço do Sermão"))
    pdf.chapter_title(sermon_title)
    pdf.content_box(entry['sermon'], (255, 250, 240))  # Bege claro
    
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer


def generate_devotional_pdf(entry: Dict, trans: Dict) -> BytesIO:
    """Gera PDF elegante para devocional."""
    title = remove_emojis(trans.get("headers", {}).get("devotional_meditation", "Devocional"))
    pdf = ElegantBiblePDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Título
    reference = f"{entry.get('book', '')} {entry.get('chapter', '')}:{entry.get('verses', '')}"
    if entry.get('scope'):
        reference = entry['scope']
    
    pdf.chapter_title(reference)
    
    # Informações
    pdf.ln(3)
    timestamp_str = time.strftime(
        trans.get("formatting", {}).get("timestamp_format", "%d/%m/%Y às %H:%M"),
        time.localtime(entry["timestamp"])
    )
    
    feeling_label = remove_emojis(trans.get("captions", {}).get("feeling", "Sentimento"))
    model_label = remove_emojis(trans.get("captions", {}).get("model", "Modelo"))
    
    pdf.info_box('Data', timestamp_str)
    if entry.get('feeling'):
        pdf.info_box(feeling_label, entry['feeling'])
    pdf.info_box(model_label, entry.get('model', 'N/A'))
    
    # Conteúdo do Devocional
    pdf.ln(5)
    devotional_title = remove_emojis(trans.get("headers", {}).get("devotional_meditation", "Meditação"))
    pdf.chapter_title(devotional_title)
    pdf.content_box(entry['devotional'], (240, 255, 240))  # Verde claro
    
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer


def generate_chat_pdf(entry: Dict, trans: Dict) -> BytesIO:
    """Gera PDF elegante para conversa teológica."""
    title = remove_emojis(trans.get("headers", {}).get("theological_chat", "Chat Teológico"))
    pdf = ElegantBiblePDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Título
    reference = f"{entry.get('book', '')} {entry.get('chapter', '')}:{entry.get('verses', '')}"
    pdf.chapter_title(reference)
    
    # Informações
    pdf.ln(3)
    timestamp_str = time.strftime(
        trans.get("formatting", {}).get("timestamp_format", "%d/%m/%Y às %H:%M"),
        time.localtime(entry["timestamp"])
    )
    
    model_label = remove_emojis(trans.get("captions", {}).get("model", "Modelo"))
    
    pdf.info_box('Data', timestamp_str)
    pdf.info_box(model_label, entry.get('model', 'N/A'))
    
    # Pergunta
    pdf.ln(5)
    question_label = remove_emojis(trans.get("formatting", {}).get("question_label", "Pergunta"))
    pdf.chapter_title(question_label)
    pdf.content_box(entry['question'], (255, 248, 240))  # Laranja claro
    
    # Resposta
    pdf.ln(3)
    answer_label = remove_emojis(trans.get("formatting", {}).get("answer_label", "Resposta"))
    pdf.chapter_title(answer_label)
    pdf.content_box(entry['answer'], (240, 255, 255))  # Ciano claro
    
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer


def generate_questions_pdf(entry: Dict, trans: Dict) -> BytesIO:
    """Gera PDF elegante para perguntas bíblicas."""
    title = remove_emojis(trans.get("headers", {}).get("bible_questions", "Perguntas Bíblicas"))
    pdf = ElegantBiblePDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Título
    reference = entry.get('reference', '')
    pdf.chapter_title(reference)
    
    # Informações
    pdf.ln(3)
    timestamp_str = time.strftime(
        trans.get("formatting", {}).get("timestamp_format", "%d/%m/%Y às %H:%M"),
        time.localtime(entry["timestamp"])
    )
    
    model_label = remove_emojis(trans.get("captions", {}).get("model", "Modelo"))
    questions_count_label = remove_emojis(trans.get("captions", {}).get("questions_count", "Quantidade"))
    mode_label = remove_emojis(trans.get("captions", {}).get("mode", "Modo"))
    
    pdf.info_box('Data', timestamp_str)
    pdf.info_box(questions_count_label, str(entry.get('questions_count', 'N/A')))
    pdf.info_box(mode_label, entry.get('mode', 'N/A'))
    pdf.info_box(model_label, entry.get('model', 'N/A'))
    
    # Conteúdo das Perguntas
    pdf.ln(5)
    questions_title = remove_emojis(trans.get("headers", {}).get("generated_questions", "Perguntas Geradas"))
    pdf.chapter_title(questions_title)
    pdf.content_box(entry['questions'], (255, 245, 230))  # Amarelo claro
    
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer


# =============================================================================
# FIM DAS FUNÇÕES DE PDF
# =============================================================================


def render_book_page(
    book_label: str,
    book_entry: Dict[str, Any],
    selected_chapter: Optional[str],
    highlighted_verses: Set[str],
    trans: Dict = None,
) -> None:
    if trans is None:
        trans = {}
    chapters = get_chapters(book_entry)
    if not chapters:
        return
    chapter_to_show = selected_chapter if selected_chapter in chapters else chapters[0]
    chapter_data = book_entry.get("chapters", {}).get(chapter_to_show)
    if not chapter_data:
        return
    chapter_title = chapter_data.get("chapter_title")
    header = f"{t(trans, 'labels.reading_page', 'Página de leitura')} – {book_label} {chapter_to_show}"
    if chapter_title:
        header += f" · {chapter_title}"
    st.markdown(f"### {header}")
    verses = chapter_data.get("verses", {})
    if not verses:
        st.info(t(trans, "messages.no_verses_in_chapter", "Nenhum versículo encontrado neste capítulo."))
        return
    for verse_key in sorted(verses.keys(), key=lambda value: int(value)):
        text = verses.get(verse_key, "")
        if not text:
            continue
        safe_text = html.escape(text).replace("\n", " ")
        style = (
            "background:linear-gradient(135deg,#1e293b,#111625);color:#f8fafc;border-radius:10px;padding:0.6rem;border:1px solid #3f4f7a;box-shadow:0 12px 30px rgba(15,23,42,0.4);"
            if verse_key in highlighted_verses
            else "margin-bottom:0.25rem;padding:0.25rem 0;"
        )
        st.markdown(
            f"<p style='{style}'><strong>{verse_key}</strong> {safe_text}</p>",
            unsafe_allow_html=True,
        )


def _format_book_label(key_name: str) -> str:
    """Formata o label do livro - o key_name JÁ é o nome traduzido."""
    # O key_name agora é o próprio nome do livro no idioma correto
    # Não precisa fazer lookup, apenas retornar o nome
    return key_name


def parse_verse_selection(raw: str, available: List[str]) -> List[str]:
    if not raw:
        return []
    numeric = {int(value) for value in available if value.isdigit()}
    selected: Set[int] = set()
    for token in re.split(r"[\s,]+", raw.strip()):
        if not token:
            continue
        if "-" in token:
            parts = token.split("-", 1)
            if len(parts) != 2:
                continue
            if not (parts[0].isdigit() and parts[1].isdigit()):
                continue
            start, end = sorted((int(parts[0]), int(parts[1])))
            for value in range(start, end + 1):
                if value in numeric:
                    selected.add(value)
            continue
        if token.isdigit():
            value = int(token)
            if value in numeric:
                selected.add(value)
    return [str(value) for value in sorted(selected)]


def summarize_verses(selection: List[str]) -> str:
    if not selection:
        return ""
    numbers = sorted({int(value) for value in selection if value.isdigit()})
    if not numbers:
        return ""
    ranges: List[str] = []
    start = prev = numbers[0]
    for num in numbers[1:]:
        if num == prev + 1:
            prev = num
            continue
        if start == prev:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{prev}")
        start = prev = num
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{prev}")
    return ", ".join(ranges)


def build_context_text(verses: Dict[str, str], selection: List[str]) -> str:
    entries = [f"{key}. {verses[key]}" for key in selection if verses.get(key)]
    return "\n".join(entries)


def get_testament_for_book(book_abbrev: str) -> str:
    """Identifica se um livro pertence ao Velho ou Novo Testamento baseado na abreviação."""
    # Normalizar a abreviação para lowercase para comparação
    abbrev_lower = book_abbrev.lower() if book_abbrev else ""
    
    # Livros do Novo Testamento começam em Mateus
    new_testament = {"mt", "mc", "lc", "jo", "at", "rm", "1co", "2co", "gl", "ef", "fp", "cl", 
                     "1ts", "2ts", "1tm", "2tm", "tt", "fm", "hb", "tg", "1pe", "2pe", "1jo", 
                     "2jo", "3jo", "jd", "ap"}
    
    return "NT" if abbrev_lower in new_testament else "VT"


def get_book_category(book_abbrev: str) -> str:
    """Retorna a categoria teológica de um livro bíblico."""
    abbrev_lower = book_abbrev.lower() if book_abbrev else ""
    
    # Livros da Lei (Pentateuco)
    law_books = {"gn", "ex", "lv", "nm", "dt"}
    
    # Livros Históricos
    historical_books = {"js", "jz", "rt", "1sm", "2sm", "1rs", "2rs", "1cr", "2cr", 
                        "ed", "ne", "et"}
    
    # Livros Poéticos e de Sabedoria
    poetic_books = {"job", "sl", "pv", "ec", "ct"}  # ct = Cânticos/Cantares
    
    # Livros Proféticos Maiores
    major_prophets = {"is", "jr", "lm", "ez", "dn"}
    
    # Livros Proféticos Menores
    minor_prophets = {"os", "jl", "am", "ob", "jn", "mq", "na", "hc", "sf", "ag", "zc", "ml"}
    
    # Evangelhos
    gospels = {"mt", "mc", "lc", "jo"}
    
    # Livro Histórico do NT
    acts = {"at"}
    
    # Epístolas Paulinas
    pauline_epistles = {"rm", "1co", "2co", "gl", "ef", "fp", "cl", "1ts", "2ts", 
                        "1tm", "2tm", "tt", "fm"}
    
    # Epístolas Gerais
    general_epistles = {"hb", "tg", "1pe", "2pe", "1jo", "2jo", "3jo", "jd"}
    
    # Livro Apocalíptico
    apocalyptic = {"ap"}
    
    # Determinar categoria
    if abbrev_lower in law_books:
        return "Lei/Pentateuco"
    elif abbrev_lower in historical_books:
        return "Histórico"
    elif abbrev_lower in poetic_books:
        return "Poético/Sabedoria"
    elif abbrev_lower in major_prophets:
        return "Profético Maior"
    elif abbrev_lower in minor_prophets:
        return "Profético Menor"
    elif abbrev_lower in gospels:
        return "Evangelho"
    elif abbrev_lower in acts:
        return "Histórico do NT"
    elif abbrev_lower in pauline_epistles:
        return "Epístola Paulina"
    elif abbrev_lower in general_epistles:
        return "Epístola Geral"
    elif abbrev_lower in apocalyptic:
        return "Apocalíptico"
    else:
        return "Desconhecido"


def get_books_by_testament(data: Dict, version: str, testament: str = "ALL") -> List[Tuple[str, Dict]]:
    """Obtém livros filtrados por testamento (VT, NT ou ALL)."""
    all_books = get_books_for_version(data, version)
    if testament == "ALL":
        return all_books
    # Usa a abreviação (abbrev) para determinar o testamento, não a chave
    return [(name, book) for name, book in all_books 
            if get_testament_for_book(book.get("abbrev", "")) == testament]


def suggest_books_for_theme(keywords: List[str]) -> List[str]:
    """Sugere livros bíblicos baseado em palavras-chave do tema."""
    keywords_lower = [k.lower() for k in keywords]
    suggested_books = []
    
    # Temas musicais/louvor
    music_keywords = {"música", "musica", "louvor", "cântico", "cantico", "orquestra", 
                      "instrumento", "alegria", "celebração", "celebracao", "adoração", 
                      "adoracao", "hino", "salmo", "levita"}
    
    # Temas de liderança/servo
    leadership_keywords = {"lider", "líder", "servo", "servir", "serviço", "servico", 
                           "ministério", "ministerio", "pastor", "presbítero", "presbitero"}
    
    # Temas de família/casamento
    family_keywords = {"casamento", "família", "familia", "esposa", "esposo", "marido", 
                      "mulher", "filhos", "pais", "submissão", "submissao"}
    
    # Temas de fé/salvação
    faith_keywords = {"fé", "fe", "salvação", "salvacao", "graça", "graca", "perdão", 
                     "perdao", "cruz", "jesus", "cristo", "evangelho"}
    
    # Verificar temas
    is_music = any(k in music_keywords for k in keywords_lower)
    is_leadership = any(k in leadership_keywords for k in keywords_lower)
    is_family = any(k in family_keywords for k in keywords_lower)
    is_faith = any(k in faith_keywords for k in keywords_lower)
    
    # Sugerir livros baseado no tema
    if is_music:
        # Salmos (louvor), Crônicas (levitas músicos), Neemias (organização do templo)
        suggested_books.extend(["Salmos", "1 Crônicas", "2 Crônicas", "Neemias", "Esdras"])
    
    if is_leadership:
        # Timóteo, Tito (instruções pastorais), Atos (liderança da igreja)
        suggested_books.extend(["1 Timóteo", "2 Timóteo", "Tito", "Atos", "1 Pedro"])
    
    if is_family:
        # Efésios 5, Colossenses 3, 1 Pedro 3, Provérbios
        suggested_books.extend(["Efésios", "Colossenses", "1 Pedro", "Provérbios", "Gênesis"])
    
    if is_faith:
        # Romanos, Efésios, João, Hebreus
        suggested_books.extend(["Romanos", "Efésios", "João", "Hebreus", "Gálatas"])
    
    # Se não identificou tema específico, retornar livros gerais
    if not suggested_books:
        suggested_books = ["Salmos", "Provérbios", "João", "Romanos"]
    
    return suggested_books


def search_verses_by_keywords(chapters: Dict, keywords: List[str], max_results: int = 10) -> List[Tuple[str, str, str]]:
    """Busca versículos que contenham palavras-chave do tema.
    
    Returns:
        Lista de tuplas (chapter_num, verse_num, verse_text)
    """
    keywords_lower = [k.lower() for k in keywords if k]
    if not keywords_lower:
        return []
    
    # Expandir keywords com sinônimos e variações
    expanded_keywords = set(keywords_lower)
    for keyword in keywords_lower:
        if "musica" in keyword or "música" in keyword:
            expanded_keywords.update(["cântico", "cantico", "louvor", "instrumento", 
                                     "harpa", "lira", "címbalo", "trombeta", "levita", 
                                     "cantar", "cantai", "salmo"])
        elif "alegria" in keyword:
            expanded_keywords.update(["júbilo", "jubilo", "gozo", "regozijo", "alegrai"])
        elif "servo" in keyword or "servir" in keyword:
            expanded_keywords.update(["serviço", "servico", "ministrar", "ministério", 
                                     "ministerio", "trabalho", "obra"])
        elif "adoração" in keyword or "adoracao" in keyword:
            expanded_keywords.update(["adorar", "adorai", "prostrai", "louvar"])
    
    matching_verses = []
    
    for ch_num, ch_data in chapters.items():
        verses = ch_data.get("verses", {})
        for v_num, v_text in verses.items():
            v_text_lower = v_text.lower()
            
            # Contar quantas keywords aparecem no versículo
            match_count = sum(1 for kw in expanded_keywords if kw in v_text_lower)
            
            if match_count > 0:
                matching_verses.append((ch_num, v_num, v_text, match_count))
    
    # Ordenar por relevância (número de matches) e limitar resultados
    matching_verses.sort(key=lambda x: x[3], reverse=True)
    
    # Retornar sem o match_count
    return [(ch, v, text) for ch, v, text, _ in matching_verses[:max_results]]


def collect_verses_from_books(data: Dict, version: str, book_keys: List[str], max_verses: int = 10, randomize: bool = False, include_metadata: bool = False, theme_keywords: List[str] = None) -> str:
    """Coleta versículos de múltiplos livros para usar como contexto.
    
    Args:
        data: Dados da Bíblia
        version: Versão da Bíblia
        book_keys: Lista de chaves de livros
        max_verses: Número máximo de versículos por livro
        randomize: Se True, seleciona livros e versículos aleatórios
        include_metadata: Se True, inclui categoria teológica de cada livro
        theme_keywords: Lista de palavras-chave para filtrar versículos relevantes ao tema
    """
    version_books = data.get("versions", {}).get(version, {}).get("books", {})
    collected_text = []
    
    # Se randomize, embaralhar a lista de livros
    books_to_process = book_keys.copy()
    if randomize:
        random.shuffle(books_to_process)
    
    # Priorizar livros específicos baseado em palavras-chave do tema
    if theme_keywords:
        priority_books = suggest_books_for_theme(theme_keywords)
        # Mover livros prioritários para o início
        for priority_book in reversed(priority_books):
            if priority_book in books_to_process:
                books_to_process.remove(priority_book)
                books_to_process.insert(0, priority_book)
    
    for book_key in books_to_process:
        book_entry = version_books.get(book_key)
        if not book_entry:
            continue
        
        book_name = book_entry.get("name", book_key)
        book_abbrev = book_entry.get("abbrev", "")
        chapters = book_entry.get("chapters", {})
        
        if not chapters:
            continue
        
        # Obter categoria do livro se metadata estiver habilitado
        category_info = ""
        if include_metadata and book_abbrev:
            category = get_book_category(book_abbrev)
            testament = get_testament_for_book(book_abbrev)
            category_info = f" [Categoria: {category}, Testamento: {testament}]"
        
        # Se há palavras-chave do tema, buscar versículos relevantes
        if theme_keywords:
            relevant_verses = search_verses_by_keywords(chapters, theme_keywords, max_verses)
            if relevant_verses:
                # Adicionar header com metadata se habilitado
                if include_metadata:
                    collected_text.append(f"=== {book_name}{category_info} ===")
                
                for ch_num, v_key, verse_text in relevant_verses:
                    collected_text.append(f"{book_name} {ch_num}:{v_key} - {verse_text}")
                continue  # Pular seleção aleatória se encontrou versículos relevantes
        
        # Seleção padrão (aleatória) se não há palavras-chave ou não encontrou versículos relevantes
        chapter_keys = sorted(chapters.keys(), key=int)
        if randomize and len(chapter_keys) > 1:
            # Preferir capítulos do meio do livro (mais conteúdo relevante)
            mid_start = len(chapter_keys) // 4
            mid_end = (len(chapter_keys) * 3) // 4
            selected_chapter = random.choice(chapter_keys[mid_start:mid_end] if mid_end > mid_start else chapter_keys)
        else:
            selected_chapter = chapter_keys[0]
        
        verses = chapters[selected_chapter].get("verses", {})
        if not verses:
            continue
        
        # Selecionar versículos
        verse_keys = sorted(verses.keys(), key=int)
        if randomize and len(verse_keys) > max_verses:
            # Selecionar versículos aleatórios (evitar sempre o início)
            start_idx = random.randint(0, max(0, len(verse_keys) - max_verses - 1))
            selected_verses = verse_keys[start_idx:start_idx + max_verses]
        else:
            selected_verses = verse_keys[:max_verses]
        
        # Adicionar header com metadata se habilitado
        if include_metadata:
            collected_text.append(f"=== {book_name}{category_info} ===")
        
        for v_key in selected_verses:
            collected_text.append(f"{book_name} {selected_chapter}:{v_key} - {verses[v_key]}")
    
    return "\n\n".join(collected_text)


def render_reference_selectors(
    prefix: str,
    data: Dict,
    version: str,
    key_suffix: str,
    trans: Dict,
    include_verse_selector: bool = True,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], List[str]]:
    """Renderiza seletores para livro, capítulo e versículo."""
    books = get_books_for_version(data, version)
    if not books:
        return None, None, None, None, None, []
    
    key = f"{key_suffix}_book"
    # Agora books tem nomes traduzidos como chaves
    # Não precisa mais de book_label_map, os nomes já estão corretos
    book_key = st.selectbox(
        f"{prefix} {t(trans, 'labels.book_selector', 'Livro')}",
        [item[0] for item in books],  # item[0] já é o nome traduzido
        format_func=_format_book_label,
        key=key,
        index=0,
    )
    book_entry = dict(books).get(book_key)
    if not book_entry:
        return None, None, None, None, None, []
    
    # book_key já é o nome traduzido (ex: "創世記" em japonês, "Genèse" em francês)
    book_label = book_entry.get("name") or book_entry.get("abbrev") or book_key
    chapters = get_chapters(book_entry)
    if not chapters:
        return book_key, book_label, None, None, None, []
    chapter_key = f"{key_suffix}_chapter"
    chapter = st.selectbox(f"{prefix} {t(trans, 'labels.chapter_selector', 'Capítulo')}", chapters, key=chapter_key, index=0)
    verse_options = sorted(
        book_entry.get("chapters", {}).get(chapter, {}).get("verses", {}).keys(),
        key=int,
    )
    if not verse_options:
        return book_key, book_label, chapter, None, None, []
    default_verse = verse_options[0]
    if include_verse_selector:
        verse_key = f"{key_suffix}_verse"
        verse = st.selectbox(f"{prefix} {t(trans, 'labels.verse_selector', 'Versículo')}", verse_options, key=verse_key)
        reference_text = get_verse(book_entry, chapter, verse)
        return book_key, book_label, chapter, verse, reference_text, verse_options
    reference_text = get_verse(book_entry, chapter, default_verse)
    return book_key, book_label, chapter, default_verse, reference_text, verse_options


def display_context_card(book: str, chapter: str, verse_label: str, verse_text: str, trans: Dict = None) -> None:
    if trans is None:
        trans = {}
    header = f"**{t(trans, 'formatting.selected_context', 'Contexto selecionado:')}** {book} {chapter}"
    if verse_label:
        header += f":{verse_label}"
    st.markdown(
        f"{header}\n\n{verse_text}"
    )


def rerun() -> None:
    rerun_func: Optional[Callable[[], None]] = getattr(st, "experimental_rerun", None)
    if rerun_func is not None:
        try:
            rerun_func()
        except RuntimeError:
            pass


def main() -> None:
    st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)
    
    # Inicializar históricos do ChromaDB (apenas uma vez por sessão)
    if 'histories_loaded' not in st.session_state:
        st.session_state.study_history = load_from_chromadb("study_history")
        st.session_state.sermon_history = load_from_chromadb("sermon_history")
        st.session_state.devotional_history = load_from_chromadb("devotional_history")
        st.session_state.chat_conversation_history = load_from_chromadb("chat_history")
        st.session_state.chat_history = []  # Chat em tempo real (não persiste)
        st.session_state.questions_history = load_from_chromadb("questions_history")
        st.session_state.histories_loaded = True
    
    # Carregar idiomas disponíveis e configuração
    available_languages = get_available_languages()
    app_config = load_app_config()
    saved_language = app_config.get("language", "pt")
    
    # Garantir que o idioma salvo está disponível
    if saved_language not in available_languages:
        saved_language = "pt"
    
    # Carregar traduções ANTES de usar
    # Usamos saved_language para carregar as traduções iniciais
    trans = load_translation(saved_language)
    
    # Seletor de idioma na sidebar (no topo)
    lang_code = st.sidebar.selectbox(
        t(trans, "labels.language_selector", "🌍 Idioma"),
        options=list(available_languages.keys()),
        format_func=lambda x: available_languages[x],
        index=list(available_languages.keys()).index(saved_language) if saved_language in available_languages else 0,
        key="language_selector"
    )
    
    # Salvar idioma selecionado e recarregar traduções se mudou
    if lang_code != saved_language:
        app_config["language"] = lang_code
        save_app_config(app_config)
        # Recarregar traduções com o novo idioma
        trans = load_translation(lang_code)
    
    st.sidebar.divider()
    
    # Botão para limpar cache e recarregar dados
    if st.sidebar.button("🔄 " + t(trans, 'buttons.clear_cache', 'Limpar Cache'), use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Carregar dados da Bíblia do idioma selecionado
    bible_data = cached_data_by_language(lang_code)
    versions = list_versions(bible_data)
    data_available = bool(versions)

    if not data_available:
        # Verificar se existe pasta mas sem dados
        lang_dir = LOCAL_JSON_DIR / lang_code
        if lang_dir.exists():
            json_files = list(lang_dir.glob("*.json"))
            if json_files:
                lang_name = available_languages.get(lang_code, lang_code)
                msg1 = t(trans, 'messages.no_data_in_files', f'Os arquivos de {lang_name} existem mas estão vazios.')
                msg2 = t(trans, 'messages.import_data_help', 'Use a aba "📥 Importar Dados" para baixar o conteúdo bíblico.')
                st.info(f"📖 {msg1} {msg2}")
            else:
                lang_name = available_languages.get(lang_code, lang_code)
                msg = t(trans, "messages.no_version", f"📖 Nenhuma versão bíblica carregada para {lang_name}. Use a aba '📥 Importar Dados' para começar!")
                st.info(msg)
        else:
            lang_name = available_languages.get(lang_code, lang_code)
            msg = t(trans, "messages.no_version", f"📖 Nenhuma versão bíblica carregada para {lang_name}. Use a aba '📥 Importar Dados' para começar!")
            st.info(msg)

    # Carregar configurações salvas
    app_config = load_app_config()
    default_version_saved = app_config.get("default_version")
    
    if versions:
        # Determinar o índice padrão
        if default_version_saved and default_version_saved in versions:
            default_index = versions.index(default_version_saved)
        else:
            default_index = 0
        
        version = st.sidebar.selectbox(t(trans, "labels.bible_version", "Versão da Bíblia"), versions, index=default_index)
        
        # Checkbox para definir como padrão (só aparece se houver mais de uma versão)
        if len(versions) > 1:
            col1, col2 = st.sidebar.columns([3, 1])
            with col2:
                is_current_default = (default_version_saved == version)
                set_default = st.checkbox(
                    "⭐",
                    value=is_current_default,
                    help=t(trans, "labels.set_default_version", "Definir como versão padrão ao iniciar"),
                    key="set_default_version"
                )
            with col1:
                if set_default and not is_current_default:
                    # Salvar nova versão padrão
                    app_config["default_version"] = version
                    save_app_config(app_config)
                    st.caption(f"{t(trans, 'captions.default_pattern', '✅ Padrão:')} {version}")
                elif not set_default and is_current_default:
                    # Remover versão padrão
                    app_config["default_version"] = None
                    save_app_config(app_config)
                elif is_current_default:
                    st.caption(f"{t(trans, 'captions.default_pattern', '✅ Padrão:')} {version}")
    else:
        st.sidebar.caption(t(trans, "messages.no_local_versions", "Nenhuma versão local encontrada. Use Importar Dados para carregar conteúdo."))
        version = None

    models = list_ollama_models()
    default_model = models[0] if models else OLLAMA_MODEL_DEFAULT
    model_input = st.sidebar.text_input(
        t(trans, "labels.ollama_model", "Modelo Ollama (ou digite)"), 
        value=default_model
    )
    selected_model = model_input
    ollama_online, connection_status = check_ollama_online()
    status_label = t(trans, "labels.ollama_status_online", "Online") if ollama_online else t(trans, "labels.ollama_status_offline", "Offline")
    status_hint = connection_status or t(trans, "labels.ollama_help", "Conecta ao servidor local")
    st.sidebar.metric(
        t(trans, "labels.ollama_status", "Status Ollama"), 
        status_label, 
        status_hint
    )
    st.sidebar.caption(t(trans, "labels.ollama_help", "Se os modelos não aparecerem, use 'ollama pull <modelo>' via terminal."))

    tabs = st.tabs([
        t(trans, "menu.reading", "📖 Leitura & Exegese"),
        t(trans, "menu.sermon_gen", "🗣️ Gerador Sermões"),
        t(trans, "menu.devotional", "🧘 Devocional & Meditação"),
        t(trans, "menu.chat", "💬 Chat Teológico"),
        t(trans, "menu.questions", "❓ Gerar Perguntas"),
        t(trans, "menu.import", "📥 Importar Dados"),
    ])

    with tabs[0]:
        # Criar subtabs dentro de Leitura & Exegese
        reading_subtabs = st.tabs([
            t(trans, "menu.reading", "📖 Leitura"),
            t(trans, "menu.history", "📚 Histórico de Estudos")
        ])
        
        with reading_subtabs[0]:
            st.subheader(t(trans, "labels.guided_reading", "Leitura Guiada"))
            if not data_available or not version:
                st.info(t(trans, "messages.no_data", "Importe uma versão bíblica para começar a leitura guiada."))
            else:
                ex_book_key, ex_book_label, ex_chapter, _, ex_text, ex_options = render_reference_selectors(
                    t(trans, "labels.base_book", "Base"), bible_data, version, "exegese", trans=trans, include_verse_selector=False
                )
                version_books = bible_data.get("versions", {}).get(version, {}).get("books", {})
                book_entry = version_books.get(ex_book_key)
                if not book_entry or not ex_chapter or not ex_options:
                    st.warning(t(trans, "messages.select_book_chapter", "Selecione um livro e capítulo para começar a leitura guiada."))
                else:
                    chapter_data = book_entry.get("chapters", {}).get(ex_chapter, {})
                    verses_map = chapter_data.get("verses", {})
                    if not verses_map:
                        st.warning(t(trans, "messages.no_verses_chapter", "Nenhum versículo encontrado neste capítulo."))
                    else:
                        verse_input_key = "exegese_verse_selection"
                        chapter_state_key = "exegese_selected_chapter"
                        if st.session_state.get(chapter_state_key) != ex_chapter:
                            st.session_state[chapter_state_key] = ex_chapter
                            st.session_state[verse_input_key] = ""
                        st.session_state.setdefault(verse_input_key, "")
                        verse_selection = st.text_input(
                            t(trans, "labels.verses", "Versículos (ex: 1, 1-5)"),
                            value=st.session_state[verse_input_key],
                            key=verse_input_key,
                            help=t(trans, "labels.verses_help", "Informe um único versículo ou um intervalo para usar como base ou deixe em branco para o capítulo inteiro."),
                        )
                        cleaned_selection = verse_selection.strip()
                        selected_verses = parse_verse_selection(cleaned_selection, ex_options) if cleaned_selection else []
                        if cleaned_selection and not selected_verses:
                            st.warning(t(trans, "messages.invalid_verse_syntax", "Nenhum versículo correspondente foi encontrado. Revise a sintaxe ou use vírgulas/intervalos."))
                        verse_keys_for_context: List[str]
                        if selected_verses:
                            verse_keys_for_context = selected_verses
                        else:
                            verse_keys_for_context = sorted(verses_map.keys(), key=int)
                        verse_label = summarize_verses(selected_verses) if selected_verses else t(trans, "labels.full_chapter", "Capítulo inteiro")
                        context_text = build_context_text(verses_map, verse_keys_for_context) or ex_text
                        highlighted = set(selected_verses)
                        display_context_card(ex_book_label or ex_book_key, ex_chapter, verse_label, context_text, trans)
                        
                        # Opção de comparar versões (só aparece se houver mais de uma versão e versículos específicos selecionados)
                        compare_versions_enabled = False
                        if len(versions) > 1 and selected_verses:
                            compare_versions_enabled = st.checkbox(
                                t(trans, "labels.compare_versions", "🔍 Comparar com outras versões"),
                                key="compare_versions_reading",
                                help=t(trans, "labels.compare_versions_help", "Compare o texto selecionado em diferentes traduções bíblicas")
                            )
                        
                        # Botões de ação
                        if compare_versions_enabled:
                            col_btn1, col_btn2 = st.columns(2)
                            
                            # Botão para gerar explicação
                            with col_btn1:
                                if st.button(t(trans, "buttons.generate_explanation", "✨ Gerar Explicação Bíblica"), key="explain", type="primary", use_container_width=True):
                                    online, offline_reason = check_ollama_online()
                                    if not online:
                                        detail = offline_reason or "Sem resposta do servidor."
                                        st.error(t(trans, "messages.ollama_offline_detail", "Ollama esta offline ({detail}). Ligue o servidor e tente novamente.").format(detail=detail))
                                    else:
                                        with st.spinner(t(trans, "messages.generating_explanation", "🔮 Gerando explicação bíblica...")):
                                            # Criar referência completa
                                            reference = f"{ex_book_label or ex_book_key} {ex_chapter}:{verse_label}"
                                            prompt = build_prompt(
                                                context_text,
                                                t(trans, "prompts.explain_context", "Explique o contexto historico e teologico, pondere sobre palavras-chave e sugira aplicacoes pastorais."),
                                                reference=reference
                                            )
                                            ok, message = query_ollama(selected_model, prompt, max_tokens=1500, auto_continue=True, lang_code=lang_code)
                                        if ok:
                                            # Salvar no histórico
                                            if "study_history" not in st.session_state:
                                                st.session_state.study_history = []
                                            study_entry = {
                                                "timestamp": time.time(),
                                                "book": ex_book_label or ex_book_key,
                                                "chapter": ex_chapter,
                                                "verses": verse_label,
                                                "context": context_text,
                                                "explanation": message,
                                                "version": version,
                                                "model": selected_model
                                            }
                                            st.session_state.study_history.insert(0, study_entry)
                                            auto_save_history("study_history", st.session_state.study_history)
                                            st.success(t(trans, "messages.explanation_saved", "✅ Explicação gerada e salva no histórico!"))
                                            st.info(t(trans, "messages.check_history_tab", "📚 Acesse a aba 'Histórico de Estudos' para ver todas as suas análises."))
                                            # Mostrar preview
                                            with st.expander(t(trans, "expanders.explanation_preview", "👁️ Prévia da Explicação"), expanded=True):
                                                st.markdown(message)
                                        else:
                                            st.error(message)
                            
                            # Botão para comparar versões
                            with col_btn2:
                                if st.button(t(trans, "buttons.compare_versions", "🔍 Comparar Versões"), key="compare_versions_btn", type="secondary", use_container_width=True):
                                    online, offline_reason = check_ollama_online()
                                    if not online:
                                        detail = offline_reason or "Sem resposta do servidor."
                                        st.error(t(trans, "messages.ollama_offline_detail", "Ollama esta offline ({detail}). Ligue o servidor e tente novamente.").format(detail=detail))
                                    else:
                                        with st.spinner(t(trans, "messages.comparing_versions", "🔍 Comparando versões bíblicas...")):
                                            # Coletar texto de todas as versões disponíveis
                                            comparison_texts = []
                                            reference = f"{ex_book_label or ex_book_key} {ex_chapter}:{verse_label}"
                                            
                                            for ver in versions:
                                                ver_books = bible_data.get("versions", {}).get(ver, {}).get("books", {})
                                                ver_book_entry = ver_books.get(ex_book_key)
                                                if ver_book_entry:
                                                    ver_chapter_data = ver_book_entry.get("chapters", {}).get(ex_chapter, {})
                                                    ver_verses_map = ver_chapter_data.get("verses", {})
                                                    ver_context_text = build_context_text(ver_verses_map, verse_keys_for_context)
                                                    if ver_context_text:
                                                        comparison_texts.append(f"**{ver}:**\n{ver_context_text}")
                                            
                                            # Criar contexto de comparação
                                            full_comparison = "\n\n".join(comparison_texts)
                                            
                                            # Criar prompt específico para comparação
                                            compare_request = t(trans, "prompts.compare_versions", 
                                                "Compare estas diferentes traduções do mesmo texto bíblico. Analise as diferenças de tradução, "
                                                "explique possíveis razões para as variações (manuscritos originais, escolhas de tradução, etc.), "
                                                "e indique qual o impacto teológico ou interpretativo dessas diferenças.")
                                            
                                            prompt = build_prompt(full_comparison, compare_request, reference=reference)
                                            ok, comparison_result = query_ollama(selected_model, prompt, max_tokens=1800, auto_continue=True, lang_code=lang_code)
                                        
                                        if ok:
                                            # Salvar no histórico com marcação de comparação
                                            if "study_history" not in st.session_state:
                                                st.session_state.study_history = []
                                            study_entry = {
                                                "timestamp": time.time(),
                                                "book": ex_book_label or ex_book_key,
                                                "chapter": ex_chapter,
                                                "verses": verse_label,
                                                "context": full_comparison,
                                                "explanation": comparison_result,
                                                "version": f"{len(versions)} versões comparadas: {', '.join(versions)}",
                                                "model": selected_model,
                                                "is_comparison": True
                                            }
                                            st.session_state.study_history.insert(0, study_entry)
                                            auto_save_history("study_history", st.session_state.study_history)
                                            st.success(t(trans, "messages.comparison_saved", "✅ Comparação gerada e salva no histórico!"))
                                            st.info(t(trans, "messages.check_history_tab", "📚 Acesse a aba 'Histórico de Estudos' para ver todas as suas análises."))
                                            
                                            # Mostrar preview da comparação
                                            with st.expander(t(trans, "expanders.comparison_preview", "👁️ Prévia da Comparação"), expanded=True):
                                                st.markdown("### " + t(trans, "headers.versions_compared", "Versões Comparadas:"))
                                                st.markdown(full_comparison)
                                                st.markdown("---")
                                                st.markdown("### " + t(trans, "headers.comparative_analysis", "Análise Comparativa:"))
                                                st.markdown(comparison_result)
                                        else:
                                            st.error(comparison_result)
                        else:
                            # Botão único quando não há comparação
                            if st.button(t(trans, "buttons.generate_explanation", "✨ Gerar Explicação Bíblica"), key="explain", type="primary", use_container_width=True):
                                online, offline_reason = check_ollama_online()
                                if not online:
                                    detail = offline_reason or "Sem resposta do servidor."
                                    st.error(t(trans, "messages.ollama_offline_detail", "Ollama esta offline ({detail}). Ligue o servidor e tente novamente.").format(detail=detail))
                                else:
                                    with st.spinner(t(trans, "messages.generating_explanation", "🔮 Gerando explicação bíblica...")):
                                        # Criar referência completa
                                        reference = f"{ex_book_label or ex_book_key} {ex_chapter}:{verse_label}"
                                        prompt = build_prompt(
                                            context_text,
                                            t(trans, "prompts.explain_context", "Explique o contexto historico e teologico, pondere sobre palavras-chave e sugira aplicacoes pastorais."),
                                            reference=reference
                                        )
                                        ok, message = query_ollama(selected_model, prompt, max_tokens=1500, auto_continue=True, lang_code=lang_code)
                                    if ok:
                                        # Salvar no histórico
                                        if "study_history" not in st.session_state:
                                            st.session_state.study_history = []
                                        study_entry = {
                                            "timestamp": time.time(),
                                            "book": ex_book_label or ex_book_key,
                                            "chapter": ex_chapter,
                                            "verses": verse_label,
                                            "context": context_text,
                                            "explanation": message,
                                            "version": version,
                                            "model": selected_model
                                        }
                                        st.session_state.study_history.insert(0, study_entry)
                                        auto_save_history("study_history", st.session_state.study_history)
                                        st.success(t(trans, "messages.explanation_saved", "✅ Explicação gerada e salva no histórico!"))
                                        st.info(t(trans, "messages.check_history_tab", "📚 Acesse a aba 'Histórico de Estudos' para ver todas as suas análises."))
                                        # Mostrar preview
                                        with st.expander(t(trans, "expanders.explanation_preview", "👁️ Prévia da Explicação"), expanded=True):
                                            st.markdown(message)
                                    else:
                                        st.error(message)
                        
                        st.markdown("---")
                        # Exibir página completa do capítulo
                        render_book_page(
                            ex_book_label or ex_book_key,
                            book_entry,
                            ex_chapter,
                            highlighted,
                            trans,
                        )
        
        with reading_subtabs[1]:
            st.subheader(t(trans, "headers.bible_studies_history", "📚 Histórico de Estudos Bíblicos"))
            
            if "study_history" not in st.session_state:
                st.session_state.study_history = []
            
            history = st.session_state.study_history
            
            if not history:
                st.info(t(trans, "messages.no_studies_yet", "Nenhum estudo foi gerado ainda. Vá para a aba 'Leitura & Exegese' e clique em 'Gerar Explicacao' para começar."))
            else:
                # Barra de ferramentas
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    search_term = st.text_input(t(trans, "labels.search_history", "🔍 Buscar no histórico"), placeholder=t(trans, "labels.search_placeholder", "Digite livro, capítulo ou palavra-chave..."))
                with col2:
                    sort_order = st.selectbox(t(trans, "labels.sort_by", "Ordenar por"), [t(trans, "labels.most_recent", "Mais recente"), t(trans, "labels.oldest", "Mais antigo"), t(trans, "labels.by_book", "Livro")])
                with col3:
                    if st.button(t(trans, "buttons.clear_history", "🗑️ Limpar histórico"), use_container_width=True):
                        st.session_state.study_history = []
                        auto_save_history("study_history", st.session_state.study_history)
                        st.success(t(trans, "messages.history_cleared", "✅ Histórico limpo com sucesso!"))
                
                st.markdown("---")
                
                # Filtrar histórico
                filtered_history = history
                if search_term:
                    search_lower = search_term.lower()
                    filtered_history = [
                        entry for entry in history
                        if search_lower in entry["book"].lower()
                        or search_lower in entry.get("chapter", "").lower()
                        or search_lower in entry.get("verses", "").lower()
                        or search_lower in entry.get("context", "").lower()
                    ]
                
                # Ordenar
                if sort_order == t(trans, "labels.oldest", "Mais antigo"):
                    filtered_history = list(reversed(filtered_history))
                elif sort_order == t(trans, "labels.by_book", "Livro"):
                    filtered_history = sorted(filtered_history, key=lambda x: x["book"])
                
                if not filtered_history:
                    st.warning(t(trans, "messages.no_search_results", "Nenhum resultado encontrado para sua busca."))
                else:
                    st.caption(t(trans, "captions.studies_found", "📊 {count} estudo(s) encontrado(s)").format(count=len(filtered_history)))
                    
                    # Exibir cada estudo como um card expansível
                    for idx, entry in enumerate(filtered_history):
                        timestamp_str = time.strftime("%d/%m/%Y %H:%M", time.localtime(entry["timestamp"]))
                        reference = f"{entry['book']} {entry['chapter']}:{entry['verses']}"
                        
                        # Verificar se é uma comparação
                        is_comparison = entry.get("is_comparison", False)
                        icon = "🔍" if is_comparison else "📖"
                        border_color = "#ff6b6b" if is_comparison else "#ffd700"
                        
                        # Card personalizado
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    border-radius: 15px;
                                    padding: 1.5rem;
                                    margin-bottom: 1rem;
                                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                                    border-left: 5px solid {border_color};
                                ">
                                    <h3 style="color: white; margin: 0 0 0.5rem 0;">{icon} {reference}</h3>
                                    <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0;">
                                        🕐 {timestamp_str} | 📚 {entry.get('version', 'N/A')} | 🤖 {entry.get('model', 'N/A')}
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Expander de contexto (com título apropriado para comparação ou contexto)
                            # Expander de contexto (com título apropriado para comparação ou contexto)
                            context_title = t(trans, "expanders.versions_compared", "🔍 Ver Versões Comparadas") if is_comparison else t(trans, "expanders.biblical_context", "📜 Ver Contexto Bíblico")
                            with st.expander(context_title, expanded=False):
                                st.markdown(
                                    f"""
                                    <div style="
                                        background: rgba(102, 126, 234, 0.15);
                                        border-left: 4px solid #667eea;
                                        padding: 1rem;
                                        border-radius: 8px;
                                        font-family: 'Georgia', serif;
                                        line-height: 1.8;
                                        color: inherit;
                                    ">
                                        {html.escape(entry['context']).replace(chr(10), '<br>')}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            
                            # Expander de explicação (com título apropriado para análise comparativa ou explicação)
                            explanation_title = t(trans, "expanders.comparative_analysis", "📊 Ver Análise Comparativa") if is_comparison else t(trans, "expanders.full_explanation", "💡 Ver Explicação Completa")
                            with st.expander(explanation_title, expanded=False):
                                st.markdown(
                                    f"""
                                    <div style="
                                        background: rgba(118, 75, 162, 0.1);
                                        padding: 1.5rem;
                                        border-radius: 12px;
                                        border: 2px solid rgba(102, 126, 234, 0.5);
                                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
                                        color: inherit;
                                    ">
                                        {entry['explanation']}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            
                            # Ações
                            col_a, col_b, col_c = st.columns([1, 1, 1])
                            with col_a:
                                if st.button(t(trans, "buttons.copy", "📋 Copiar"), key=f"copy_{idx}", use_container_width=True):
                                    context_label = t(trans, "formatting.context_label", "Contexto:")
                                    explanation_label = t(trans, "formatting.explanation_label", "Explicação:")
                                    full_text = f"**{reference}**\n\n**{context_label}**\n{entry['context']}\n\n**{explanation_label}**\n{entry['explanation']}"
                                    st.code(full_text, language=None)
                                    st.success(t(trans, "messages.ready_to_copy", "Texto pronto para copiar!"))
                            with col_b:
                                # Botão de geração de PDF
                                if st.button(t(trans, "buttons.generate_pdf", "📄 Gerar PDF"), key=f"pdf_{idx}", use_container_width=True):
                                    pdf_buffer = generate_study_pdf(entry, trans)
                                    pdf_filename = f"estudo_biblico_{entry['book']}_{entry['chapter']}_{entry['verses'].replace(',', '_').replace('-', '_')}_{int(entry['timestamp'])}.pdf"
                                    
                                    # Criar botão de download
                                    b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" style="display:inline-block;padding:0.5rem 1rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:bold;box-shadow:0 4px 15px rgba(102,126,234,0.3);">📥 Baixar PDF</a>'
                                    st.markdown(href, unsafe_allow_html=True)
                                    st.success("✅ PDF gerado com sucesso!")
                            with col_c:
                                if st.button(t(trans, "buttons.delete", "🗑️ Excluir"), key=f"del_{idx}", use_container_width=True):
                                    st.session_state.study_history.pop(
                                        history.index(entry) if search_term or sort_order != t(trans, "labels.most_recent", "Mais recente") else idx
                                    )
                                    auto_save_history("study_history", st.session_state.study_history)
                                    st.toast(t(trans, "messages.study_deleted", "✅ Estudo excluído!"), icon="✅")
                            
                            st.markdown("<br>", unsafe_allow_html=True)

    with tabs[1]:
        # Criar subtabs dentro de Gerador de Sermões
        sermon_subtabs = st.tabs([
            t(trans, "menu.sermon_gen", "🗣️ Gerador"),
            t(trans, "menu.sermon_hist", "📋 Histórico")
        ])
        
        with sermon_subtabs[0]:
            st.subheader(t(trans, "headers.sermon_generator", "Gerador de Sermoes"))
            if not data_available or not version:
                st.info(t(trans, "messages.import_data_sermon", "Importe dados para começar a gerar um sermao."))
            else:
                # Seção de filtros de escopo
                st.markdown(f"#### {t(trans, 'headers.sermon_scope', '📚 Escopo do Sermão')}")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    scope_option = st.radio(
                        t(trans, "labels.sermon_scope_prompt", "Selecione o escopo para geração do sermão:"),
                        [
                            t(trans, "labels.sermon_scope_specific_book", "📖 Livro Específico"),
                            t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"),
                            t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"),
                            t(trans, "labels.sermon_scope_whole_bible", "🌍 Toda a Bíblia")
                        ],
                        key="sermon_scope_option"
                    )
                
                with col2:
                    use_multiple_books = st.checkbox(
                        t(trans, "labels.select_multiple_books", "🔖 Selecionar múltiplos livros"),
                        help=t(trans, "labels.select_multiple_books_help", "Marque para selecionar livros específicos manualmente"),
                        key="sermon_use_multiple"
                    )
                
                # Determinar quais livros usar
                selected_books = []
                context_description = ""
                
                if scope_option == t(trans, "labels.sermon_scope_specific_book", "📖 Livro Específico"):
                    # Modo original - um livro específico
                    book_key, book_label, chapter, _, sermon_text, verse_options = render_reference_selectors(
                        t(trans, "labels.sermon_book_label", "Sermao"), bible_data, version, "sermon", trans=trans, include_verse_selector=False
                    )
                    
                    # Adicionar seleção de múltiplos versículos
                    if book_key and chapter:
                        version_books = bible_data.get("versions", {}).get(version, {}).get("books", {})
                        book_entry = version_books.get(book_key)
                        if book_entry:
                            chapter_data = book_entry.get("chapters", {}).get(chapter, {})
                            verses_map = chapter_data.get("verses", {})
                            
                            verse_input_key = "sermon_verse_selection"
                            chapter_state_key = "sermon_selected_chapter"
                            if st.session_state.get(chapter_state_key) != chapter:
                                st.session_state[chapter_state_key] = chapter
                                st.session_state[verse_input_key] = ""
                            st.session_state.setdefault(verse_input_key, "")
                            
                            verse_selection = st.text_input(
                                t(trans, "labels.verses", "Versículos (ex: 1, 1-5, 10-15)"),
                                value=st.session_state[verse_input_key],
                                key=verse_input_key,
                                help=t(trans, "labels.verses_help", "Informe versículos específicos, intervalos, ou deixe em branco para o capítulo inteiro."),
                            )
                            
                            cleaned_selection = verse_selection.strip()
                            selected_verses = parse_verse_selection(cleaned_selection, verse_options) if cleaned_selection else []
                            
                            if cleaned_selection and not selected_verses:
                                st.warning(t(trans, "messages.invalid_verse_syntax", "Nenhum versículo correspondente foi encontrado. Revise a sintaxe."))
                            
                            # Determinar quais versículos usar
                            verse_keys_for_context = selected_verses if selected_verses else sorted(verses_map.keys(), key=int)
                            verse_label = summarize_verses(selected_verses) if selected_verses else t(trans, "labels.full_chapter", "Capítulo inteiro")
                            sermon_text = build_context_text(verses_map, verse_keys_for_context)
                            
                            selected_books = [book_key]
                            context_description = f"{t(trans, 'labels.book_colon', 'Livro:')} {book_label}, {t(trans, 'labels.chapter_colon', 'Capítulo')} {chapter}, {t(trans, 'labels.verse_colon', 'Versículo(s):')} {verse_label}"
                        else:
                            selected_books = [book_key] if book_key else []
                            context_description = f"{t(trans, 'labels.book_colon', 'Livro:')} {book_label}, {t(trans, 'labels.chapter_colon', 'Capítulo')} {chapter}"
                    else:
                        selected_books = [book_key] if book_key else []
                        context_description = f"{t(trans, 'labels.book_colon', 'Livro:')} {book_label}"
                    
                elif use_multiple_books:
                    # Seleção manual de múltiplos livros
                    if scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        available_books = get_books_by_testament(bible_data, version, "VT")
                    elif scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        available_books = get_books_by_testament(bible_data, version, "NT")
                    else:  # Toda a Bíblia
                        available_books = get_books_by_testament(bible_data, version, "ALL")
                    
                    book_options = {abbr: entry.get("name", abbr) for abbr, entry in available_books}
                    selected_books = st.multiselect(
                        t(trans, "labels.select_books_for_sermon", "Selecione os livros para o sermão:"),
                        options=list(book_options.keys()),
                        format_func=lambda x: book_options[x],
                        default=[available_books[0][0]] if available_books else [],
                        key="sermon_selected_books"
                    )
                    context_description = f"{len(selected_books)} {t(trans, 'labels.selected_books_count', 'livro(s) selecionado(s):')} {', '.join([book_options[b] for b in selected_books[:3]])}{' ...' if len(selected_books) > 3 else ''}"
                    # Limitar a 8 livros e 2 versículos cada para múltiplos livros, com randomização e metadata
                    limited_books = selected_books[:8]
                    # Extrair palavras-chave do tema e notas para busca temática
                    theme_keywords = []
                    if 'sermon_tema' in st.session_state and st.session_state.sermon_tema:
                        theme_keywords.extend(st.session_state.sermon_tema.split())
                    if 'sermon_notes' in st.session_state and st.session_state.sermon_notes:
                        theme_keywords.extend(st.session_state.sermon_notes.split())
                    sermon_text = collect_verses_from_books(bible_data, version, limited_books, max_verses=2, randomize=True, include_metadata=True, theme_keywords=theme_keywords) if selected_books else ""
                    
                else:
                    # Usar todos os livros do escopo selecionado
                    if scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        available_books = get_books_by_testament(bible_data, version, "VT")
                        context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_old_testament', 'Todo o Velho Testamento')}"
                    elif scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        available_books = get_books_by_testament(bible_data, version, "NT")
                        context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_new_testament', 'Todo o Novo Testamento')}"
                    else:  # Toda a Bíblia
                        available_books = get_books_by_testament(bible_data, version, "ALL")
                        context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_bible', 'Toda a Bíblia')}"
                    
                    # Selecionar apenas 4 livros para processar mais rápido, priorizando livros relevantes ao tema
                    all_book_keys = [abbr for abbr, _ in available_books]
                    
                    # Extrair palavras-chave do tema e notas ANTES de coletar versículos
                    theme_keywords = []
                    if 'sermon_tema' in st.session_state and st.session_state.sermon_tema:
                        theme_keywords.extend(st.session_state.sermon_tema.split())
                    if 'sermon_notes' in st.session_state and st.session_state.sermon_notes:
                        theme_keywords.extend(st.session_state.sermon_notes.split())
                    
                    # Se há palavras-chave, sugerir livros relevantes e priorizar
                    if theme_keywords:
                        suggested = suggest_books_for_theme(theme_keywords)
                        # Filtrar apenas livros que existem no escopo
                        priority_books = [b for b in suggested if b in all_book_keys]
                        # Combinar prioritários + aleatórios até ter 4 livros
                        selected_books = priority_books[:4]
                        if len(selected_books) < 4:
                            remaining = [b for b in all_book_keys if b not in selected_books]
                            selected_books.extend(random.sample(remaining, min(4 - len(selected_books), len(remaining))))
                    else:
                        # Sem palavras-chave, seleção aleatória
                        selected_books = random.sample(all_book_keys, min(4, len(all_book_keys)))
                    
                    sermon_text = collect_verses_from_books(bible_data, version, selected_books, max_verses=1, randomize=True, include_metadata=True, theme_keywords=theme_keywords)
                
                st.info(f"📍 {context_description}")
                
                # Campos adicionais
                st.markdown(f"#### {t(trans, 'headers.sermon_style', '🎭 Persona/Estilo do Sermão')}")
                
                # Definir estilos de sermão
                sermon_styles = {
                    "🔍 Analítico-Essência": {
                        "subtitle": "O Investigador (Baseado em Jó)",
                        "description": "Psicologia espiritual, motivações ocultas, racionalidade da fé",
                        "icon": "🔍"
                    },
                    "📚 Expositivo-Teológico": {
                        "subtitle": "O Professor",
                        "description": "Contexto histórico, exegese, doutrina sólida",
                        "icon": "📚"
                    },
                    "🎬 Narrativo-Imersivo": {
                        "subtitle": "O Storyteller",
                        "description": "Atmosfera, sentidos, emoção, tensão dramática",
                        "icon": "🎬"
                    },
                    "💡 Devocional-Prático": {
                        "subtitle": "O Mentor",
                        "description": "Vida diária, consolo, resolução de problemas",
                        "icon": "💡"
                    },
                    "✝️ Cristocêntrico-Tipológico": {
                        "subtitle": "O Revelador",
                        "description": "Jesus em todo o texto, tipos e sombras, a Cruz",
                        "icon": "✝️"
                    },
                    "🔥 Profético-Confrontador": {
                        "subtitle": "O Atalaia",
                        "description": "Arrependimento, santidade, despertar, urgência",
                        "icon": "🔥"
                    },
                    "🛡️ Apologético-Filosófico": {
                        "subtitle": "O Defensor",
                        "description": "Lógica, razão, defesa da fé, resposta aos céticos",
                        "icon": "🛡️"
                    }
                }
                
                # Criar opções formatadas para o selectbox
                style_options = [f"{info['icon']} {style_name} - {info['subtitle']}" for style_name, info in sermon_styles.items()]
                
                sermon_style = st.selectbox(
                    t(trans, "labels.sermon_style_prompt", "Escolha a persona/estilo do sermão:"),
                    style_options,
                    key="sermon_style_option",
                    help=t(trans, "help.sermon_style", "Cada estilo possui tom, método e estrutura únicos. Escolha a persona que melhor se adequa ao seu público e objetivo.")
                )
                
                # Extrair o nome do estilo selecionado
                selected_style_name = sermon_style.split(" - ")[0].strip()
                
                # Mostrar descrição do estilo selecionado
                for style_name, info in sermon_styles.items():
                    if f"{info['icon']} {style_name}" == selected_style_name:
                        st.caption(f"📝 **Características:** {info['description']}")
                        break
                
                st.divider()
                
                tema = st.text_input(t(trans, "labels.theme_optional", "Tema (opcional)"), key="sermon_tema")
                publico = st.text_input(t(trans, "labels.audience_optional", "Público-alvo (opcional)"), key="sermon_publico")
                base_note = st.text_area(t(trans, "labels.extra_notes", "Notas extras (contexto do pregador)"), height=100, key="sermon_notes")
                
                if not sermon_text:
                    st.warning(t(trans, "messages.choose_verse_base", "Escolha um versiculo base ou escopo para que o modelo use como autoridade."))
                else:
                    if st.button(t(trans, "buttons.generate_sermon", "✨ Gerar Esboço de Sermão"), type="primary", use_container_width=True):
                        if not ollama_online:
                            st.error(t(trans, "messages.ollama_offline", "Ollama esta offline. Inicie o servidor local."))
                        else:
                            with st.spinner(t(trans, "messages.generating_sermon", "🎤 Gerando esboço de sermão...")):
                                scope_info = f" {t(trans, 'prompts.sermon_scope_info', 'O sermão deve abranger textos de:')} {context_description}."
                                
                                # Definir prompts específicos para cada estilo
                                style_prompts = {
                                    "🔍 Analítico-Essência": """
# ATIVAÇÃO DE PERSONA: ANALÍTICO-ESSÊNCIA (O Investigador - Baseado em Jó)

**FOCO:** Psicologia espiritual, motivações ocultas, "humanidade essência", racionalidade da fé.

### TOM E VOZ
* **Autoridade Reveladora:** Desvende um mistério espiritual profundo. Tom sério, sóbrio e extremamente detalhista.
* **Vocabulário Específico:** "humanidade essência", "racionalidade espiritual", "temor a Deus", "soberania", "Deus Jeová".
* **Didática Dialética:** Use perguntas retóricas que desafiem o senso comum.

### ESTRUTURA OBRIGATÓRIA
1. **A Introdução (O Gancho):** Visão popular do tema/personagem → proposta de investigação profunda
2. **O Cotidiano (A Base):** Vida diária do personagem antes do evento principal
3. **A Prova/Evento (A Reação):** Evento crítico e reação imediata
4. **A Análise Psicológica-Espiritual (O Núcleo):** Contraste, desconstrução, redefinição
5. **A Verdadeira Face (Conclusão):** Essência descoberta, ações externas = construção interna

**REGRAS:** Cite TEXTO COMPLETO dos versículos. Foque na INTENÇÃO, não na aparência. Evite autoajuda moderna.
""",
                                    "📚 Expositivo-Teológico": """
# ATIVAÇÃO DE PERSONA: EXPOSITIVO-TEOLÓGICO (O Professor)

**FOCO:** Contexto histórico, cultural, geográfico e linguístico (Grego/Hebraico). Exegese versículo por versículo.

### TOM E VOZ
* **Acadêmico, didático, claro, informativo.**
* Explique costumes da época, significados de palavras originais.
* Ensine doutrina sólida com autoridade bíblica.

### ESTRUTURA OBRIGATÓRIA
1. **Contexto Histórico:** Época, autor, destinatários, situação cultural
2. **Exegese das Palavras Chave:** Significados em Grego/Hebraico, uso no texto
3. **Verdade Doutrinária:** Princípio teológico extraído do texto
4. **Aplicação:** Como essa verdade se aplica hoje

**REGRAS:** Cite TEXTO COMPLETO dos versículos. Use termos técnicos quando necessário. Seja preciso e informativo.
""",
                                    "🎬 Narrativo-Imersivo": """
# ATIVAÇÃO DE PERSONA: NARRATIVO-IMERSIVO (O Storyteller)

**FOCO:** Atmosfera, sentidos (cheiro, som, visão), emoção, tensão dramática. Coloque o ouvinte dentro da cena.

### TOM E VOZ
* **Descritivo, emocional, cinematográfico.**
* Recontar a história no TEMPO PRESENTE.
* Descreva o ambiente e os sentimentos dos personagens como se estivesse lá.

### ESTRUTURA OBRIGATÓRIA
1. **O Cenário (Ambientação):** Onde? Quando? Como era o lugar? Que cheiros, sons, cores?
2. **O Conflito (A Crise):** Qual o problema? Que tensão estava no ar?
3. **O Clímax (Intervenção Divina):** O momento decisivo, a ação de Deus
4. **A Resolução:** O desfecho e suas consequências emocionais

**REGRAS:** Use prosa fluida e cinematográfica. Envolva os 5 sentidos. Crie tensão e emoção.
""",
                                    "💡 Devocional-Prático": """
# ATIVAÇÃO DE PERSONA: DEVOCIONAL-PRÁTICO (O Mentor)

**FOCO:** Vida diária, segunda-feira de manhã, consolo, resolução de problemas (ansiedade, medo, família).

### TOM E VOZ
* **Empático, próximo, encorajador, prático.**
* Simplifique a teologia para torná-la "usável".
* Foque no "como fazer" e no conforto genuíno.

### ESTRUTURA OBRIGATÓRIA
1. **O Problema Humano:** Situação real da vida (medo, ansiedade, solidão, etc.)
2. **A Perspectiva Divina:** O que Deus diz sobre isso no texto
3. **3 Passos Práticos para Hoje:** Ações concretas que podem ser aplicadas HOJE

**REGRAS:** Seja simples e direto. Use exemplos cotidianos. Ofereça AÇÕES práticas, não apenas teoria.
""",
                                    "✝️ Cristocêntrico-Tipológico": """
# ATIVAÇÃO DE PERSONA: CRISTOCÊNTRICO-TIPOLÓGICO (O Revelador)

**FOCO:** Jesus em todo o texto, sombras, tipos e antítipos, a Cruz, a Graça, a Redenção.

### TOM E VOZ
* **Admirado, adorador, focado na Redenção.**
* Conecte qualquer passagem (especialmente AT) à obra de Cristo.
* Mostre como personagens falham onde Cristo vence.

### ESTRUTURA OBRIGATÓRIA
1. **A Sombra (O Texto Antigo):** O evento/personagem do AT ou Evangelho
2. **A Luz (A Revelação em Cristo):** Como Jesus cumpre, supera ou reverte isso
3. **A Nossa Posição na Graça:** O que isso significa para nós em Cristo hoje

**REGRAS:** Sempre conecte à Cruz. Evite alegorizações forçadas, mas busque tipos genuínos. Exalte Cristo.
""",
                                    "🔥 Profético-Confrontador": """
# ATIVAÇÃO DE PERSONA: PROFÉTICO-CONFRONTADOR (O Atalaia)

**FOCO:** Arrependimento, santidade, despertar, alinhamento, justiça divina, urgência.

### TOM E VOZ
* **Urgente, firme, apaixonado, direto.**
* Confronte a mornidão e o pecado sem passar a mão na cabeça.
* Use linguagem de URGÊNCIA e chamado à santidade.

### ESTRUTURA OBRIGATÓRIA
1. **A Denúncia do Estado Atual:** O que está errado na igreja/sociedade hoje
2. **O Padrão de Deus:** O que Deus espera segundo o texto
3. **O Chamado ao Arrependimento:** Convocação à mudança radical e imediata

**REGRAS:** Seja direto mas amoroso. Use o texto como autoridade. Chame ao arrependimento genuíno.
""",
                                    "🛡️ Apologético-Filosófico": """
# ATIVAÇÃO DE PERSONA: APOLOGÉTICO-FILOSÓFICO (O Defensor)

**FOCO:** Lógica, razão, defesa da fé, resposta aos céticos, "porquês", argumentação.

### TOM E VOZ
* **Racional, lógico, persuasivo, intelectual.**
* Use argumentos lógicos para defender a verdade bíblica.
* Responda objeções modernas e ideologias seculares.

### ESTRUTURA OBRIGATÓRIA
1. **O Questionamento do Mundo:** Objeção comum ou dúvida filosófica
2. **A Lógica da Escritura:** Resposta racional baseada no texto
3. **A Conclusão Racional:** Por que a perspectiva bíblica é a mais coerente

**REGRAS:** Use lógica sólida. Antecipe objeções. Seja persuasivo sem ser arrogante.
"""
                                }
                                
                                # Identificar qual estilo foi selecionado
                                selected_style_key = None
                                for key in style_prompts.keys():
                                    if key in sermon_style:
                                        selected_style_key = key
                                        break
                                
                                # Montar o prompt final
                                if selected_style_key and selected_style_key in style_prompts:
                                    style_instructions = style_prompts[selected_style_key]
                                    request = (
                                        "# GERADOR MESTRE DE SERMÕES MULTIDIMENSIONAIS\n\n"
                                        + "Você é um especialista em Homilética Avançada e Hermenêutica. "
                                        + "Analise o texto bíblico fornecido e gere um sermão completo seguindo ESTRITAMENTE as regras do estilo escolhido.\n\n"
                                        + style_instructions
                                        + f"\n\n### CONTEXTO DO SERMÃO\n"
                                        + f"**Tema:** {tema or 'A ser desenvolvido do texto'}\n"
                                        + f"**Público:** {publico or 'Igreja cristã geral'}\n"
                                        + f"**Escopo:** {scope_info}\n"
                                        + f"**Notas do Pregador:** {base_note if base_note else 'Nenhuma nota adicional'}\n\n"
                                        + "### FORMATO DE SAÍDA OBRIGATÓRIO\n"
                                        + "1. **Título:** Crie um título impactante adequado ao estilo escolhido\n"
                                        + f"2. **Estilo Aplicado:** {selected_style_key}\n"
                                        + "3. **Corpo do Texto:** Desenvolva profundamente usando a ESTRUTURA OBRIGATÓRIA do estilo\n"
                                        + "4. **Frase de Encerramento:** Uma frase final que resuma a essência da mensagem\n\n"
                                        + "⚠️ IMPORTANTE: Cite o TEXTO COMPLETO dos versículos chave, não apenas as referências.\n\n"
                                        + "Agora, gere o sermão seguindo RIGOROSAMENTE o estilo e a estrutura especificados."
                                    )
                                else:
                                    # Fallback para prompt padrão (não deveria acontecer)
                                    request = (
                                        t(trans, "prompts.sermon_request", "Escreva um esboco completo de sermao com titulo, introducao, topicos expositivos, ilustracoes e conclusao.")
                                        + f" {t(trans, 'prompts.sermon_theme', 'Tema:')} {tema or t(trans, 'labels.indefinido', 'Indefinido')}. "
                                        + f"{t(trans, 'prompts.sermon_audience', 'Publico:')} {publico or t(trans, 'labels.generic', 'Generico')}.{scope_info} {base_note}"
                                    )
                                
                                prompt = build_prompt(sermon_text, request, reference=context_description)
                                
                                # Timeout dinâmico baseado no escopo e tamanho do contexto
                                # Calcular baseado no número de livros E tamanho do texto
                                context_size = len(sermon_text)
                                
                                # Base: 180s (3 minutos)
                                # + 60s por livro adicional
                                # + 1s por 100 caracteres de contexto
                                # Mínimo: 240s (4 minutos)
                                # Máximo: 600s (10 minutos)
                                base_timeout = 180
                                books_timeout = len(selected_books) * 60
                                context_timeout = context_size // 100
                                calculated_timeout = base_timeout + books_timeout + context_timeout
                                timeout = max(240, min(calculated_timeout, 600))
                                
                                st.info(f"🔄 Gerando sermão completo ({len(selected_books)} livro(s), timeout: {timeout}s)... Se necessário, continuarei automaticamente até completar todo o conteúdo (até 5 continuações).")
                                ok, response = query_ollama(selected_model, prompt, max_tokens=2500, timeout=timeout, auto_continue=True, lang_code=lang_code, show_progress=True)
                            
                            if ok:
                                # Salvar no histórico
                                if "sermon_history" not in st.session_state:
                                    st.session_state.sermon_history = []
                                sermon_entry = {
                                    "timestamp": time.time(),
                                    "reference": context_description,
                                    "tema": tema or t(trans, "labels.no_theme", "Sem tema"),
                                    "publico": publico or t(trans, "labels.generic", "Genérico"),
                                    "notas": base_note,
                                    "sermon": response,
                                    "version": version,
                                    "model": selected_model,
                                    "scope": scope_option,
                                    "books": selected_books,
                                    "style": sermon_style
                                }
                                st.session_state.sermon_history.insert(0, sermon_entry)
                                auto_save_history("sermon_history", st.session_state.sermon_history)
                                st.success(t(trans, "messages.sermon_saved", "✅ Sermão gerado e salvo no histórico!"))
                                st.info(t(trans, "messages.check_sermon_tab", "📋 Acesse a aba 'Histórico Sermões' para revisar todos os seus sermões."))
                                with st.expander(t(trans, "expanders.sermon_preview", "👁️ Prévia do Sermão"), expanded=True):
                                    st.markdown(response)
                            else:
                                st.error(response)
        
        with sermon_subtabs[1]:
            st.subheader(t(trans, "headers.sermons_history", "📋 Histórico de Sermões"))
            if "sermon_history" not in st.session_state or not st.session_state.sermon_history:
                st.info(t(trans, "messages.no_sermons_yet", "🎤 Nenhum sermão gerado ainda. Use a aba 'Gerador Sermoes' para criar seu primeiro sermão!"))
            else:
                # Filtros e ordenação
                col1, col2 = st.columns([2, 1])
                with col1:
                    search_term_sermon = st.text_input(t(trans, "labels.search_sermons", "🔍 Buscar sermões"), placeholder=t(trans, "labels.search_sermons_placeholder", "Tema, referência, conteúdo..."), key="search_sermon_hist")
                with col2:
                    sort_order_sermon = st.selectbox(t(trans, "labels.order_by", "📅 Ordenar por"), [t(trans, "labels.most_recent_plural", "Mais recentes"), t(trans, "labels.oldest_plural", "Mais antigos")], key="sort_sermon_hist")
                
                # Filtrar e ordenar
                filtered_sermons = st.session_state.sermon_history
                if search_term_sermon:
                    search_lower = search_term_sermon.lower()
                    filtered_sermons = [
                        s for s in filtered_sermons
                        if search_lower in s.get("tema", "").lower()
                        or search_lower in s.get("reference", "").lower()
                        or search_lower in s.get("sermon", "").lower()
                    ]
                
                if sort_order_sermon == t(trans, "labels.oldest_plural", "Mais antigos"):
                    filtered_sermons = list(reversed(filtered_sermons))
                
                st.caption(t(trans, "captions.sermons_found", "📄 {count} sermões encontrados").format(count=len(filtered_sermons)))
                
                # Exibir sermões (código completo será adicionado depois)
                for idx, sermon in enumerate(filtered_sermons):
                    timestamp_str = time.strftime(t(trans, 'formatting.timestamp_format', '%d/%m/%Y às %H:%M'), time.localtime(sermon["timestamp"]))
                    with st.expander(
                        f"🎤 {sermon.get('tema', t(trans, 'labels.no_theme', 'Sem tema'))} - {sermon.get('reference', '')} ({timestamp_str})",
                        expanded=False
                    ):
                        st.markdown(f"**{t(trans, 'labels.theme_colon', 'Tema:')}** {sermon.get('tema', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.audience_colon', 'Público:')}** {sermon.get('publico', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.version_colon', 'Versão:')}** {sermon.get('version', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.model_colon', 'Modelo:')}** {sermon.get('model', 'N/A')}")
                        
                        # Exibir estilo se disponível
                        if sermon.get('style'):
                            st.markdown(f"**{t(trans, 'labels.style_colon', 'Estilo:')}** {sermon.get('style', 'N/A')}")
                        
                        if sermon.get('notas'):
                            st.markdown(f"**{t(trans, 'labels.notes_colon', 'Notas:')}** {sermon['notas']}")
                        
                        st.markdown("---")
                        st.markdown(sermon["sermon"])
                        st.markdown("---")
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button(t(trans, "buttons.copy", "📋 Copiar"), key=f"sermon_copy_{idx}", use_container_width=True):
                                st.code(sermon["sermon"], language=None)
                                st.success(t(trans, "messages.ready_to_copy", "Texto pronto para copiar!"))
                        with col_b:
                            if st.button(t(trans, "buttons.generate_pdf", "📄 Gerar PDF"), key=f"sermon_pdf_{idx}", use_container_width=True):
                                pdf_buffer = generate_sermon_pdf(sermon, trans)
                                pdf_filename = f"sermao_{sermon.get('tema', 'sem_tema').replace(' ', '_')}_{int(sermon['timestamp'])}.pdf"
                                b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" style="display:inline-block;padding:0.5rem 1rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:bold;">📥 Baixar PDF</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success("✅ PDF gerado!")
                        with col_c:
                            if st.button(t(trans, "buttons.delete", "🗑️ Excluir"), key=f"sermon_del_{idx}", use_container_width=True):
                                st.session_state.sermon_history.remove(sermon)
                                auto_save_history("sermon_history", st.session_state.sermon_history)
                                st.toast(t(trans, "messages.sermon_deleted", "✅ Sermão excluído!"), icon="✅")

    with tabs[2]:
        # Criar subtabs dentro de Devocional & Meditação
        devotional_subtabs = st.tabs([
            t(trans, "menu.devotional", "🧘 Devocional"),
            t(trans, "menu.devotional_hist", "🕊️ Histórico")
        ])
        
        with devotional_subtabs[0]:
            st.subheader(t(trans, "headers.devotional_meditation", "Devocional e Meditacao"))
            if not data_available or not version:
                st.info(t(trans, "messages.import_verse_devotional", "Carregue um versiculo para montar o devocional."))
            else:
                # Seção de filtros de escopo
                st.markdown(f"#### {t(trans, 'headers.devotional_scope', '📚 Escopo do Devocional')}")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    dev_scope_option = st.radio(
                        t(trans, "labels.devotional_scope_prompt", "Selecione o escopo para geração do devocional:"),
                        [
                            t(trans, "labels.sermon_scope_specific_book", "📖 Livro Específico"),
                            t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"),
                            t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"),
                            t(trans, "labels.sermon_scope_whole_bible", "🌍 Toda a Bíblia")
                        ],
                        key="devotional_scope_option"
                    )
                
                with col2:
                    dev_use_multiple_books = st.checkbox(
                        t(trans, "labels.select_multiple_books", "🔖 Selecionar múltiplos livros"),
                        help=t(trans, "labels.select_multiple_books_help", "Marque para selecionar livros específicos manualmente"),
                        key="devotional_use_multiple"
                    )
                
                # Determinar quais livros usar
                dev_selected_books = []
                dev_context_description = ""
                
                if dev_scope_option == t(trans, "labels.sermon_scope_specific_book", "📖 Livro Específico"):
                    # Modo original - um livro específico
                    book_key, book_label, chapter, _, dev_text, verse_options = render_reference_selectors(
                        t(trans, "labels.devotional_book_label", "Devocional"), bible_data, version, "devotional", trans=trans, include_verse_selector=False
                    )
                    
                    # Adicionar seleção de múltiplos versículos
                    if book_key and chapter:
                        version_books = bible_data.get("versions", {}).get(version, {}).get("books", {})
                        book_entry = version_books.get(book_key)
                        if book_entry:
                            chapter_data = book_entry.get("chapters", {}).get(chapter, {})
                            verses_map = chapter_data.get("verses", {})
                            
                            verse_input_key = "devotional_verse_selection"
                            chapter_state_key = "devotional_selected_chapter"
                            if st.session_state.get(chapter_state_key) != chapter:
                                st.session_state[chapter_state_key] = chapter
                                st.session_state[verse_input_key] = ""
                            st.session_state.setdefault(verse_input_key, "")
                            
                            verse_selection = st.text_input(
                                t(trans, "labels.verses", "Versículos (ex: 1, 1-5, 10-15)"),
                                value=st.session_state[verse_input_key],
                                key=verse_input_key,
                                help=t(trans, "labels.verses_help", "Informe versículos específicos, intervalos, ou deixe em branco para o capítulo inteiro."),
                            )
                            
                            cleaned_selection = verse_selection.strip()
                            selected_verses = parse_verse_selection(cleaned_selection, verse_options) if cleaned_selection else []
                            
                            if cleaned_selection and not selected_verses:
                                st.warning(t(trans, "messages.invalid_verse_syntax", "Nenhum versículo correspondente foi encontrado. Revise a sintaxe."))
                            
                            # Determinar quais versículos usar
                            verse_keys_for_context = selected_verses if selected_verses else sorted(verses_map.keys(), key=int)
                            verse_label = summarize_verses(selected_verses) if selected_verses else t(trans, "labels.full_chapter", "Capítulo inteiro")
                            dev_text = build_context_text(verses_map, verse_keys_for_context)
                            
                            dev_selected_books = [book_key]
                            dev_context_description = f"{t(trans, 'labels.book_colon', 'Livro:')} {book_label}, {t(trans, 'labels.chapter_colon', 'Capítulo')} {chapter}, {t(trans, 'labels.verse_colon', 'Versículo(s):')} {verse_label}"
                    
                elif dev_use_multiple_books:
                    # Seleção manual de múltiplos livros
                    if dev_scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        dev_available_books = get_books_by_testament(bible_data, version, "VT")
                    elif dev_scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        dev_available_books = get_books_by_testament(bible_data, version, "NT")
                    else:  # Toda a Bíblia
                        dev_available_books = get_books_by_testament(bible_data, version, "ALL")
                    
                    dev_book_options = {abbr: entry.get("name", abbr) for abbr, entry in dev_available_books}
                    dev_selected_books = st.multiselect(
                        t(trans, "labels.select_books_for_devotional", "Selecione os livros para o devocional:"),
                        options=list(dev_book_options.keys()),
                        format_func=lambda x: dev_book_options[x],
                        default=[dev_available_books[0][0]] if dev_available_books else [],
                        key="devotional_selected_books"
                    )
                    dev_context_description = f"{len(dev_selected_books)} {t(trans, 'labels.selected_books_count', 'livro(s) selecionado(s):')} {', '.join([dev_book_options[b] for b in dev_selected_books[:3]])}{'...' if len(dev_selected_books) > 3 else ''}"
                    # Limitar a 6 livros e 1 versículo cada para evitar timeout
                    limited_books = dev_selected_books[:6] if len(dev_selected_books) > 6 else dev_selected_books
                    dev_text = collect_verses_from_books(bible_data, version, limited_books, max_verses=1, randomize=True) if dev_selected_books else ""
                    
                else:
                    # Usar todos os livros do escopo selecionado
                    if dev_scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        dev_available_books = get_books_by_testament(bible_data, version, "VT")
                        dev_context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_old_testament', 'Todo o Velho Testamento')}"
                    elif dev_scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        dev_available_books = get_books_by_testament(bible_data, version, "NT")
                        dev_context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_new_testament', 'Todo o Novo Testamento')}"
                    else:  # Toda a Bíblia
                        dev_available_books = get_books_by_testament(bible_data, version, "ALL")
                        dev_context_description = f"{t(trans, 'labels.scope_prefix', 'Escopo:')} {t(trans, 'labels.whole_bible', 'Toda a Bíblia')}"
                    
                    # ULTRA-REDUZIDO: 4 livros × 1 versículo = 4 versículos totais
                    all_book_keys = [abbr for abbr, _ in dev_available_books]
                    # Selecionar apenas 4 livros aleatórios para mínima carga
                    dev_selected_books = random.sample(all_book_keys, min(4, len(all_book_keys)))
                    dev_text = collect_verses_from_books(bible_data, version, dev_selected_books, max_verses=1, randomize=True)
                
                st.info(f"📍 {dev_context_description}")
                
                sentimento = st.text_input(t(trans, "labels.theme_or_feeling", "Tema ou sentimento a meditar"), value="Gratidao", key="devotional_sentiment")
                
                if not dev_text:
                    st.warning(t(trans, "messages.select_verse_meditation", "Selecione um versiculo ou escopo para ancorar a meditacao."))
                else:
                    if st.button(t(trans, "buttons.generate_devotional", "✨ Gerar Devocional"), type="primary", use_container_width=True):
                        if not ollama_online:
                            st.error(t(trans, "messages.ollama_offline_retry", "Ollama esta offline. Ligue o servidor e tente novamente."))
                        else:
                            with st.spinner(t(trans, "messages.generating_devotional", "🕊️ Criando devocional...")):
                                # Prompt SIMPLIFICADO para processar mais rápido
                                request = (
                                    f"Crie um devocional breve sobre '{sentimento}' usando os versículos fornecidos.\n\n"
                                    f"Estrutura:\n"
                                    f"- Leitura: [cite os versículos]\n"
                                    f"- Reflexão: [breve reflexão sobre {sentimento}]\n"
                                    f"- Oração: [oração curta em português correto, terminando com 'Amém']\n\n"
                                    f"Use gramática correta em português."
                                )
                                prompt = build_prompt(dev_text, request, reference=dev_context_description)
                                
                                # Timeout dinâmico baseado no escopo e tamanho do contexto
                                context_size = len(dev_text)
                                
                                # Base: 120s (2 minutos)
                                # + 45s por livro adicional
                                # + 1s por 150 caracteres de contexto
                                # Mínimo: 180s (3 minutos)
                                # Máximo: 420s (7 minutos)
                                base_timeout = 120
                                books_timeout = len(dev_selected_books) * 45
                                context_timeout = context_size // 150
                                calculated_timeout = base_timeout + books_timeout + context_timeout
                                timeout = max(180, min(calculated_timeout, 420))
                                
                                st.info(f"🔄 Gerando devocional ({len(dev_selected_books)} livro(s), timeout: {timeout}s)...")
                                ok, devotional_response = query_ollama(selected_model, prompt, temperature=0.18, max_tokens=1200, timeout=timeout, auto_continue=True, lang_code=lang_code)
                            
                            if ok:
                                # Salvar no histórico
                                if "devotional_history" not in st.session_state:
                                    st.session_state.devotional_history = []
                                dev_entry = {
                                    "timestamp": time.time(),
                                    "reference": dev_context_description,
                                    "sentimento": sentimento,
                                    "text": dev_text,
                                    "devotional": devotional_response,
                                    "version": version,
                                    "model": selected_model,
                                    "scope": dev_scope_option,
                                    "books": dev_selected_books
                                }
                                st.session_state.devotional_history.insert(0, dev_entry)
                                auto_save_history("devotional_history", st.session_state.devotional_history)
                                st.success(t(trans, "messages.devotional_saved", "✅ Devocional gerado e salvo no histórico!"))
                                st.info(t(trans, "messages.check_devotional_tab", "🕊️ Acesse a aba 'Histórico Devocionais' para revisar suas meditações."))
                                with st.expander(t(trans, "expanders.devotional_preview", "👁️ Prévia do Devocional"), expanded=True):
                                    st.markdown(devotional_response)
                            else:
                                st.error(devotional_response)
        
        with devotional_subtabs[1]:
            st.subheader(t(trans, "headers.devotional_history", "🕊️ Histórico de Devocionais"))
            if "devotional_history" not in st.session_state or not st.session_state.devotional_history:
                st.info(t(trans, "messages.no_devotionals_yet", "🧘 Nenhum devocional gerado ainda. Use a aba 'Devocional & Meditação' para criar sua primeira meditação!"))
            else:
                # Filtros
                col1, col2 = st.columns([2, 1])
                with col1:
                    search_dev = st.text_input(t(trans, "labels.search_devotionals", "🔍 Buscar devocionais"), placeholder=t(trans, "labels.search_placeholder", "Sentimento, referência..."), key="search_dev_hist")
                with col2:
                    sort_dev = st.selectbox(t(trans, "labels.order_by", "📅 Ordenar"), [t(trans, "labels.most_recent_plural", "Mais recentes"), t(trans, "labels.oldest_plural", "Mais antigos")], key="sort_dev_hist")
                
                filtered_devs = st.session_state.devotional_history
                if search_dev:
                    search_lower = search_dev.lower()
                    filtered_devs = [
                        d for d in filtered_devs
                        if search_lower in d.get("sentimento", "").lower()
                        or search_lower in d.get("reference", "").lower()
                        or search_lower in d.get("devotional", "").lower()
                    ]
                
                if sort_dev == t(trans, "labels.oldest_plural", "Mais antigos"):
                    filtered_devs = list(reversed(filtered_devs))
                
                st.caption(t(trans, "captions.devotionals_found", "🕊️ {count} devocionais encontrados").format(count=len(filtered_devs)))
                
                for idx, dev in enumerate(filtered_devs):
                    timestamp_str = time.strftime(t(trans, 'formatting.timestamp_format', '%d/%m/%Y às %H:%M'), time.localtime(dev["timestamp"]))
                    with st.expander(
                        f"🧘 {dev.get('sentimento', 'Meditação')} - {dev.get('reference', '')} ({timestamp_str})",
                        expanded=False
                    ):
                        st.markdown(f"**{t(trans, 'labels.feeling_colon', 'Sentimento:')}** {dev.get('sentimento', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.version_colon', 'Versão:')}** {dev.get('version', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.model_colon', 'Modelo:')}** {dev.get('model', 'N/A')}")
                        st.markdown("---")
                        st.markdown(dev["devotional"])
                        st.markdown("---")
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button(t(trans, "buttons.copy", "📋 Copiar"), key=f"dev_copy_{idx}", use_container_width=True):
                                st.code(dev["devotional"], language=None)
                                st.success(t(trans, "messages.ready_to_copy", "Texto pronto!"))
                        with col_b:
                            if st.button(t(trans, "buttons.generate_pdf", "📄 PDF"), key=f"dev_pdf_{idx}", use_container_width=True):
                                pdf_buffer = generate_devotional_pdf(dev, trans)
                                pdf_filename = f"devocional_{dev.get('sentimento', 'meditacao').replace(' ', '_')}_{int(dev['timestamp'])}.pdf"
                                b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" style="display:inline-block;padding:0.5rem 1rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:bold;">📥 Baixar</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success("✅ PDF gerado!")
                        with col_c:
                            if st.button(t(trans, "buttons.delete", "🗑️"), key=f"dev_del_{idx}", use_container_width=True):
                                st.session_state.devotional_history.remove(dev)
                                auto_save_history("devotional_history", st.session_state.devotional_history)
                                st.toast(t(trans, "messages.devotional_deleted", "✅ Devocional excluído!"), icon="✅")

    with tabs[3]:
        # Criar subtabs dentro de Chat Teológico
        chat_subtabs = st.tabs([
            t(trans, "menu.chat", "💬 Chat"),
            t(trans, "menu.chat_hist", "💭 Histórico")
        ])
        
        with chat_subtabs[0]:
            st.subheader(t(trans, "headers.theological_chat", "Chat Teologico"))
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            if not data_available or not version:
                st.info(t(trans, "messages.import_version_chat", "Importe uma versao para poder dialogar com o chat teologico."))
            else:
                # Seção de filtros de escopo
                st.markdown(f"#### {t(trans, 'headers.chat_scope', '📚 Escopo da Consulta')}")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    chat_scope_option = st.radio(
                        t(trans, "labels.chat_scope_prompt", "Selecione o escopo para a consulta bíblica:"),
                        [
                            t(trans, "labels.chat_scope_specific_verse", "📖 Versículo Específico"),
                            t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"),
                            t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"),
                            t(trans, "labels.sermon_scope_whole_bible", "🌍 Toda a Bíblia")
                        ],
                        key="chat_scope_option"
                    )
                
                with col2:
                    use_multiple_books_chat = st.checkbox(
                        t(trans, "labels.use_multiple_books", "📚 Múltiplos livros"),
                        value=False,
                        key="chat_use_multiple_books",
                        help=t(trans, "labels.multiple_books_help", "Use versículos de vários livros como base")
                    )
                
                # Determinar quais livros usar
                selected_books_chat = []
                context_description_chat = ""
                chat_reference = ""
                
                if chat_scope_option == t(trans, "labels.chat_scope_specific_verse", "📖 Versículo Específico"):
                    # Modo original: selecionar livro, capítulo e versículos específicos
                    chat_book_key, chat_book_label, chat_chapter, _, chat_text, verse_options = render_reference_selectors(
                        "Chat", bible_data, version, "chat", trans=trans, include_verse_selector=False
                    )
                    
                    # Adicionar seleção de múltiplos versículos
                    if chat_book_key and chat_chapter:
                        version_books = bible_data.get("versions", {}).get(version, {}).get("books", {})
                        book_entry = version_books.get(chat_book_key)
                        if book_entry:
                            chapter_data = book_entry.get("chapters", {}).get(chat_chapter, {})
                            verses_map = chapter_data.get("verses", {})
                            
                            verse_input_key = "chat_verse_selection"
                            chapter_state_key = "chat_selected_chapter"
                            if st.session_state.get(chapter_state_key) != chat_chapter:
                                st.session_state[chapter_state_key] = chat_chapter
                                st.session_state[verse_input_key] = ""
                            st.session_state.setdefault(verse_input_key, "")
                            
                            verse_selection = st.text_input(
                                t(trans, "labels.verses", "Versículos (ex: 1, 1-5, 10-15)"),
                                value=st.session_state[verse_input_key],
                                key=verse_input_key,
                                help=t(trans, "labels.verses_help", "Informe versículos específicos, intervalos, ou deixe em branco para o capítulo inteiro."),
                            )
                            
                            cleaned_selection = verse_selection.strip()
                            selected_verses = parse_verse_selection(cleaned_selection, verse_options) if cleaned_selection else []
                            
                            if cleaned_selection and not selected_verses:
                                st.warning(t(trans, "messages.invalid_verse_syntax", "Nenhum versículo correspondente foi encontrado. Revise a sintaxe."))
                            
                            # Determinar quais versículos usar
                            verse_keys_for_context = selected_verses if selected_verses else sorted(verses_map.keys(), key=int)
                            verse_label = summarize_verses(selected_verses) if selected_verses else t(trans, "labels.full_chapter", "Capítulo inteiro")
                            chat_text = build_context_text(verses_map, verse_keys_for_context)
                            context_description_chat = chat_text or ""
                            chat_reference = f"{chat_book_label} {chat_chapter}:{verse_label}" if chat_book_label else ""
                    
                elif use_multiple_books_chat:
                    # Múltiplos livros no testamento/bíblia selecionado
                    if chat_scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        testament_books = get_books_by_testament(bible_data, version, "VT")
                        context_description_chat = t(trans, "labels.old_testament", "Velho Testamento")
                    elif chat_scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        testament_books = get_books_by_testament(bible_data, version, "NT")
                        context_description_chat = t(trans, "labels.new_testament", "Novo Testamento")
                    else:  # Toda a Bíblia
                        testament_books = get_books_for_version(bible_data, version)
                        context_description_chat = t(trans, "labels.whole_bible", "Toda a Bíblia")
                    
                    book_names = [book[0] for book in testament_books]
                    selected_books_chat = st.multiselect(
                        t(trans, "labels.select_books", "📚 Selecione os livros"),
                        book_names,
                        default=book_names[:3] if len(book_names) >= 3 else book_names,
                        key="chat_selected_books"
                    )
                    chat_reference = f"{context_description_chat} ({len(selected_books_chat)} livros)"
                    
                else:
                    # Um testamento/bíblia inteiro (primeiros versículos de cada livro)
                    if chat_scope_option == t(trans, "labels.sermon_scope_old_testament", "📜 Velho Testamento"):
                        testament_books = get_books_by_testament(bible_data, version, "VT")
                        context_description_chat = t(trans, "labels.old_testament", "Velho Testamento")
                    elif chat_scope_option == t(trans, "labels.sermon_scope_new_testament", "✝️ Novo Testamento"):
                        testament_books = get_books_by_testament(bible_data, version, "NT")
                        context_description_chat = t(trans, "labels.new_testament", "Novo Testamento")
                    else:  # Toda a Bíblia
                        testament_books = get_books_for_version(bible_data, version)
                        context_description_chat = t(trans, "labels.whole_bible", "Toda a Bíblia")
                    
                    selected_books_chat = [book[0] for book in testament_books]
                    chat_reference = context_description_chat
                
                st.markdown("---")
                
                user_message = st.text_area(t(trans, "labels.your_question", "Digite sua dúvida bíblica"), height=120)
                
                if st.button(t(trans, "buttons.send_question", "✨ Enviar Pergunta"), type="primary", use_container_width=True):
                    if not user_message.strip():
                        st.warning(t(trans, "messages.write_question_first", "Escreva a pergunta antes de enviar."))
                    elif not ollama_online:
                        st.error(t(trans, "messages.ollama_offline_start", "Ollama esta offline. Por favor inicie o servidor."))
                    else:
                        with st.spinner(t(trans, "messages.generating_answer", "💬 Processando sua pergunta...")):
                            # Coletar contexto baseado no escopo
                            if chat_scope_option == t(trans, "labels.chat_scope_specific_verse", "📖 Versículo Específico"):
                                chat_context = context_description_chat
                            else:
                                # Limitar quantidade de dados para evitar timeout
                                # Para escopos amplos, usar menos versículos por livro e menos livros
                                if use_multiple_books_chat:
                                    # Múltiplos livros selecionados: 1 versículo por livro, máximo 6 livros, com randomização
                                    max_books = min(len(selected_books_chat), 6)
                                    chat_context = collect_verses_from_books(bible_data, version, selected_books_chat[:max_books], max_verses=1, randomize=True)
                                else:
                                    # Testamento/Bíblia inteira: 1 versículo de 4 livros ALEATÓRIOS (ultra-reduzido)
                                    all_chat_books = selected_books_chat if isinstance(selected_books_chat, list) else []
                                    if all_chat_books:
                                        sampled_books = random.sample(all_chat_books, min(4, len(all_chat_books)))
                                        chat_context = collect_verses_from_books(bible_data, version, sampled_books, max_verses=1, randomize=True)
                                    else:
                                        chat_context = ""
                            
                            if not chat_context:
                                st.warning(t(trans, "messages.no_context_found", "Nenhum contexto bíblico encontrado para o escopo selecionado."))
                            else:
                                prompt = build_prompt(
                                    chat_context,
                                    f"O usuario pergunta o seguinte: {user_message.strip()}. Responda sempre com base no texto e seja didatico.",
                                    reference=chat_reference
                                )
                                
                                # Timeout dinâmico baseado no escopo e tamanho do contexto
                                context_size = len(chat_context)
                                
                                # Base: 120s (2 minutos)
                                # + 40s por livro adicional
                                # + 1s por 200 caracteres de contexto
                                # Mínimo: 180s (3 minutos)
                                # Máximo: 360s (6 minutos)
                                base_timeout = 120
                                books_timeout = len(selected_books_chat) * 40 if selected_books_chat else 0
                                context_timeout = context_size // 200
                                calculated_timeout = base_timeout + books_timeout + context_timeout
                                timeout = max(180, min(calculated_timeout, 360))
                                
                                ok, answer = query_ollama(selected_model, prompt, timeout=timeout, max_tokens=1200, lang_code=lang_code)
                                
                                if ok:
                                    # Salvar no histórico de chat
                                    if "chat_conversation_history" not in st.session_state:
                                        st.session_state.chat_conversation_history = []
                                    chat_entry = {
                                        "timestamp": time.time(),
                                        "reference": chat_reference,
                                        "scope": chat_scope_option,
                                        "text": chat_context[:500],  # Primeiros 500 caracteres
                                        "question": user_message.strip(),
                                        "answer": answer,
                                        "version": version,
                                        "model": selected_model
                                    }
                                    st.session_state.chat_conversation_history.insert(0, chat_entry)
                                    auto_save_history("chat_history", st.session_state.chat_conversation_history)
                                    st.session_state.chat_history.append((user_message, answer))
                                    st.success(t(trans, "messages.answer_saved", "✅ Resposta gerada e salva no histórico!"))
                                    st.info(t(trans, "messages.check_chat_tab", "💭 Acesse a aba 'Histórico Chat' para revisar suas conversas."))
                                else:
                                    st.error(answer)
                for question, answer in st.session_state.chat_history:
                    with st.container():
                        st.markdown(f"**{t(trans, 'formatting.question_label', '💬 Pergunta:')}** {question}")
                        st.markdown(f"**{t(trans, 'formatting.answer_label', '🤖 Resposta:')}** {answer}")
                        st.divider()
        
        with chat_subtabs[1]:
            st.subheader(t(trans, "headers.chat_history", "💭 Histórico de Conversas"))
            if "chat_conversation_history" not in st.session_state or not st.session_state.chat_conversation_history:
                st.info(t(trans, "messages.no_chats_yet", "💬 Nenhuma conversa salva ainda. Use a aba 'Chat Teológico' para começar!"))
            else:
                # Filtros
                col1, col2 = st.columns([2, 1])
                with col1:
                    search_chat = st.text_input(t(trans, "labels.search_chats", "🔍 Buscar conversas"), placeholder=t(trans, "labels.search_placeholder", "Pergunta, resposta..."), key="search_chat_hist")
                with col2:
                    sort_chat = st.selectbox(t(trans, "labels.order_by", "📅 Ordenar"), [t(trans, "labels.most_recent_plural", "Mais recentes"), t(trans, "labels.oldest_plural", "Mais antigos")], key="sort_chat_hist")
                
                filtered_chats = st.session_state.chat_conversation_history
                if search_chat:
                    search_lower = search_chat.lower()
                    filtered_chats = [
                        c for c in filtered_chats
                        if search_lower in c.get("question", "").lower()
                        or search_lower in c.get("answer", "").lower()
                        or search_lower in c.get("reference", "").lower()
                    ]
                
                if sort_chat == t(trans, "labels.oldest_plural", "Mais antigos"):
                    filtered_chats = list(reversed(filtered_chats))
                
                st.caption(t(trans, "captions.chats_found", "💭 {count} conversas encontradas").format(count=len(filtered_chats)))
                
                for idx, chat in enumerate(filtered_chats):
                    timestamp_str = time.strftime(t(trans, 'formatting.timestamp_format', '%d/%m/%Y às %H:%M'), time.localtime(chat["timestamp"]))
                    with st.expander(
                        f"💬 {chat.get('reference', 'Chat')} ({timestamp_str})",
                        expanded=False
                    ):
                        st.markdown(f"**{t(trans, 'labels.reference_colon', 'Referência:')}** {chat.get('reference', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.version_colon', 'Versão:')}** {chat.get('version', 'N/A')}")
                        st.markdown(f"**{t(trans, 'labels.model_colon', 'Modelo:')}** {chat.get('model', 'N/A')}")
                        st.markdown("---")
                        st.markdown(f"**{t(trans, 'formatting.question_label', '❓ Pergunta:')}**\n{chat['question']}")
                        st.markdown(f"**{t(trans, 'formatting.answer_label', '💡 Resposta:')}**\n{chat['answer']}")
                        st.markdown("---")
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button(t(trans, "buttons.copy", "📋 Copiar"), key=f"chat_copy_{idx}", use_container_width=True):
                                full_text = f"Pergunta: {chat['question']}\n\nResposta: {chat['answer']}"
                                st.code(full_text, language=None)
                                st.success(t(trans, "messages.ready_to_copy", "Pronto!"))
                        with col_b:
                            if st.button(t(trans, "buttons.generate_pdf", "📄 PDF"), key=f"chat_pdf_{idx}", use_container_width=True):
                                pdf_buffer = generate_chat_pdf(chat, trans)
                                pdf_filename = f"chat_teologico_{int(chat['timestamp'])}.pdf"
                                b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" style="display:inline-block;padding:0.5rem 1rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:bold;">📥 Baixar</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success("✅ PDF gerado!")
                        with col_c:
                            if st.button(t(trans, "buttons.delete", "🗑️"), key=f"chat_del_{idx}", use_container_width=True):
                                st.session_state.chat_conversation_history.remove(chat)
                                auto_save_history("chat_history", st.session_state.chat_conversation_history)
                                st.toast(t(trans, "messages.chat_deleted", "✅ Conversa excluída!"), icon="✅")

    with tabs[4]:
        # Nova aba: Gerar Perguntas
        st.subheader(t(trans, "headers.questions_generator", "❓ Gerador de Perguntas Bíblicas"))
        
        if not data_available or not version:
            st.info(t(trans, "messages.no_data", "Importe uma versão bíblica para começar a usar o gerador de perguntas."))
        else:
            # Criar subtabs para geração e histórico
            questions_subtabs = st.tabs([
                t(trans, "menu.generate_questions", "❓ Gerar Perguntas"),
                t(trans, "menu.questions_history", "📚 Histórico de Perguntas")
            ])
            
            with questions_subtabs[0]:
                st.markdown(t(trans, "captions.questions_description", "Gere perguntas sobre curiosidades e conhecimentos bíblicos de um livro específico, múltiplos livros ou da Bíblia toda."))
                
                # Seleção de escopo
                scope_options = [
                    t(trans, "labels.specific_book", "Livro Específico"),
                    t(trans, "labels.multiple_books", "Múltiplos Livros"),
                    t(trans, "labels.entire_bible", "Bíblia Toda")
                ]
                scope_selection = st.radio(
                    t(trans, "labels.scope", "Escopo"),
                    scope_options,
                    key="questions_scope",
                    horizontal=True
                )
                
                st.divider()
                
                # Variáveis para armazenar seleção
                selected_book_name = None
                selected_book_label = None
                context_text = ""
                reference = ""
                
                if scope_selection == scope_options[0]:  # Livro específico
                    q_book_key, q_book_label, q_chapter, _, q_text, q_options = render_reference_selectors(
                        "", bible_data, version, "questions", trans=trans, include_verse_selector=False
                    )
                    
                    if q_book_key and q_book_label:
                        selected_book_name = q_book_key
                        selected_book_label = q_book_label
                        reference = q_book_label
                        
                        # Coletar texto do livro inteiro (até 10 versículos aleatórios para contexto)
                        version_books = bible_data.get("versions", {}).get(version, {}).get("books", {})
                        book_entry = version_books.get(q_book_key)
                        if book_entry:
                            context_text = collect_verses_from_books(
                                bible_data, version, [q_book_key], 
                                max_verses=10, randomize=True
                            )
                        
                        st.info(f"📖 **{t(trans, 'labels.selected_book_colon', 'Livro selecionado:')}** {q_book_label}")
                
                elif scope_selection == scope_options[1]:  # Múltiplos livros
                    all_books = get_books_for_version(bible_data, version)
                    if all_books:
                        book_names = [book[0] for book in all_books]
                        
                        # Multiselect para escolher múltiplos livros
                        selected_books = st.multiselect(
                            t(trans, "labels.select_books", "Selecione os livros"),
                            options=book_names,
                            default=None,
                            key="questions_multiple_books",
                            help=t(trans, "labels.select_books_help", "Escolha 2 ou mais livros para gerar perguntas")
                        )
                        
                        if selected_books:
                            if len(selected_books) < 2:
                                st.warning(t(trans, "messages.select_at_least_two_books", "⚠️ Selecione pelo menos 2 livros para continuar."))
                            else:
                                reference = ", ".join(selected_books)
                                st.info(f"📚 **{t(trans, 'labels.selected_books_colon', 'Livros selecionados:')}** {reference}")
                                
                                # Coletar versículos dos livros selecionados (8 versículos por livro)
                                context_text = collect_verses_from_books(
                                    bible_data, version, selected_books,
                                    max_verses=8, randomize=True
                                )
                        else:
                            st.info(t(trans, "messages.select_books_to_continue", "📚 Selecione os livros para continuar"))
                
                else:  # Bíblia toda (scope_options[2])
                    reference = t(trans, "labels.entire_bible", "Bíblia Toda")
                    st.info(f"📚 **{t(trans, 'labels.scope_colon', 'Escopo:')}** {reference}")
                    
                    # Coletar versículos de múltiplos livros (4 livros, 5 versículos cada)
                    all_books = get_books_for_version(bible_data, version)
                    if all_books:
                        book_keys = [book[0] for book in all_books]
                        # Selecionar 4 livros aleatórios
                        selected_books = random.sample(book_keys, min(4, len(book_keys)))
                        context_text = collect_verses_from_books(
                            bible_data, version, selected_books,
                            max_verses=5, randomize=True
                        )
                
                st.divider()
                
                # Configurações de geração
                col1, col2 = st.columns(2)
                
                with col1:
                    # Quantidade de perguntas
                    questions_count = st.number_input(
                        t(trans, "labels.questions_count", "Quantidade de perguntas"),
                        min_value=1,
                        max_value=50,
                        value=10,
                        step=1,
                        key="questions_count",
                        help=t(trans, "labels.questions_count_help", "Número de perguntas a serem geradas")
                    )
                
                with col2:
                    # Modo: com ou sem respostas
                    mode_options = [
                        t(trans, "labels.with_answers", "Com Respostas"),
                        t(trans, "labels.only_questions", "Só Perguntas")
                    ]
                    generation_mode = st.radio(
                        t(trans, "labels.generation_mode", "Modo de Geração"),
                        mode_options,
                        key="generation_mode",
                        help=t(trans, "labels.generation_mode_help", "Escolha se quer gerar perguntas com respostas ou apenas as perguntas (para quiz)")
                    )
                
                st.divider()
                
                # Botão para gerar perguntas
                if st.button(
                    t(trans, "buttons.generate_questions", "❓ Gerar Perguntas"),
                    type="primary",
                    use_container_width=True,
                    key="generate_questions_btn"
                ):
                    if not context_text:
                        st.error(t(trans, "messages.select_valid_scope", "Por favor, selecione um escopo válido."))
                    else:
                        online, offline_reason = check_ollama_online()
                        if not online:
                            detail = offline_reason or "Sem resposta do servidor."
                            st.error(t(trans, "messages.ollama_offline_detail", "Ollama está offline ({detail}). Ligue o servidor e tente novamente.").format(detail=detail))
                        else:
                            with st.spinner(t(trans, "messages.generating_questions", "❓ Gerando perguntas bíblicas...")):
                                # Criar prompt baseado no modo selecionado
                                with_answers = (generation_mode == mode_options[0])
                                
                                if with_answers:
                                    prompt_request = f"""Com base no texto bíblico fornecido, gere EXATAMENTE {questions_count} perguntas sobre curiosidades, 
                                    fatos interessantes, contexto histórico, personagens, ensinamentos e eventos descritos.
                                    
                                    IMPORTANTE - Instruções para respostas:
                                    - Respostas CURTAS e DIRETAS (máximo 1-2 frases)
                                    - Use linguagem teológica equilibrada e respeitosa
                                    - Evite interpretações que tornem Jesus, Deus ou personagens bíblicos negativos
                                    - Cite versículos específicos quando possível
                                    - Foque em FATOS do texto, não em especulações
                                    
                                    Formato OBRIGATÓRIO:
                                    1. [Pergunta aqui]
                                    R: [Resposta curta e direta em 1-2 frases]
                                    
                                    2. [Próxima pergunta]
                                    R: [Próxima resposta curta]
                                    
                                    Continue até completar TODAS as {questions_count} perguntas.
                                    Foque em perguntas que testem conhecimento profundo e curiosidades interessantes sobre o texto."""
                                else:
                                    prompt_request = f"""Com base no texto bíblico fornecido, gere EXATAMENTE {questions_count} perguntas sobre curiosidades, 
                                    fatos interessantes, contexto histórico, personagens, ensinamentos e eventos descritos.
                                    
                                    Gere APENAS as perguntas, SEM respostas (para usar como quiz ou teste).
                                    
                                    Formato OBRIGATÓRIO:
                                    1. [Pergunta aqui]
                                    2. [Próxima pergunta]
                                    3. [Próxima pergunta]
                                    
                                    Continue até completar TODAS as {questions_count} perguntas.
                                    Foque em perguntas que testem conhecimento profundo e curiosidades interessantes sobre o texto."""
                                
                                prompt = build_prompt(context_text, prompt_request, reference=reference)
                                
                                # Calcular max_tokens baseado na quantidade de perguntas
                                # Com respostas curtas: 80 tokens por pergunta; Sem respostas: 50 tokens
                                tokens_per_question = 80 if with_answers else 50
                                max_tokens = min(questions_count * tokens_per_question + 800, 8000)
                                
                                # Calcular timeout dinamicamente baseado na quantidade de perguntas
                                # Aproximadamente 8-10 segundos por pergunta com resposta, 3-4 segundos sem resposta
                                seconds_per_question = 10 if with_answers else 4
                                dynamic_timeout = max(180, questions_count * seconds_per_question)  # Mínimo 180s
                                
                                ok, result = query_ollama(
                                    selected_model, 
                                    prompt, 
                                    max_tokens=max_tokens,
                                    timeout=dynamic_timeout,
                                    auto_continue=True,
                                    lang_code=lang_code,
                                    show_progress=True
                                )
                            
                            if ok:
                                # Salvar no histórico
                                if "questions_history" not in st.session_state:
                                    st.session_state.questions_history = []
                                
                                mode_text = mode_options[0] if with_answers else mode_options[1]
                                
                                question_entry = {
                                    "timestamp": time.time(),
                                    "reference": reference,
                                    "scope": scope_selection,
                                    "questions_count": questions_count,
                                    "mode": mode_text,
                                    "questions": result,
                                    "version": version,
                                    "model": selected_model,
                                    "with_answers": with_answers
                                }
                                
                                st.session_state.questions_history.insert(0, question_entry)
                                auto_save_history("questions_history", st.session_state.questions_history)
                                
                                st.success(t(trans, "messages.questions_generated", "✅ Perguntas geradas e salvas no histórico!"))
                                st.info(t(trans, "messages.check_questions_history", "📚 Acesse a aba 'Histórico de Perguntas' para ver todas as suas perguntas."))
                                
                                # Mostrar preview
                                with st.expander(t(trans, "expanders.questions_preview", "👁️ Prévia das Perguntas"), expanded=True):
                                    st.markdown(result)
                            else:
                                st.error(result)
            
            with questions_subtabs[1]:
                st.markdown(t(trans, "captions.questions_history_description", "Todas as perguntas geradas são salvas automaticamente aqui."))
                
                if not st.session_state.get("questions_history"):
                    st.info(t(trans, "messages.no_questions_history", "Nenhuma pergunta gerada ainda."))
                else:
                    # Filtros
                    col_filter1, col_filter2 = st.columns(2)
                    
                    with col_filter1:
                        filter_mode = st.selectbox(
                            t(trans, "labels.filter_by_mode", "Filtrar por modo"),
                            [t(trans, "labels.all", "Todos"), 
                             t(trans, "labels.with_answers", "Com Respostas"),
                             t(trans, "labels.only_questions", "Só Perguntas")],
                            key="filter_questions_mode"
                        )
                    
                    with col_filter2:
                        search_text = st.text_input(
                            t(trans, "labels.search", "🔍 Buscar"),
                            key="search_questions",
                            placeholder=t(trans, "labels.search_placeholder", "Digite para buscar...")
                        )
                    
                    # Aplicar filtros
                    filtered_questions = st.session_state.questions_history
                    
                    if filter_mode != t(trans, "labels.all", "Todos"):
                        filtered_questions = [q for q in filtered_questions if q.get("mode") == filter_mode]
                    
                    if search_text:
                        search_lower = search_text.lower()
                        filtered_questions = [
                            q for q in filtered_questions
                            if search_lower in q.get("reference", "").lower() or
                               search_lower in q.get("questions", "").lower()
                        ]
                    
                    st.caption(t(trans, "captions.questions_found", "❓ {count} conjunto(s) de perguntas encontrado(s)").format(count=len(filtered_questions)))
                    
                    for idx, q_entry in enumerate(filtered_questions):
                        timestamp_str = time.strftime(
                            t(trans, 'formatting.timestamp_format', '%d/%m/%Y às %H:%M'),
                            time.localtime(q_entry["timestamp"])
                        )
                        
                        with st.expander(
                            f"❓ {q_entry.get('reference', 'Perguntas')} - {q_entry.get('questions_count', 0)} perguntas ({timestamp_str})",
                            expanded=False
                        ):
                            st.markdown(f"**{t(trans, 'labels.reference_colon', 'Referência:')}** {q_entry.get('reference', 'N/A')}")
                            st.markdown(f"**{t(trans, 'labels.questions_count_colon', 'Quantidade:')}** {q_entry.get('questions_count', 'N/A')}")
                            st.markdown(f"**{t(trans, 'labels.mode_colon', 'Modo:')}** {q_entry.get('mode', 'N/A')}")
                            st.markdown(f"**{t(trans, 'labels.version_colon', 'Versão:')}** {q_entry.get('version', 'N/A')}")
                            st.markdown(f"**{t(trans, 'labels.model_colon', 'Modelo:')}** {q_entry.get('model', 'N/A')}")
                            st.markdown("---")
                            st.markdown(q_entry['questions'])
                            st.markdown("---")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                if st.button(t(trans, "buttons.copy", "📋 Copiar"), key=f"questions_copy_{idx}", use_container_width=True):
                                    st.code(q_entry['questions'], language=None)
                                    st.success(t(trans, "messages.ready_to_copy", "Pronto!"))
                            with col_b:
                                if st.button(t(trans, "buttons.generate_pdf", "📄 PDF"), key=f"questions_pdf_{idx}", use_container_width=True):
                                    pdf_buffer = generate_questions_pdf(q_entry, trans)
                                    pdf_filename = f"perguntas_biblicas_{int(q_entry['timestamp'])}.pdf"
                                    b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" style="display:inline-block;padding:0.5rem 1rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:bold;">📥 Baixar</a>'
                                    st.markdown(href, unsafe_allow_html=True)
                                    st.success("✅ PDF gerado!")
                            with col_c:
                                if st.button(t(trans, "buttons.delete", "🗑️"), key=f"questions_del_{idx}", use_container_width=True):
                                    st.session_state.questions_history.remove(q_entry)
                                    auto_save_history("questions_history", st.session_state.questions_history)
                                    st.toast(t(trans, "messages.questions_deleted", "✅ Perguntas excluídas!"), icon="✅")

    with tabs[5]:
        st.subheader(t(trans, "sections.import_data", "Importar dados bíblicos"))
        
        # Informações sobre organização por idioma
        st.info(f"📁 **{t(trans, 'labels.language', 'Idioma')} {t(trans, 'labels.selected_colon', 'Selecionado:')}** {available_languages.get(lang_code, lang_code)}")
        st.markdown(f"**📂 {t(trans, 'labels.import_folder', 'Pasta de importação:')}** `Dados_Json/{lang_code}/`")
        
        st.divider()
        
        # Verificar arquivos disponíveis na pasta do idioma
        lang_dir = LOCAL_JSON_DIR / lang_code
        if lang_dir.exists():
            json_files = list(lang_dir.glob("*.json"))
            json_files = [f for f in json_files if f.name.lower() != "readme.md"]
            
            if json_files:
                st.success(f"✅ **{len(json_files)} {t(trans, 'labels.files_found', 'arquivo(s) encontrado(s)')}**")
                cols = st.columns([3, 1])
                with cols[0]:
                    for file in json_files:
                        st.text(f"  📄 {file.name}")
            else:
                st.warning(t(trans, "warnings.no_json_files", "⚠️ Nenhum arquivo JSON encontrado em `Dados_Json/{lang}/`").format(lang=lang_code))
                st.caption(t(trans, "messages.add_json_files", "💡 Adicione arquivos .json de versões bíblicas nesta pasta e clique em 'Importar'."))
        else:
            st.error(t(trans, "warnings.folder_not_exist", "❌ Pasta `Dados_Json/{lang}/` não existe.").format(lang=lang_code))
            st.caption(t(trans, "captions.folder_instruction", "Crie a pasta manualmente ou a aplicação criará automaticamente ao importar."))
        
        st.divider()
        
        # Opções de importação
        col1, col2 = st.columns(2)
        with col1:
            version_filter_value = st.text_input(
                t(trans, "labels.filter_versions", "🔍 Filtrar versões (opcional)"), 
                value="",
                placeholder=t(trans, "labels.import_placeholder_versions", "Ex: nvi,kjv,acf"),
                help=t(trans, "help.filter_versions", "Deixe vazio para importar todas as versões disponíveis na pasta")
            )
        with col2:
            keep_existing = st.checkbox(t(trans, "labels.keep_existing", "✅ Manter versões já importadas"), value=True, help=t(trans, "labels.keep_existing_help", "Mesclar com versões existentes ao invés de substituir"))
        
        # Botão de importação
        if st.button(t(trans, "buttons.import_versions", "🔄 Importar Versões da Pasta"), type="primary", use_container_width=True):
            target_versions = parse_version_filter(version_filter_value)
            lang_json_dir = LOCAL_JSON_DIR / lang_code
            
            if not lang_json_dir.exists():
                st.error(t(trans, "warnings.folder_not_found", "❌ Pasta `Dados_Json/{lang}/` não encontrada.").format(lang=lang_code))
                st.info(t(trans, "messages.create_folder_add_json", "💡 Crie a pasta e adicione arquivos JSON de versões bíblicas."))
            else:
                with st.spinner(t(trans, "messages.importing_versions", "⏳ Importando versões...")):
                    local_versions = load_local_json_versions(lang_json_dir, version_filter=target_versions)
                
                if not local_versions:
                    st.warning(t(trans, "warnings.no_versions_found", "⚠️ Nenhuma versão encontrada em `Dados_Json/{lang}/`.").format(lang=lang_code))
                    st.info(t(trans, "messages.add_json_retry", "💡 Adicione arquivos JSON na pasta e tente novamente."))
                else:
                    persist_versions(local_versions, merge=keep_existing)
                    st.success(f"✅ **{len(local_versions)} versão(ões) importada(s) com sucesso!**")
                    st.balloons()
                    st.info(t(trans, "messages.page_will_reload", "🔄 A página será recarregada..."))
                    rerun()
        
        st.divider()
        
        # Informações de ajuda
        with st.expander(t(trans, "expanders.how_to_add_versions", "ℹ️ Como Adicionar Versões Bíblicas"), expanded=False):
            st.markdown(f"""
            ### {t(trans, "sections.folder_structure", "📁 Estrutura de Pastas por Idioma")}
            
            ```
            Dados_Json/
              ├── pt/     ← Versões em Português
              │   ├── nvi.json
              │   ├── acf.json
              │   └── aa.json
              ├── en/     ← English Versions
              │   ├── kjv.json
              │   └── niv.json
              ├── es/     ← Versiones en Español
              │   └── rv1960.json
              └── ...     ← Outros idiomas
            ```
            
            ### 🚀 Passos para Adicionar uma Versão
            
            1. **Baixe** o arquivo JSON da versão bíblica desejada
            2. **Coloque** o arquivo na pasta do idioma: `Dados_Json/{lang_code}/`
            3. **Clique** em t(trans, "buttons.import_versions", "🔄 Importar Versões da Pasta")
            4. **Aguarde** a confirmação e recarregamento automático
            
            ### 🌐 Fontes de Bíblias JSON
            
            - **Português (pt)**: 
              - [github.com/thiagobodruk/bible](https://github.com/thiagobodruk/bible)
              - Contém: NVI, ACF, AA, NTLH, etc.
            
            - **English (en)**: 
              - [github.com/scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)
              - Contém: KJV, NIV, ESV, NKJV, etc.
            
            - **Español (es)**:
              - [github.com/thiagobodruk/bible](https://github.com/thiagobodruk/bible) (branch es)
              - Contém: RV1960, RV1995, DHH, etc.
            
            - **Outros idiomas**: 
              - Procure por "bible json [idioma]" no GitHub
              - Verifique se o formato é compatível (livro/capítulo/versículo)
            
            ### 🛠️ Formato do JSON
            
            Os arquivos devem seguir este formato básico:
            ```json
            {{
              "version": "NVI",
              "books": [
                {{
                  "name": "Gênesis",
                  "chapters": [
                    [
                      "No princípio Deus criou os céus e a terra...",
                      "Era a terra sem forma e vazia..."
                    ]
                  ]
                }}
              ]
            }}
            ```
            
            ### ⚙️ Filtro de Versões
            
            Use o campo "Filtrar versões" para importar apenas versões específicas:
            - **Vazio**: Importa todas as versões encontradas
            - **nvi**: Importa apenas NVI
            - **nvi,kjv,acf**: Importa NVI, KJV e ACF (separadas por vírgula)
            """)



if __name__ == "__main__":
    main()
