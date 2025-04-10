from fastapi.testclient import TestClient
from app.main import app
from app.api import openai_api
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_openai_client(monkeypatch):
    class DummyResponse:
        class DummyChoices:
            message = type("obj", (object,), {"content": "😄 Witzige Antwort"})

        choices = [DummyChoices()]

    class DummyClient:
        class chat:
            class completions:
                @staticmethod
                def create(model, messages):
                    return DummyResponse()

    monkeypatch.setattr(openai_api, "client", DummyClient())

def test_generate_funny_response():
    response = client.post("/generate_funny_response/", params={"event_text": "Test"})
    assert response.status_code == 200
    assert "response" in response.json()