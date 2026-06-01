from __future__ import annotations

import io
import json
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.config import LOCAL_JSON_DIR, TRANSLATIONS_DIR, load_providers_config, save_providers_config
from backend.models import ExportPdfRequest, ExegesisRequest, ExegesisResponse, GenerationRequest, GenerationResponse
from backend.services.bible_service import list_languages, load_bible_data_by_language
from backend.services.ollama_service import check_ollama_online, generate_with_ollama, list_ollama_models
from backend.services.providers import get_provider, list_available_providers, provider_label, DEFAULT_MODELS

load_dotenv()

app = FastAPI(
    title="Biblical Study API",
    version="0.1.0",
    description="Fase 1 da migracao Streamlit -> FastAPI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _resolve_version(data: dict[str, Any], version: str | None) -> tuple[str, dict[str, Any]]:
    versions = data.get("versions", {}) if isinstance(data, dict) else {}
    if not versions:
        raise HTTPException(status_code=404, detail="Nenhuma versao biblica encontrada")

    if not version:
        first_key = next(iter(versions.keys()))
        return first_key, versions[first_key]

    for key, value in versions.items():
        if key.lower() == version.lower():
            return key, value

    raise HTTPException(status_code=404, detail=f"Versao nao encontrada: {version}")


def _normalize_pdf_text(value: str) -> str:
    return str(value or "").encode("latin-1", "replace").decode("latin-1")


def _translate_provider_error(error_code: str, provider: str) -> str:
    friendly = {
        "invalid_api_key": "Chave de API invalida. Verifique em Configuracoes.",
        "rate_limit": "Limite de requisicoes excedido. Aguarde ou altere o provedor.",
        "quota_exhausted": "Cota do provedor esgotada. Verifique seu plano.",
        "timeout": "Tempo limite excedido. Tente novamente ou use o Ollama.",
        "connection_error": "Sem conexao com o provedor. Verifique sua internet ou use o Ollama.",
        "empty_response": "Provedor retornou resposta vazia. Tente novamente.",
    }
    msg = friendly.get(error_code, error_code)
    return f"[ERRO: {provider}] {msg}"


def _build_prompt(language: str, reference: str, context: str, request: str) -> str:
    language = (language or "pt").lower()
    language_hint = {
        "pt": "Responda em portugues.",
        "en": "Answer in English.",
        "es": "Responde en espanol.",
    }.get(language, "Responda no idioma solicitado pelo usuario.")

    return (
        "Voce e um guia teologico cuidadoso e fiel ao texto biblico. "
        "Produza uma resposta objetiva, clara e pastoral sem inventar versiculos.\n\n"
        f"Referencia: {reference}\n"
        f"Texto base:\n{context}\n\n"
        f"Pedido: {request}\n"
        f"Instrucao de idioma: {language_hint}\n"
        "Se algo nao estiver no texto, diga com transparencia."
    )


def _render_pdf_bytes(title: str, subtitle: str | None, sections: list[dict[str, str]], footer: str | None) -> bytes:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, _normalize_pdf_text(title), align="C")

    if subtitle:
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _normalize_pdf_text(subtitle), align="C")

    pdf.ln(4)

    for section in sections:
        heading = section.get("heading", "")
        body = section.get("body", "")
        if heading:
            pdf.set_font("Helvetica", "B", 13)
            pdf.multi_cell(0, 8, _normalize_pdf_text(heading))
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _normalize_pdf_text(body or ""))
        pdf.ln(2)

    if footer:
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(0, 5, _normalize_pdf_text(footer), align="C")

    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "biblical-study-api",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ollama_online": check_ollama_online(),
    }


@app.get("/api/meta/languages")
def get_languages() -> dict[str, Any]:
    return {"items": list_languages()}


@app.get("/api/meta/import-sources")
def get_import_sources(lang: str = Query("pt", min_length=2, max_length=5)) -> dict[str, Any]:
    lang_dir = LOCAL_JSON_DIR / lang
    items: list[dict[str, Any]] = []

    if lang_dir.exists():
        for path in sorted(lang_dir.glob("*.json")):
            if path.name.lower() == "readme.json":
                continue
            items.append(
                {
                    "name": path.name,
                    "version": path.stem.upper(),
                    "size": path.stat().st_size,
                    "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )

    return {"language": lang, "folder": str(lang_dir), "items": items}


@app.get("/api/meta/translation")
def get_translation(lang: str = Query("pt", min_length=2, max_length=5)) -> dict[str, Any]:
    normalized = (lang or "pt").lower()
    file_path = TRANSLATIONS_DIR / f"{normalized}.json"
    if not file_path.exists():
        normalized = "pt"
        file_path = TRANSLATIONS_DIR / "pt.json"

    if not file_path.exists():
        return {"language": normalized, "items": {}}

    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        payload = {}

    return {"language": normalized, "items": payload if isinstance(payload, dict) else {}}


@app.get("/api/bible/versions")
def get_versions(lang: str = Query("pt", min_length=2, max_length=5)) -> dict[str, Any]:
    data = load_bible_data_by_language(lang)
    versions = list(data.get("versions", {}).keys())
    return {"language": lang, "versions": versions}


@app.get("/api/bible/books")
def get_books(
    lang: str = Query("pt", min_length=2, max_length=5),
    version: str | None = None,
) -> dict[str, Any]:
    data = load_bible_data_by_language(lang)
    version_name, version_data = _resolve_version(data, version)
    books = version_data.get("books", {})

    items = []
    for key, book in books.items():
        items.append(
            {
                "key": key,
                "name": book.get("name", key),
                "abbrev": book.get("abbrev", ""),
                "chapters": len(book.get("chapters", {})),
                "order": book.get("order", 0),
            }
        )

    if any(item.get("order") for item in items):
        items.sort(key=lambda x: (x.get("order") or 0, x["name"]))
    else:
        items.sort(key=lambda x: x["name"])
    return {"language": lang, "version": version_name, "items": items}


@app.get("/api/bible/chapter")
def get_chapter(
    book: str,
    chapter: int = Query(..., ge=1),
    lang: str = Query("pt", min_length=2, max_length=5),
    version: str | None = None,
) -> dict[str, Any]:
    data = load_bible_data_by_language(lang)
    version_name, version_data = _resolve_version(data, version)
    books = version_data.get("books", {})

    if book not in books:
        for key in books:
            if key.lower() == book.lower():
                book = key
                break

    if book not in books:
        raise HTTPException(status_code=404, detail=f"Livro nao encontrado: {book}")

    chapter_key = str(chapter)
    chapter_data = books[book].get("chapters", {}).get(chapter_key)
    if not chapter_data:
        raise HTTPException(status_code=404, detail=f"Capitulo nao encontrado: {chapter}")

    verses = chapter_data.get("verses", {})
    return {
        "language": lang,
        "version": version_name,
        "book": books[book].get("name", book),
        "chapter": chapter,
        "verses": verses,
    }


@app.post("/api/ai/exegesis", response_model=ExegesisResponse)
def exegesis(payload: ExegesisRequest) -> ExegesisResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Texto biblico vazio")

    # Provider externo
    if payload.provider and payload.provider != "ollama":
        config = load_providers_config()
        provider_cfg = config["providers"].get(payload.provider, {})
        if not provider_cfg.get("api_key"):
            return ExegesisResponse(
                model="", reference=payload.reference,
                response="[ERRO] Chave de API nao configurada para este provedor."
            )
        provider = get_provider(payload.provider, provider_cfg)
        if not provider:
            return ExegesisResponse(
                model="", reference=payload.reference,
                response="[ERRO] Provedor nao suportado."
            )
        result = provider.generate(
            prompt=payload.text,
            kind="study",
            model=payload.model or provider_cfg.get("model"),
            timeout_sec=180,
        )
        if "error" in result:
            return ExegesisResponse(
                model="", reference=payload.reference,
                response=_translate_provider_error(result["error"], payload.provider)
            )
        return ExegesisResponse(
            model=result.get("model", payload.model or ""),
            reference=payload.reference,
            response=result.get("response", ""),
        )

    # Fallback Ollama
    lang = payload.language.lower()
    language_hint = {
        "pt": "Responda em portugues.",
        "en": "Answer in English.",
        "es": "Responde en espanol.",
    }.get(lang, "Responda no idioma solicitado pelo usuario.")

    prompt = (
        "Voce e um guia teologico cuidadoso e fiel ao texto biblico. "
        "Produza uma explicacao com contexto, observacoes praticas e aplicacao pastoral.\n\n"
        f"Referencia: {payload.reference}\n"
        f"Texto base:\n{payload.text}\n\n"
        f"Instrucao de idioma: {language_hint}\n"
        "Nao invente versiculos. Se algo nao estiver no texto, diga com transparencia."
    )

    try:
        result = generate_with_ollama(prompt=prompt, model=payload.model, timeout_sec=180)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    response = result.get("response", "").strip()
    if not response:
        raise HTTPException(status_code=502, detail="Ollama retornou resposta vazia")

    return ExegesisResponse(
        model=result.get("model", payload.model or ""),
        reference=payload.reference,
        response=response,
    )


@app.post("/api/ai/generate", response_model=GenerationResponse)
def generate(payload: GenerationRequest) -> GenerationResponse:
    if not payload.context.strip():
        raise HTTPException(status_code=400, detail="Contexto vazio")
    if not payload.request.strip():
        raise HTTPException(status_code=400, detail="Pedido vazio")

    # Provider externo (nao-Ollama)
    if payload.provider and payload.provider != "ollama":
        config = load_providers_config()
        provider_cfg = config["providers"].get(payload.provider, {})
        if not provider_cfg.get("api_key"):
            return GenerationResponse(
                kind=payload.kind, model="", reference=payload.reference,
                response="[ERRO] Chave de API nao configurada para este provedor. "
                         "Configure em Configuracoes ou use o Ollama como fallback."
            )
        provider = get_provider(payload.provider, provider_cfg)
        if not provider:
            return GenerationResponse(
                kind=payload.kind, model="", reference=payload.reference,
                response="[ERRO] Provedor nao suportado."
            )
        result = provider.generate(
            prompt=payload.request,
            kind=payload.kind,
            model=payload.model or provider_cfg.get("model"),
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
            timeout_sec=payload.timeout_sec,
        )
        if "error" in result:
            error_msg = _translate_provider_error(result["error"], payload.provider)
            return GenerationResponse(
                kind=payload.kind, model="", reference=payload.reference,
                response=error_msg
            )
        return GenerationResponse(
            kind=payload.kind,
            model=result.get("model", payload.model or ""),
            reference=payload.reference,
            response=result.get("response", ""),
        )

    # Fallback: Ollama (codigo existente)
    prompt = _build_prompt(payload.language, payload.reference, payload.context, payload.request)
    try:
        result = generate_with_ollama(
            prompt=prompt,
            model=payload.model,
            timeout_sec=payload.timeout_sec,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    response = result.get("response", "").strip()
    if not response:
        raise HTTPException(status_code=502, detail="Ollama retornou resposta vazia")
    return GenerationResponse(
        kind=payload.kind,
        model=result.get("model", payload.model or ""),
        reference=payload.reference,
        response=response,
    )


@app.get("/api/ai/models")
def get_ollama_models() -> dict[str, Any]:
    try:
        models = list_ollama_models(timeout_sec=6)
        return {"online": True, "items": models}
    except RuntimeError as exc:
        return {"online": False, "items": [], "error": str(exc)}


# ===== PROVIDER ROUTES =====

@app.get("/api/providers")
def get_providers() -> dict[str, Any]:
    config = load_providers_config()
    safe_config: dict[str, Any] = {}
    for pid, cfg in config.get("providers", {}).items():
        safe_config[pid] = {k: v for k, v in cfg.items() if k != "api_key"}
        safe_config[pid]["has_key"] = bool(cfg.get("api_key"))
    safe_config["active_provider"] = config.get("active_provider", "ollama")
    return safe_config


@app.post("/api/providers/config")
def save_provider_config(data: dict) -> dict[str, str]:
    provider_id = data.get("provider_id")
    if not provider_id:
        raise HTTPException(status_code=400, detail="provider_id is required")
    config = load_providers_config()
    if provider_id not in config["providers"]:
        config["providers"][provider_id] = {}
    if "api_key" in data:
        config["providers"][provider_id]["api_key"] = data["api_key"]
    if "model" in data:
        config["providers"][provider_id]["model"] = data["model"]
    if "enabled" in data:
        config["providers"][provider_id]["enabled"] = data["enabled"]
    save_providers_config(config)
    return {"status": "ok"}


@app.post("/api/providers/active")
def set_active_provider(data: dict) -> dict[str, str]:
    provider = data.get("provider", "ollama")
    config = load_providers_config()
    config["active_provider"] = provider
    save_providers_config(config)
    return {"status": "ok"}


@app.post("/api/providers/test")
def test_provider(data: dict) -> dict[str, Any]:
    provider_id = data.get("provider_id")
    api_key = data.get("api_key", "")
    model = data.get("model")
    if not provider_id:
        return {"ok": False, "error": "provider_id is required"}
    cfg = {"api_key": api_key, "model": model or DEFAULT_MODELS.get(provider_id, "")}
    provider = get_provider(provider_id, cfg)
    if not provider:
        return {"ok": False, "error": "Provedor nao encontrado"}
    online = provider.check_online()
    if online:
        models = provider.list_models()
        return {"ok": True, "models": models}
    return {"ok": False, "error": "Falha ao conectar. Verifique a chave de API."}


# ===== PDF EXPORT =====

@app.post("/api/export/pdf")
def export_pdf(payload: ExportPdfRequest) -> StreamingResponse:
    pdf_bytes = _render_pdf_bytes(payload.title, payload.subtitle, payload.sections, payload.footer)
    filename = payload.title.strip().replace(" ", "_") or "export"
    headers = {"Content-Disposition": f'attachment; filename="{filename}.pdf"'}
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers=headers)
