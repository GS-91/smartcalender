from fastapi.testclient import TestClient
import app.main as main  # Damit monkeypatch wirkt

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API läuft!"}


def test_create_event(monkeypatch):
    def dummy_event(user_input, day, time, duration):
        return {
            "message": "Dummy-Termin erstellt",
            "link": "http://example.com"
        }

    monkeypatch.setattr(main, "create_calendar_event", dummy_event)

    response = client.post(
        "/calendar/create_event/",
        json={
            "user_input": "Testmeeting",
            "day": "MO",
            "time": "10:00",
            "duration": 1
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Dummy-Termin erstellt"


def test_list_events(monkeypatch):
    def dummy_list(*args, **kwargs):
        return {
            "items": [
                {
                    "summary": "Dummy Event",
                    "start": {"dateTime": "2024-12-11T10:00:00"},
                    "end": {"dateTime": "2024-12-11T11:00:00"},
                }
            ]
        }

    monkeypatch.setattr(
        main,
        "get_calendar_service",
        lambda: type("DummyService", (), {
            "events": lambda self=None: type(
                "obj", (),
                {"list": lambda *a, **kw: type(
                    "r", (), {"execute": dummy_list}
                )()}
            )
        })()
    )

    response = client.get("/calendar/list_events/")
    assert response.status_code == 200
    assert "events" in response.json()
    assert response.json()["events"][0]["summary"] == "Dummy Event"


def test_list_calendars(monkeypatch):
    def dummy_calendars(*args, **kwargs):
        return {
            "items": [
                {
                    "id": "test-calendar-id",
                    "summary": "Test Kalender",
                    "timeZone": "Europe/Berlin"
                }
            ]
        }

    monkeypatch.setattr(
        main,
        "get_calendar_service",
        lambda: type("DummyService", (), {
            "calendarList": lambda self=None: type(
                "obj", (),
                {"list": lambda *a, **kw: type(
                    "r", (), {"execute": dummy_calendars}
                )()}
            )
        })()
    )

    response = client.get("/calendar/list_calendars/")
    assert response.status_code == 200
    assert "calendars" in response.json()
    assert response.json()["calendars"][0]["id"] == "test-calendar-id"
