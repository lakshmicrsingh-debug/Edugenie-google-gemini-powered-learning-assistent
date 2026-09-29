from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_qa_rejected():
    response = client.post("/qa", json={"text": "   "})
    assert response.status_code == 422


def test_quiz_count_validation():
    response = client.post("/quiz", json={"text": "Photosynthesis", "count": 11})
    assert response.status_code == 422


def test_learning_path_validation():
    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "beginner", "hours_per_week": 0},
    )
    assert response.status_code == 422
