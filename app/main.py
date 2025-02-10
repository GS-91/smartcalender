from fastapi import FastAPI
from pydantic import BaseModel
from app.api.calendar_api import create_calendar_event

app = FastAPI()

# Definiere das Schema für die JSON-Eingabe
class EventRequest(BaseModel):
    user_input: str
    day: str
    time: str
    duration: int

@app.get("/")
def read_root():
    return {"message": "API läuft!"}

@app.post("/calendar/create_event/")
def create_event(event: EventRequest):
    """FastAPI Endpoint zum Erstellen eines Google Calendar Events."""
    return create_calendar_event(event.user_input, event.day, event.time, event.duration)
