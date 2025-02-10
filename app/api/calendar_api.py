import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from openai import OpenAI

# Google Calendar API-Berechtigungen
SCOPES = ['https://www.googleapis.com/auth/calendar']

# OpenAI-API-Schlüssel aus Datei laden
def load_api_key():
    try:
        with open("api_key.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Die Datei 'api_key.txt' wurde nicht gefunden. Bitte füge dort deinen API-Schlüssel ein.")

api_key = load_api_key()
client = OpenAI(api_key=api_key)

def generate_funny_title(user_input):
    """Generiert einen lustigen und kreativen Titel für den Termin mit OpenAI."""
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
    """Erstellt einen Termin in Google Kalender mit einem lustigen Titel."""
    
    # Korrekte Pfade für Token- und Credentials-Dateien
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_file = os.path.join(script_dir, "token.json")
    credentials_file = os.path.join(script_dir, "credentials.json")

    creds = None

    # **DEBUGGING: Pfade ausgeben**
    print("\n--- DEBUG: Datei-Pfade ---")
    print(f"Token-Pfad: {token_file}")
    print(f"Credentials-Pfad: {credentials_file}")

    # **Prüfen, ob der Token existiert, ansonsten neu authentifizieren**
    if os.path.exists(token_file):
        print("\n--- DEBUG: Token-Datei gefunden. Lade Credentials... ---")
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        print("\n--- DEBUG: Token nicht gefunden. Starte neue Authentifizierung... ---")
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    # Google Calendar API-Dienst aufbauen
    service = build('calendar', 'v3', credentials=creds)

    # Lustigen Titel generieren
    summary = generate_funny_title(user_input)

    # **Zeitformatierung**
    start_datetime = datetime.strptime(f'2024-12-11T{time}:00', '%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + timedelta(hours=duration)

    # **DEBUGGING: Event-Daten ausgeben**
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Berlin',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;BYDAY={day.upper()}',
        ],
    }

    print("\n--- DEBUG: Event-Daten ---")
    print(event)

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()

        # **DEBUGGING: API-Antwort ausgeben**
        print("\n--- DEBUG: Google API Response ---")
        print(event_result)

        return {
            "message": f"Termin '{summary}' am {day} um {time} für {duration} Stunden erstellt!",
            "link": event_result.get('htmlLink', 'Kein Link verfügbar')
        }
    except Exception as e:
        print("\n--- DEBUG: Fehler beim Erstellen des Termins ---")
        print(str(e))
        return {"error": f"Fehler beim Erstellen des Termins: {e}"}
