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

    # 👉 monkeypatch auf die Funktion statt auf das Modulattribut
    monkeypatch.setattr(
        calendar_api, "get_openai_client", lambda: DummyClient()
    )
    result = calendar_api.generate_funny_title("Testmeeting")
    assert result == "🦄 Testtitel"
