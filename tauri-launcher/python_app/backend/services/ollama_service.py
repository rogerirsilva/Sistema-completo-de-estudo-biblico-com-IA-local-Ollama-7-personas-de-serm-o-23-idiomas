from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

import requests

from backend.config import OLLAMA_BASE, OLLAMA_GENERATE_PATHS, OLLAMA_MODEL_DEFAULT


def _normalize_endpoint(endpoint: str) -> str:
    clean_endpoint = endpoint.strip().lstrip("/")
    if not clean_endpoint:
        return ""

    base_path = urlsplit(OLLAMA_BASE).path.strip("/")
    if not base_path:
        return clean_endpoint

    first_base_part = base_path.split("/", maxsplit=1)[0]
    if clean_endpoint == first_base_part:
        return ""
    if clean_endpoint.startswith(f"{first_base_part}/"):
        return clean_endpoint[len(first_base_part) + 1 :]
    return clean_endpoint


def make_ollama_url(endpoint: str) -> str:
    clean_base = OLLAMA_BASE.rstrip("/")
    clean_endpoint = _normalize_endpoint(endpoint)
    if not clean_endpoint:
        return clean_base
    return f"{clean_base}/{clean_endpoint}"


def check_ollama_online(timeout_sec: int = 2) -> bool:
    try:
        resp = requests.get(make_ollama_url("api/version"), timeout=timeout_sec)
        return resp.ok
    except requests.RequestException:
        return False


def list_ollama_models(timeout_sec: int = 6) -> list[str]:
    endpoints = ("api/tags", "api/ps", "v1/models")
    names: set[str] = set()
    last_error: Exception | None = None

    for endpoint in endpoints:
        try:
            response = requests.get(make_ollama_url(endpoint), timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()

            if endpoint == "api/tags":
                models = data.get("models", []) if isinstance(data, dict) else []
                for item in models:
                    if not isinstance(item, dict):
                        continue
                    names.add(str(item.get("name", "")).strip())
                    names.add(str(item.get("model", "")).strip())
            elif endpoint == "api/ps":
                models = data.get("models", []) if isinstance(data, dict) else []
                for item in models:
                    if not isinstance(item, dict):
                        continue
                    names.add(str(item.get("name", "")).strip())
                    names.add(str(item.get("model", "")).strip())
            else:
                models = data.get("data", []) if isinstance(data, dict) else []
                for item in models:
                    if not isinstance(item, dict):
                        continue
                    names.add(str(item.get("id", "")).strip())
        except requests.RequestException as exc:
            last_error = exc

    clean_names = sorted(name for name in names if name)
    if clean_names:
        return clean_names

    raise RuntimeError(f"Ollama models request failed: {last_error}")


def generate_with_ollama(
    prompt: str,
    model: str | None = None,
    timeout_sec: int = 120,
    temperature: float | None = None,
    max_tokens: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    selected_model = model or OLLAMA_MODEL_DEFAULT
    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
    }

    options: dict[str, Any] = {}
    if temperature is not None:
        options["temperature"] = temperature
    if max_tokens is not None:
        options["num_predict"] = max_tokens
    if options:
        payload["options"] = options

    endpoints: list[str] = []
    for endpoint in OLLAMA_GENERATE_PATHS:
        normalized = _normalize_endpoint(endpoint)
        if normalized and normalized not in endpoints:
            endpoints.append(normalized)
    for fallback in ("api/generate", "api/v1/generate", "v1/generate"):
        normalized = _normalize_endpoint(fallback)
        if normalized and normalized not in endpoints:
            endpoints.append(normalized)

    last_error: Exception | None = None
    for endpoint in endpoints:
        try:
            response = requests.post(
                make_ollama_url(endpoint),
                json=payload,
                timeout=timeout_sec,
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("response") or data.get("text") or ""
            return {
                "model": selected_model,
                "response": str(content).strip(),
                "endpoint": endpoint,
            }
        except requests.RequestException as exc:
            last_error = exc

    raise RuntimeError(f"Ollama request failed for all endpoints: {last_error}")
