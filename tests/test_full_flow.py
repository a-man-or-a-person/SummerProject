# tests/test_full_flow.py
import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@pytest.mark.integration
def test_full_url_flow():
    # Шаг 1: Создание короткой ссылки
    response = client.post("/get_short", json={"url": "https://integration-test.com"})
    assert response.status_code == 201
    short_url = response.json()["short_url"]
    short_id = short_url.split("/")[-1]

    # Шаг 2: Редирект по короткой ссылке
    response = client.get(f"/red/{short_id}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://integration-test.com"
