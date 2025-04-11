import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from openai import OpenAI

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "/app/app/api/credentials.json"


def load_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not set in environment.")
    return api_key


def get_openai_client():
    return OpenAI(api_key=load_api_key())


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)


def generate_funny_title(user_input):
    prompt = (
        f'Erstelle einen lustigen Titel für: "{user_input}". '
        "Maximal 10 Wörter, übertrieben & spaßig."
    )
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Super geheimer Top-Manager-Termin"


def create_calendar_event(user_input, day, time, duration):
    summary = generate_funny_title(user_input)
    start_str = f"2024-12-11T{time}:00"
    start_datetime = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S")
    end_datetime = start_datetime + timedelta(hours=duration)

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Berlin",
        },
        "end": {
            "dateTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Berlin",
        },
        "recurrence": [f"RRULE:FREQ=WEEKLY;BYDAY={day.upper()}"],
    }

    try:
        service = get_calendar_service()
        event_result = (
            service.events()
            .insert(calendarId="91gabriel.simon@gmail.com", body=event)
            .execute()
        )
        return {
            "message": (
                f"Termin '{summary}' am {day} um {time} "
                f"für {duration} Stunden erstellt!"
            ),
            "link": event_result.get("htmlLink", "Kein Link verfügbar"),
        }
    except Exception as e:
        return {"error": f"Fehler beim Erstellen des Termins: {e}"}
