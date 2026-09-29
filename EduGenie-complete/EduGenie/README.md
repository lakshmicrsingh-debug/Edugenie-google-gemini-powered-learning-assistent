# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI web application based on the supplied project documentation. It provides:

- Question answering (`/qa`)
- Simplified concept explanations (`/explain`)
- Structured MCQ quiz generation (`/quiz`)
- Educational summarization (`/summarize`)
- Personalized learning paths (`/learn/recommendations`)

The original document describes Gemini 1.5 Pro for cloud tasks and LaMini-Flan-T5-783M for local explanations. The implementation keeps the same module architecture but uses Google's current `google-genai` SDK and a configurable current Gemini model. The LaMini model is optional because installing PyTorch/Transformers is substantially heavier than the cloud-only path.

## Project structure

```text
EduGenie/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── gemini_client.py
│   ├── explanation_module.py
│   ├── qna.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   ├── learning_path.py
│   ├── schemas.py
│   └── main.py
├── templates/index.html
├── static/style.css
├── static/app.js
├── tests/test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-local.txt
└── README.md
```

## 1. VS Code setup

Install Python 3.10+ and open this folder in VS Code. In the VS Code terminal:

### Windows

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Select the `.venv` interpreter in VS Code: `Ctrl+Shift+P` → `Python: Select Interpreter`.

## 2. Configure Gemini

Copy `.env.example` to `.env` and put your Google AI Studio API key in `GEMINI_API_KEY`.

Do not commit `.env` to Git. The application reads the key from the environment and never sends it to the browser.

## 3. Run

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 4. Test

Run automated tests:

```bash
pytest -q
```

The tests validate routing, input validation, health reporting, and the application UI without making live Gemini calls.

For live functional testing, open the web page and test each task:

1. Ask a question — e.g. `Which is the largest ocean?`
2. Explain a topic — e.g. `Explain photosynthesis.`
3. Generate a quiz — paste a short educational passage.
4. Summarize — paste a paragraph or longer passage.
5. Learning path — enter a topic such as `SQL` and choose a level.

## Optional local LaMini explanation model

The supplied documentation proposes LaMini-Flan-T5-783M for concept explanation. To enable that path:

```bash
pip install -r requirements-local.txt
```

Then set:

```env
USE_LOCAL_EXPLAINER=true
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local-model request may download model files and requires more disk space/RAM. The default configuration uses Gemini for explanations so the application is much simpler to install.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"What is photosynthesis?\"}"
```

On macOS/Linux, replace `^` with `\\` for line continuation or put the command on one line.

### Quiz

```json
POST /quiz
{
  "text": "Photosynthesis converts light energy into chemical energy in plants.",
  "count": 3
}
```

## Notes about the documentation

The supplied document lists Gemini 1.5 Pro and an older-style model/API description. Google recommends the newer Google GenAI SDK (`google-genai`) rather than the legacy `google-generativeai` library. The app therefore keeps the requested architecture and capabilities while making the model name configurable through `GEMINI_MODEL`.
