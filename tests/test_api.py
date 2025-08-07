# tests/test_api.py
from fastapi.testclient import TestClient
from app import app
from Pydantic_dir.pydantic_valid_classes import LongUrl

client = TestClient(app)


def test_ping_endpoint():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"Ping": "ok"}


def test_create_short_url_valid():
    response = client.post(
        "/get_short",
        json={"url": "https://example.com"}
    )
    assert response.status_code == 201
    assert "short_url" in response.json()
    assert response.json()["short_url"].startswith("https://localhost:8003/red/")


def test_create_short_url_invalid():
    response = client.post(
        "/get_short",
        json={"url": "not_a_url"}
    )
    assert response.status_code == 400
    assert "error" in response.json()


def test_redirect_valid(mocker):
    # Мокируем функцию get_long_link
    mocker.patch("app.get_long_link", return_value=LongUrl(url="https://example.com"))

    response = client.get("/red/abc123", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"


def test_redirect_invalid():
    response = client.get("/red/invalid_id")
    assert response.status_code == 404