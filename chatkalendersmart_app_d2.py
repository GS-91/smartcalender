import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from openai import OpenAI
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import pyttsx3

# OpenAI-API-Schlüssel aus Datei laden
def load_api_key():
    try:
        with open("api_key.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Die Datei 'api_key.txt' wurde nicht gefunden. Bitte füge dort deinen API-Schlüssel ein.")

api_key = load_api_key()

# OpenAI-Client erstellen
client = OpenAI(api_key=api_key)

# Google Calendar API-Berechtigungen
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_calendar_event(summary, day, time, duration):
    """Erstellt einen wiederkehrenden Termin in Google Kalender."""
    creds = None
    token_file = 'token.json'

    # Authentifizierung für Google Calendar
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Zeitberechnung mit Mitternacht-Korrektur
    start_time = f'2024-12-11T{time}:00'
    start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + timedelta(hours=duration)

    # Endzeit berechnen und Korrektur für nächsten Tag
    if end_datetime.day > start_datetime.day:
        end_date_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    else:
        end_date_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # Erstellen des Termins
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': end_date_str,
            'timeZone': 'Europe/Berlin',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;BYDAY={day.upper()}',
        ],
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return event_result['htmlLink']
    except Exception as e:
        return f"Fehler beim Erstellen des Termins: {e}"


# Funktion zur Sprachausgabe
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Funktion zur Generierung von humorvollen Antworten durch ChatGPT
def generate_funny_response(user_input):
    prompt = f"Erstelle eine humorvolle, freche und übermütige Antwort (aber nur maximal 3 sätze lang) auf den folgenden Google Kalender Termin: {user_input}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        funny_response = response.choices[0].message.content.strip()
    except Exception:
        funny_response = "Ups! Etwas lief schief. Versuch es noch einmal."

    return funny_response


# Funktion zum Parsen der Nutzereingabe
def parse_input(user_input):
    days_mapping = {
        "montag": "MO",
        "dienstag": "TU",
        "mittwoch": "WE",
        "donnerstag": "TH",
        "freitag": "FR",
        "samstag": "SA",
        "sonntag": "SU",
    }

    # Wochentag und Uhrzeit extrahieren
    day = next((days_mapping[day] for day in days_mapping if day in user_input.lower()), None)
    time = None
    duration = 1  # Standarddauer
    words = user_input.lower().split()
    for i, word in enumerate(words):
        if word == "uhr" and i > 0:
            time = words[i - 1]
            if ":" not in time:
                time = f"{time}:00"
        if "stunde" in word or "stunden" in word:  # Wenn "Stunde" oder "Stunden" im Wort enthalten ist
            try:
                duration = int(words[i - 1])  # Die Zahl vor "Stunden" wird als Dauer genommen
            except ValueError:
                duration = 1

    # Titel generieren mit GPT
    prompt = f"Erstelle einen kurzen und passenden Titel basierend auf der Aktivität: '{user_input}'"
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()
    except Exception:
        summary = "Aktivität"

    return day, time, duration, summary


# Kivy UI erstellen
class CalendarApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Was möchten Sie tun?", size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        self.text_input = TextInput(hint_text="Geben Sie Ihre Anfrage ein", size_hint=(1, 0.1), multiline=False)
        self.layout.add_widget(self.text_input)

        self.button = Button(text="Erstellen", size_hint=(1, 0.1))
        self.button.bind(on_press=self.on_button_press)
        self.layout.add_widget(self.button)

        # ScrollView für das Antwortfeld
        self.result_label = Label(text="", size_hint=(1, None))
        self.result_label.height = 300  # Höhe des Textbereichs anpassen
        self.scrollview = ScrollView(size_hint=(1, 0.6))
        self.scrollview.add_widget(self.result_label)
        self.layout.add_widget(self.scrollview)

        return self.layout

    def on_button_press(self, instance):
        user_input = self.text_input.text.strip()
        if user_input:
            day, time, duration, summary = parse_input(user_input)
            if day and time:
                link = create_calendar_event(summary, day, time, duration)
                # Generiere eine freche Antwort basierend auf der Eingabe
                funny_response = generate_funny_response(user_input)
                self.result_label.text = f"{funny_response}\n\nTermin-Link: {link}"
                speak(funny_response)  # Sprachausgabe
            else:
                self.result_label.text = "Oh, das habe ich nicht verstanden. Könntest du die Dauer oder die Details nochmal angeben? 😊"
                speak("Ups, das habe ich nicht ganz verstanden. Kannst du die Details nochmal angeben?")
        else:
            self.result_label.text = "Bitte gebe eine gültige Anfrage ein."


if __name__ == "__main__":
    CalendarApp().run()
