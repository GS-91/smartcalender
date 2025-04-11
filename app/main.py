import os
from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.api.calendar_api import create_calendar_event
from app.api import openai_api

app = FastAPI()


class EventRequest(BaseModel):
    user_input: str
    day: str
    time: str
    duration: int


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__), "app", "credentials.json"
)


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)


@app.get("/")
def read_root():
    return {"message": "API läuft!"}


@app.post("/calendar/create_event/")
def create_event(event: EventRequest):
    return create_calendar_event(
        event.user_input,
        event.day,
        event.time,
        event.duration
    )


@app.get("/calendar/list_events/")
def list_events():
    try:
        service = get_calendar_service()
        result = service.events().list(
            calendarId="primary",
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = result.get("items", [])
        event_list = []
        for e in events:
            event_list.append({
                "summary": e.get("summary", "Kein Titel"),
                "start": e.get("start", {}).get("dateTime", "Keine Startzeit"),
                "end": e.get("end", {}).get("dateTime", "Keine Endzeit"),
            })
        return {"events": event_list}
    except Exception as e:
        return {"error": f"Fehler beim Abrufen: {str(e)}"}


@app.get("/calendar/list_calendars/")
def list_calendars():
    try:
        service = get_calendar_service()
        calendars = service.calendarList().list().execute().get("items", [])
        calendar_list = []
        for c in calendars:
            calendar_list.append({
                "id": c["id"],
                "summary": c.get("summary", "Kein Titel"),
                "timeZone": c.get("timeZone", "Unbekannte Zeitzone"),
            })
        return {"calendars": calendar_list}
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der Kalender: {str(e)}"}


# 🔥 Wichtig: Router für OpenAI-Funktionalität hinzufügen
app.include_router(openai_api.router)
