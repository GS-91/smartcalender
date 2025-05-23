from fastapi.testclient import TestClient
from app.main import app
from app.api import openai_api


def test_generate_funny_response(monkeypatch):
    class DummyResponse:
        class DummyChoices:
            message = type(
                "obj",
                (object,),
                {"content": "🧪 Testantwort"},
            )

        choices = [DummyChoices()]

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        class chat:
            class completions:
                @staticmethod
                def create(model, messages):
                    return DummyResponse()

    monkeypatch.setattr(openai_api, "load_api_key", lambda: "test-key")
    monkeypatch.setattr(openai_api, "OpenAI", lambda api_key: DummyClient())

    client = TestClient(app)
    response = client.post(
        "/generate_funny_response/",
        json={"event_text": "Beispieltext"},
    )
    assert response.status_code == 200
    assert "🧪 Testantwort" in response.json()["response"]
