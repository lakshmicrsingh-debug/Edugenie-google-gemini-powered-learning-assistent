from .gemini_client import generate_structured
from .schemas import QuizQuestion, QuizResponse


def generate_quiz(text: str, count: int = 3) -> QuizResponse:
    schema = QuizResponse
    prompt = f"""
Create exactly {count} multiple-choice questions from the educational content below.
Each question must have exactly four distinct options. The correct_answer must exactly match
one option. Include a short explanation of why that answer is correct.
Do not use information outside the supplied content unless it is necessary to make a basic,
well-established question.

Content:
{text}
"""
    # The schema is generated dynamically below because the requested count is user-controlled.
    result = generate_structured(
        prompt,
        schema=schema,
        system_instruction=(
            "You are EduGenie's quiz generator. Produce valid structured MCQs suitable for learning."
        ),
        temperature=0.25,
        max_output_tokens=2500,
    )
    if len(result.questions) != count:
        raise ValueError(f"The model returned {len(result.questions)} questions instead of {count}.")
    for question in result.questions:
        if len(question.options) != 4 or question.correct_answer not in question.options:
            raise ValueError("The model returned an invalid quiz question.")
    return result
