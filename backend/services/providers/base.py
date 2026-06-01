from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> dict[str, Any]:
        ...

    @abstractmethod
    def list_models(self) -> list[str]:
        ...

    @abstractmethod
    def check_online(self) -> bool:
        ...
