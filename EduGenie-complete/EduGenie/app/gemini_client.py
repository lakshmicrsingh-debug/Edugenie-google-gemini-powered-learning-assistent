from functools import lru_cache
from typing import TypeVar

from pydantic import BaseModel

from .config import get_settings

T = TypeVar("T", bound=BaseModel)


class GeminiServiceError(RuntimeError):
    """Raised when Gemini cannot complete a request."""


@lru_cache
def get_client():
    """Create the Gemini client lazily so non-AI route tests can run without the SDK."""
    settings = get_settings()
    if not settings.gemini_api_key:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )
    try:
        from google import genai
    except ImportError as exc:
        raise GeminiServiceError(
            "The google-genai package is not installed. Run: pip install -r requirements.txt"
        ) from exc
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    system_instruction: str,
    temperature: float = 0.3,
    max_output_tokens: int = 1024,
) -> str:
    from google.genai import types

    settings = get_settings()
    try:
        response = get_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini request failed: {exc}") from exc

    text = (response.text or "").strip()
    if not text:
        raise GeminiServiceError("Gemini returned an empty response.")
    return text


def generate_structured(
    prompt: str,
    *,
    schema: type[T],
    system_instruction: str,
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
) -> T:
    from google.genai import types

    settings = get_settings()
    try:
        response = get_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                response_mime_type="application/json",
                response_json_schema=schema.model_json_schema(),
            ),
        )
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini structured request failed: {exc}") from exc

    text = (response.text or "").strip()
    if not text:
        raise GeminiServiceError("Gemini returned an empty structured response.")
    try:
        return schema.model_validate_json(text)
    except Exception as exc:
        raise GeminiServiceError(f"Gemini returned invalid structured data: {exc}") from exc
