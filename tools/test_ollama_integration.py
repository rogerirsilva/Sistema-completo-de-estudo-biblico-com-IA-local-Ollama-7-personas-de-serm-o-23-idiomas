import os
import sys
from typing import List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
OLLAMA_GENERATE_PATHS = tuple(
    path.strip()
    for path in os.getenv(
        "OLLAMA_GENERATE_PATHS",
        "api/generate,api/v1/generate,v1/generate,generate",
    ).split(",")
    if path.strip()
)
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL_DEFAULT", "llama3")

def make_ollama_url(endpoint: str) -> str:
    clean_base = OLLAMA_BASE.rstrip("/")
    clean_endpoint = endpoint.lstrip("/")
    return f"{clean_base}/{clean_endpoint}"


HEALTH_ENDPOINT = make_ollama_url("/api/version")
MODELS_ENDPOINT = make_ollama_url("/api/models")

TIMEOUT = 5


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


class NotOk(Exception):
    pass


def check_health() -> None:
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=TIMEOUT)
        if response.status_code != 200:
            raise NotOk(f"unexpected status {response.status_code}: {response.text}")
    except requests.RequestException as exc:
        raise NotOk(f"health check failed: {exc}") from exc


def list_models() -> List[str]:
    try:
        response = requests.get(MODELS_ENDPOINT, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        models = [item.get("name") or item.get("model") or item.get("id") for item in data if isinstance(item, dict)]
        return [name for name in models if name]
    except requests.RequestException as exc:
        raise NotOk(f"listing models failed: {exc}") from exc


def generate_sample(model: str, prompt: str = "Ping") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": "Give a short acknowledgment.",
        "temperature": 0.1,
        "max_tokens": 16,
    }
    endpoints = OLLAMA_GENERATE_PATHS or (
        "api/generate",
        "api/v1/generate",
        "v1/generate",
        "generate",
    )
    tried: List[str] = []
    last_exc: Optional[Exception] = None
    response = None
    for endpoint in endpoints:
        url = make_ollama_url(endpoint)
        tried.append(url)
        try:
            response = requests.post(url, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            last_exc = exc
            response = None
            continue
    if response is None:
        suffix = f": {last_exc}" if last_exc else ""
        raise NotOk(f"generate request failed{suffix} (tried {', '.join(tried)})")
    data = response.json()
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise NotOk("no choices returned from generate")
    first = choices[0]
    content = (first.get("message") or first).get("content") if isinstance(first, dict) else None
    if not content:
        content = first.get("output") if isinstance(first, dict) else None
    if not content:
        raise NotOk("generate returned empty content")
    return content.strip()


def main() -> None:
    try:
        print(f"OLLAMA_BASE={OLLAMA_BASE}")
        print("Checking health endpoint...")
        check_health()
        print("Health check OK")
        print("Fetching available models...")
        models = list_models()
        if not models:
            print("Warning: no models reported, proceeding with default")
        selected_model = DEFAULT_MODEL if DEFAULT_MODEL in models else (models[0] if models else DEFAULT_MODEL)
        print(f"Using model {selected_model}")
        print("Sending quick generate request...")
        generated = generate_sample(selected_model)
        print("Sample output:")
        print(generated)
        print("Integration test succeeded.")
    except NotOk as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
