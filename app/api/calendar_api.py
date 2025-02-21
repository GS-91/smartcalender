import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from openai import OpenAI

# Google Calendar API-Berechtigungen
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "/app/app/api/credentials.json"  # Pfad innerhalb des Containers

def load_api_key():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "api_key.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception(f"File '{file_path}' not found. Please ensure it's present.")

api_key = load_api_key()
client = OpenAI(api_key=api_key)

# Service Account Credentials laden – interaktiver OAuth-Flow wird NICHT verwendet!
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Google Calendar API-Dienst aufbauen
service = build("calendar", "v3", credentials=creds)

def generate_funny_title(user_input):
    """Generiert einen lustigen, kreativen Titel für den Termin mithilfe von OpenAI."""
    prompt = f"""
    Erstelle einen lustigen, kreativen und ausgefallenen Titel für einen Kalendereintrag basierend auf dieser Beschreibung: "{user_input}".
    Der Titel soll maximal 10 Wörter lang sein und sich anhören wie eine spaßige oder übertriebene Event-Beschreibung.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        title = response.choices[0].message.content.strip()
    except Exception:
        title = "Super geheimer Top-Manager-Termin"
    return title

def create_calendar_event(user_input, day, time, duration):
    """Erstellt einen Termin im Google Kalender mit einem lustigen Titel."""
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
        "recurrence": [
            f"RRULE:FREQ=WEEKLY;BYDAY={day.upper()}",
        ],
    }
    
    print("\n--- DEBUG: Event-Daten ---")
    print(event)
    
    try:
        # Termin im gewünschten Kalender (z. B. Deinem Gmail-Kalender) einfügen:
        event_result = service.events().insert(calendarId="91gabriel.simon@gmail.com", body=event).execute()
        print("\n--- DEBUG: Google API Response ---")
        print(event_result)
        return {
            "message": f"Termin '{summary}' am {day} um {time} für {duration} Stunden erstellt!",
            "link": event_result.get("htmlLink", "Kein Link verfügbar")
        }
    except Exception as e:
        print("\n--- DEBUG: Fehler beim Erstellen des Termins ---")
        print(str(e))
        return {"error": f"Fehler beim Erstellen des Termins: {e}"}
