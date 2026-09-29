from .gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner", hours_per_week: int = 5) -> str:
    prompt = f"""
Create a personalized learning path for the topic: {topic}
Learner level: {level}
Available time: {hours_per_week} hours per week.

Structure the answer as:
1. Learning goal
2. Beginner foundations
3. Intermediate topics
4. Advanced topics
5. Suggested weekly timeline
6. Practice ideas
7. Recommended resource types (videos, articles, books, documentation)
8. How to measure progress
Keep the plan realistic and step-by-step. Do not invent specific URLs.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie's personalized learning-path planner.",
        temperature=0.35,
        max_output_tokens=1400,
    )
