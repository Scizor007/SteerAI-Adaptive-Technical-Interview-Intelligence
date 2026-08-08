"""OpenRouter LLM provider — uses the standard OpenAI-compatible REST API."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import config
from services.llm.provider import LLMProvider

logger = logging.getLogger(__name__)

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterProvider(LLMProvider):
    """Talks to OpenRouter via its REST API (no SDK dependency)."""

    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.model = config.OPENROUTER_MODEL
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY is not set — provider will fail at runtime.")

    # ── LLMProvider interface ───────────────────────────────────────────

    def generate_text(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.LLM_TEMPERATURE,
            "top_p": config.LLM_TOP_P,
            "max_tokens": config.LLM_MAX_TOKENS,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://steerai.dev",
            "X-Title": "SteerAI Interview Platform",
        }

        data = json.dumps(payload).encode("utf-8")
        req = Request(_OPENROUTER_URL, data=data, headers=headers, method="POST")

        try:
            with urlopen(req, timeout=config.LLM_TIMEOUT) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"OpenRouter HTTP {exc.code}: {error_body[:500]}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(f"OpenRouter connection error: {exc.reason}") from exc

        # Navigate the OpenAI-compatible response
        choices = body.get("choices", [])
        if not choices:
            raise ValueError(f"OpenRouter returned no choices: {json.dumps(body)[:300]}")
        text = choices[0].get("message", {}).get("content", "")
        if not text:
            raise ValueError("OpenRouter returned an empty content field.")
        return text

    @property
    def display_name(self) -> str:
        return f"OpenRouter / {self.model}"
