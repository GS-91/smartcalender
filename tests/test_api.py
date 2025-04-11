from app.api import calendar_api


def test_generate_funny_title(monkeypatch):
    class DummyResponse:
        class DummyChoices:
            message = type("obj", (object,), {"content": "🦄 Testtitel"})

        choices = [DummyChoices()]

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        class chat:
            class completions:
                @staticmethod
                def create(model, messages):
                    return DummyResponse()

    monkeypatch.setattr(calendar_api, "client", DummyClient())
    result = calendar_api.generate_funny_title("Test")
    assert "Testtitel" in result
