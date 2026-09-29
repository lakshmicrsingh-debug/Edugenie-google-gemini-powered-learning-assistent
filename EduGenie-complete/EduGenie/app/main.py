from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .explanation_module import explain_topic
from .learning_path import get_learning_recommendations
from .qna import answer_question
from .quiz_module import generate_quiz
from .schemas import LearningPathRequest, QuizRequest, TextRequest
from .summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent.parent
settings = get_settings()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_length(text: str, limit: int | None = None) -> str:
    value = text.strip()
    max_chars = limit or settings.max_input_chars
    if len(value) > max_chars:
        raise ValueError(f"Input is too long. Maximum allowed is {max_chars} characters.")
    return value


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
    }


@app.post("/qa")
async def qa(payload: TextRequest):
    return {"result": answer_question(validate_length(payload.text))}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"result": explain_topic(validate_length(payload.text, 4000))}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    result = generate_quiz(validate_length(payload.text), payload.count)
    return result.model_dump()


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"result": summarize_text(validate_length(payload.text, settings.max_summary_chars))}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: LearningPathRequest):
    return {
        "result": get_learning_recommendations(
            validate_length(payload.topic, 500), payload.level, payload.hours_per_week
        )
    }
