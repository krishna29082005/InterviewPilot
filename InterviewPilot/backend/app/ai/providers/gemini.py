import json
from typing import Type

from google import genai
from pydantic import BaseModel, ValidationError

from app.ai.exceptions import (
    AIProviderError,
    AIValidationError,
)
from app.ai.providers.base import LLMProvider
from app.core.config import settings


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

        except Exception as e:
            raise AIProviderError(
                f"Gemini request failed: {e}"
            ) from e

        response_text = response.text or ""
        response_text = self._clean_json_response(response_text)

        if response_model is None:
            return response_text

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError as e:

            print("\n" + "=" * 100)
            print("❌ INVALID JSON RETURNED BY GEMINI")
            print("=" * 100)

            print(f"\nError: {e}")
            print(f"Line: {e.lineno}")
            print(f"Column: {e.colno}")
            print(f"Character: {e.pos}")

            start = max(0, e.pos - 150)
            end = min(len(response_text), e.pos + 150)

            print("\n---------------- CONTEXT ----------------\n")
            print(response_text[start:end])
            print("\n-----------------------------------------")

            print("\n================ FULL RESPONSE =================\n")
            print(response_text)
            print("\n================================================\n")

            raise AIProviderError(
                "Gemini returned invalid JSON."
            ) from e

        print("\n" + "=" * 100)
        print("✅ RAW GEMINI JSON")
        print("=" * 100)
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print("=" * 100 + "\n")

        try:
            parsed = response_model.model_validate(data)

            print("\n" + "=" * 100)
            print("✅ PYDANTIC VALIDATION SUCCESSFUL")
            print("=" * 100 + "\n")

            return parsed

        except ValidationError as e:

            print("\n" + "=" * 100)
            print("❌ PYDANTIC VALIDATION ERROR")
            print("=" * 100)
            print(e)
            print("=" * 100 + "\n")

            raise AIValidationError(
                "AI response failed schema validation."
            ) from e