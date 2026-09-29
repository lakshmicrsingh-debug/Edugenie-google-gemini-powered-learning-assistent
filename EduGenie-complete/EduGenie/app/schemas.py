from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=16000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=16000)
    count: int = Field(default=3, ge=1, le=10)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="beginner", max_length=50)
    hours_per_week: int = Field(default=5, ge=1, le=40)

    @field_validator("topic", "level")
    @classmethod
    def strip_fields(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value
