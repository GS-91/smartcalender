from fastapi import FastAPI
from pydantic import BaseModel
from app.api.calendar_api import create_calendar_event
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

app = FastAPI()

# Schema für die JSON-Eingabe
class EventRequest(BaseModel):
    user_input: str
    day: str
    time: str
    duration: int

# Google Calendar API-Berechtigungen
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "app", "credentials.json")

def get_calendar_service():
    """Erstellt eine Verbindung zur Google Calendar API mit dem Service Account."""
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

@app.get("/")
def read_root():
    return {"message": "API läuft!"}

@app.post("/calendar/create_event/")
def create_event(event: EventRequest):
    """Endpoint zum Erstellen eines Google Calendar Events."""
    return create_calendar_event(event.user_input, event.day, event.time, event.duration)

@app.get("/calendar/list_events/")
def list_events():
    """Listet alle Kalendereinträge im primären Kalender auf."""
    try:
        service = get_calendar_service()
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get("items", [])
        event_list = []
        for event in events:
            event_list.append({
                "summary": event.get("summary", "Kein Titel"),
                "start": event.get("start", {}).get("dateTime", "Keine Startzeit"),
                "end": event.get("end", {}).get("dateTime", "Keine Endzeit"),
            })
        return {"events": event_list}
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der Kalendereinträge: {str(e)}"}

@app.get("/calendar/list_calendars/")
def list_calendars():
    """Listet alle verfügbaren Kalender des Google-Accounts auf."""
    try:
        service = get_calendar_service()
        calendar_list = service.calendarList().list().execute()
        calendars = []
        for calendar in calendar_list.get("items", []):
            calendars.append({
                "id": calendar["id"],
                "summary": calendar.get("summary", "Kein Titel"),
                "timeZone": calendar.get("timeZone", "Unbekannte Zeitzone")
            })
        return {"calendars": calendars}
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der Kalenderliste: {str(e)}"}
