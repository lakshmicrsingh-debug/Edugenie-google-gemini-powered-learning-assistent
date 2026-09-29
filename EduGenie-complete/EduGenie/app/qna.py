from .gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = (
        "Answer the student's question directly. Give a concise but useful educational "
        "answer. If the question is ambiguous, state the reasonable interpretation you used. "
        "Do not invent citations or facts.\n\nQuestion: " + question
    )
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, an accurate academic question-answering assistant.",
        temperature=0.2,
        max_output_tokens=700,
    )
