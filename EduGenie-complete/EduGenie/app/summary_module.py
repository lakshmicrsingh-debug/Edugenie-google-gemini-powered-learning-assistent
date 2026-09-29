from .gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the educational passage below for quick revision. Preserve the core facts "
        "and relationships. Use a short overview followed by bullet points when appropriate. "
        "Do not add unsupported claims.\n\nPassage:\n" + text
    )
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a clear and faithful educational summarizer.",
        temperature=0.2,
        max_output_tokens=900,
    )
