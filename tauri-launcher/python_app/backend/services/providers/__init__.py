from __future__ import annotations

from .base import BaseProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider

PROVIDER_MAP = {
    "chatgpt": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://api.openai.com/v1"}),
    "deepseek": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://api.deepseek.com"}),
    "grok": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://api.x.ai/v1"}),
    "openrouter": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://openrouter.ai/api/v1"}),
    "target_ai": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://api.target.ai/v1"}),
    "nvidia": lambda cfg: OpenAIProvider({**cfg, "base_url": "https://integrate.api.nvidia.com/v1"}),
    "gemini": lambda cfg: GeminiProvider(cfg),
}

DEFAULT_MODELS = {
    "chatgpt": "gpt-4o-mini",
    "deepseek": "deepseek-chat",
    "grok": "grok-2-latest",
    "openrouter": "openrouter/auto",
    "target_ai": "target-ai-model",
    "nvidia": "meta/llama3-70b-instruct",
    "gemini": "gemini-1.5-flash",
}

PROVIDER_LABELS = {
    "ollama": "\U0001f42a Ollama (Local)",
    "chatgpt": "ChatGPT",
    "deepseek": "DeepSeek",
    "grok": "Grok (xAI)",
    "openrouter": "OpenRouter",
    "target_ai": "Target.AI",
    "nvidia": "NVIDIA NIM",
    "gemini": "Google Gemini",
}


def get_provider(provider_id: str, config: dict) -> BaseProvider | None:
    factory = PROVIDER_MAP.get(provider_id)
    if not factory:
        return None
    return factory(config)


def list_available_providers() -> list[str]:
    return list(PROVIDER_MAP.keys())


def provider_label(provider_id: str) -> str:
    return PROVIDER_LABELS.get(provider_id, provider_id)
