import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from openai import OpenAI

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__), "credentials.json"
)


def load_api_key():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "api_key.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception(f"File '{file_path}' not found.")


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)


api_key = load_api_key()
client = OpenAI(api_key=api_key)


def generate_funny_title(user_input):
    prompt = (
        f"Erstelle einen lustigen, kreativen Titel für: \"{user_input}\". "
        "Max. 10 Wörter, spaßig und übertrieben."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Super geheimer Top-Manager-Termin"


def create_calendar_event(user_input, day, time, duration):
    summary = generate_funny_title(user_input)
    start_datetime = datetime.strptime(f"2024-12-11T{time}:00", "%Y-%m-%dT%H:%M:%S")
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
        result = service.events().insert(calendarId="primary", body=event).execute()
        return {
            "message": f"Termin '{summary}' erstellt!",
            "link": result.get("htmlLink", "Kein Link verfügbar"),
        }
    except Exception as e:
        return {"error": str(e)}
