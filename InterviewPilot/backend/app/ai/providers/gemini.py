import json
import logging
from typing import Type

from google import genai
from pydantic import BaseModel, ValidationError

from app.ai.exceptions import (
    AIProviderError,
    AIValidationError,
)
from app.ai.providers.base import LLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    def __init__(self):
        self.client = None

        if settings.GEMINI_API_KEY:
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

    def _clean_json_response(self, response: str) -> str:
        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        return response.strip()

    async def generate(
        self,
        prompt: str,
        response_model: Type[BaseModel] | None = None,
    ):
        if not settings.GEMINI_API_KEY or self.client is None:
            raise AIProviderError(
                "GEMINI_API_KEY is not configured."
            )

        try:
            if response_model is not None:
                response = self.client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "max_output_tokens": 8192,
                    },
                )
            else:
                response = self.client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                )

        except Exception as exc:
            logger.exception("Gemini request failed")
            raise AIProviderError(
                f"Gemini request failed: {exc}"
            ) from exc

        response_text = response.text or ""
        response_text = self._clean_json_response(response_text)

        if response_model is None:
            return response_text

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError as exc:
            logger.error(
                "Gemini returned invalid JSON at position %s.",
                exc.pos,
            )

            raise AIProviderError(
                "Gemini returned invalid JSON."
            ) from exc

        logger.debug(
            "Gemini returned structured JSON for %s",
            response_model.__name__,
        )

        try:
            parsed = response_model.model_validate(data)

            logger.debug(
                "Gemini response validated successfully against %s",
                response_model.__name__,
            )

            return parsed

        except ValidationError as exc:
            logger.error(
                "Gemini response failed validation against %s.",
                response_model.__name__,
            )

            raise AIValidationError(
                "AI response failed schema validation."
            ) from exc