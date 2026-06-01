from __future__ import annotations

from typing import Any

import requests

from .base import BaseProvider

SYSTEM_PROMPTS = {
    "sermon": (
        "You are an experienced preacher. Create a sermon based on the biblical text provided. "
        "Structure it with introduction, development, and practical application."
    ),
    "study": (
        "You are a theologian specializing in exegesis. Provide a deep biblical study with "
        "historical context, original language insights, and cross-references."
    ),
    "devotional": (
        "You are a devotional writer. Create a warm, reflective devotional based on the passage, "
        "connecting it to daily life with practical application."
    ),
    "chat": (
        "You are a theologian answering questions about the Bible. Be accurate, clear, "
        "and faithful to the text."
    ),
    "questions": (
        "You are a Bible educator creating study questions. Generate thoughtful questions "
        "that encourage reflection and understanding of the passage."
    ),
}


class OpenAIProvider(BaseProvider):
    def generate(
        self,
        prompt: str,
        kind: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout_sec: int = 180,
    ) -> dict[str, Any]:
        selected_model = model or self.config.get("model", "gpt-4o-mini")
        messages: list[dict] = [{"role": "user", "content": prompt}]
        system_prompt = None
        if kind and kind in SYSTEM_PROMPTS:
            system_prompt = SYSTEM_PROMPTS[kind]
        if self.config.get("system_prompt"):
            system_prompt = self.config["system_prompt"]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        base_url = self.config["base_url"].rstrip("/")
        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": selected_model,
                    "messages": messages,
                    "max_tokens": max_tokens or self.config.get("max_tokens", 4000),
                    "temperature": temperature if temperature is not None else self.config.get("temperature", 0.2),
                },
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
            if status == 401:
                return {"error": "invalid_api_key"}
            if status == 429:
                return {"error": "rate_limit"}
            if status == 402 or "quota" in message.lower() or "insufficient" in message.lower():
                return {"error": "quota_exhausted"}
            return {"error": message}

        choices = data.get("choices", [])
        if not choices:
            return {"error": "empty_response"}
        content = choices[0].get("message", {}).get("content", "")
        return {
            "response": content.strip(),
            "model": data.get("model", selected_model),
        }

    def list_models(self) -> list[str]:
        base_url = self.config["base_url"].rstrip("/")
        try:
            response = requests.get(
                f"{base_url}/models",
                headers={"Authorization": f"Bearer {self.config['api_key']}"},
                timeout=10,
            )
            data = response.json()
            return [m["id"] for m in data.get("data", []) if isinstance(m, dict)]
        except Exception:
            return [self.config.get("model", "gpt-4o-mini")]

    def check_online(self) -> bool:
        return bool(self.list_models())
