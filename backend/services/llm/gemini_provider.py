"""Gemini LLM provider — wraps the google-generativeai SDK."""

from __future__ import annotations

import logging

import config
from services.llm.provider import LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Talks to Google Gemini via the official Python SDK."""

    def __init__(self):
        self.model = None
        try:
            import google.generativeai as genai
            from google.generativeai.types import GenerationConfig
        except ImportError:
            logger.warning("google-generativeai is not installed — GeminiProvider disabled.")
            return

        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set — GeminiProvider will fail.")
            return

        genai.configure(api_key=config.GEMINI_API_KEY)
        self._model_name = config.MODEL_NAME

        generation_config = GenerationConfig(
            temperature=config.LLM_TEMPERATURE,
            top_p=config.LLM_TOP_P,
            max_output_tokens=config.LLM_MAX_TOKENS,
            response_mime_type="application/json",
        )

        self.model = genai.GenerativeModel(
            model_name=self._model_name,
            generation_config=generation_config,
        )

    # ── LLMProvider interface ───────────────────────────────────────────

    def generate_text(self, prompt: str) -> str:
        if self.model is None:
            raise RuntimeError("GeminiProvider is not configured — model is None.")
        response = self.model.generate_content(prompt)
        if not response.text:
            raise ValueError("Gemini returned an empty response.")
        return response.text

    @property
    def display_name(self) -> str:
        name = getattr(self, "_model_name", "unknown")
        return f"Gemini / {name}"
