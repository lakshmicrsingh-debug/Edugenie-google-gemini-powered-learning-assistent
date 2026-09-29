from functools import lru_cache

from .config import get_settings
from .gemini_client import generate_text


@lru_cache
def _local_pipeline():
    """Load the optional LaMini model only when explicitly enabled."""
    from transformers import pipeline

    settings = get_settings()
    return pipeline("text2text-generation", model=settings.local_explainer_model)


def explain_topic(topic: str) -> str:
    settings = get_settings()
    prompt = (
        "Explain the following educational topic for a beginner. Use simple language, "
        "a short analogy when useful, and 3-5 key points. Avoid unnecessary jargon.\n\n"
        f"Topic: {topic}"
    )

    if settings.use_local_explainer:
        try:
            result = _local_pipeline()(prompt, max_new_tokens=300, do_sample=False)
            return result[0]["generated_text"].strip()
        except ImportError as exc:
            raise RuntimeError(
                "Local explanation is enabled, but optional dependencies are missing. "
                "Install requirements-local.txt or set USE_LOCAL_EXPLAINER=false."
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Local explanation model failed: {exc}") from exc

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a patient educational tutor. Explain concepts accurately, "
            "concisely, and at the learner's level."
        ),
        temperature=0.25,
        max_output_tokens=500,
    )
