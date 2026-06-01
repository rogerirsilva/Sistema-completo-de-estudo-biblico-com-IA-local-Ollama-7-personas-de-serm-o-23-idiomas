from __future__ import annotations

from typing import Any

import requests

from .base import BaseProvider


class GeminiProvider(BaseProvider):
    def generate(
        self,
        prompt: str,
        kind: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout_sec: int = 180,
    ) -> dict[str, Any]:
        selected_model = model or self.config.get("model", "gemini-1.5-flash")
        api_key = self.config.get("api_key", "")
        base_url = "https://generativelanguage.googleapis.com/v1beta"

        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        generation_config: dict[str, Any] = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_tokens is not None:
            generation_config["maxOutputTokens"] = max_tokens
        if generation_config:
            payload["generationConfig"] = generation_config

        try:
            response = requests.post(
                f"{base_url}/models/{selected_model}:generateContent",
                params={"key": api_key},
                json=payload,
                timeout=timeout_sec,
            )
            data = response.json()
        except requests.Timeout:
            return {"error": "timeout"}
        except requests.ConnectionError:
            return {"error": "connection_error"}
        except requests.RequestException as e:
            return {"error": str(e)}

        if "error" in data:
            err = data["error"]
            message = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            status = response.status_code
            if status == 401 or status == 403:
                return {"error": "invalid_api_key"}
            if status == 429:
                return {"error": "rate_limit"}
            if "quota" in message.lower() or "insufficient" in message.lower():
                return {"error": "quota_exhausted"}
            return {"error": message}

        candidates = data.get("candidates", [])
        if not candidates:
            return {"error": "empty_response"}
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        return {
            "response": text.strip(),
            "model": data.get("modelVersion", selected_model),
        }

    def list_models(self) -> list[str]:
        api_key = self.config.get("api_key", "")
        try:
            response = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": api_key},
                timeout=10,
            )
            data = response.json()
            return [
                m["name"].replace("models/", "")
                for m in data.get("models", [])
                if isinstance(m, dict) and "generateContent" in m.get("supportedGenerationMethods", [])
            ]
        except Exception:
            return [self.config.get("model", "gemini-1.5-flash")]

    def check_online(self) -> bool:
        return bool(self.list_models())
