"""Abstract LLM provider interface.

Every provider must implement `generate_text(prompt) -> str` which returns
raw text from the model.  All JSON parsing, retries, and fallback logic
lives in LLMService so providers stay simple and swappable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Contract that every LLM backend must satisfy."""

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Send *prompt* to the model and return the raw text response.

        Raises any provider-specific exception on failure — LLMService
        catches all `Exception` subclasses uniformly.
        """
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable label for logging (e.g. 'OpenRouter / deepseek/deepseek-r1')."""
        ...
