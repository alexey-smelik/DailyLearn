import json
import logging
from typing import Any

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings
from app.quiz.exceptions import LLMResponseParseError, LLMUnavailableError

logger = logging.getLogger(__name__)

_RETRYABLE_STATUS_CODES = frozenset({500, 502, 503, 504})


class OllamaClient:
    """Async HTTP client for the Ollama /api/generate endpoint with retry logic."""

    def __init__(self) -> None:
        self._base_url = settings.ollama_base_url
        self._timeout = settings.ollama_timeout

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, LLMUnavailableError)),
        stop=stop_after_attempt(settings.ollama_max_retries),
        wait=wait_exponential(
            multiplier=1,
            min=settings.ollama_retry_min_wait,
            max=settings.ollama_retry_max_wait,
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def generate(self, model: str, prompt: str) -> dict[str, Any]:
        """Call Ollama and return the parsed JSON payload from the model response."""
        logger.info(
            "Calling Ollama model=%s prompt_chars=%d",
            model,
            len(prompt),
        )
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(
                    f"{self._base_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json",
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "num_predict": 4096,
                        },
                    },
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in _RETRYABLE_STATUS_CODES:
                    raise LLMUnavailableError(
                        f"Ollama returned HTTP {exc.response.status_code}"
                    ) from exc
                raise

        raw_text: str = response.json().get("response", "")
        logger.debug("Raw LLM response (first 500 chars): %s", raw_text[:500])

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            logger.warning(
                "LLM returned non-JSON payload: %s", raw_text[:300]
            )
            raise LLMResponseParseError(
                f"LLM response is not valid JSON: {raw_text[:300]}"
            ) from exc
