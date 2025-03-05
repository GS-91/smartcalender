SmartCalendar – DevOps-Kalender mit Google API & FastAPI
Übersicht
SmartCalendar ist eine FastAPI-Anwendung zur Verwaltung von Google-Kalendereinträgen.

Funktionen:
Erstellen von Terminen
Auflisten von Kalendereinträgen
Humorvolle Event-Titel via OpenAI
Installation
1. Lokales Setup
bash
Kopieren
Bearbeiten
git clone https://github.com/GS-91/smartcalender.git
cd smartcalender
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Die API ist erreichbar unter: http://localhost:8000/

2. Docker Setup
bash
Kopieren
Bearbeiten
docker-compose -f infra/docker-compose.yml up --build -d
API Endpunkte
GET / → API-Status
POST /calendar/create_event/ → Neuen Termin erstellen
GET /calendar/list_events/ → Termine abrufen
GET /calendar/list_calendars/ → Google-Kalender abrufen
Beispiel für einen API-Request:

json
Kopieren
Bearbeiten
{
  "user_input": "Team Meeting",
  "day": "WE",
  "time": "10:00",
  "duration": 2
}
Autor
Gabriel Simon | GitHub: GS-91
