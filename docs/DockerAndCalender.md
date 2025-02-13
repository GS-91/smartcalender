# Docker und Google Calendar – Komplettanleitung

Diese Anleitung beschreibt Schritt für Schritt, wie du die SmartCalendar-App mit Docker startest und anschließend einen Kalendereintrag mit der API erstellst.

## 1. Voraussetzungen
Bevor du loslegst, stelle sicher, dass du folgende Dinge installiert hast:

- Docker (https://docs.docker.com/get-docker/)
- Git (https://git-scm.com/downloads)
- Python 3.9+ (falls du lokal testen willst)
- Google API-Zugangsdaten (credentials.json muss vorliegen)
- Ein Google-Konto mit Google Calendar API aktiviert

## 2. Repository klonen und in das Projektverzeichnis wechseln
Falls du das Repository noch nicht hast, klone es zuerst:

```bash
git clone https://github.com/dein-repo/DevOpsKalenderProjekt.git
cd DevOpsKalenderProjekt
```

Falls du bereits das Repository hast, stelle sicher, dass du im Projektverzeichnis bist:

```bash
cd "/Users/ivanappl/DevOpsKalenderProjekt"
git pull origin main
```

## 3. Docker-Container starten
Baue und starte die Anwendung mit Docker:

```bash
docker-compose -f infra/docker-compose.yml up --build -d
```

Überprüfe, ob der Container läuft:

```bash
docker ps
```

Falls du ihn stoppen möchtest:

```bash
docker-compose down
```

## 4. Überprüfen, ob die API läuft
Führe diesen Befehl aus, um zu prüfen, ob die API erreichbar ist:

```bash
curl http://localhost:8000/
```

Erwartete Ausgabe:

```json
{"message":"API läuft!"}
```

Falls die API nicht erreichbar ist, prüfe die Logs:

```bash
docker logs smartcalendar-api
```

## 5. Google Calendar API testen
Erstelle einen Kalendereintrag über die API:

```bash
curl -X POST http://localhost:8000/calendar/create_event/ \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Docker Meeting",
           "date": "2025-02-12",
           "time": "10:00",
           "description": "Besprechung über das Docker-Projekt",
           "user_input": "Gabriel Simon",
           "day": "WE",
           "duration": "60",
           "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=WE"]
         }'
```

## 6. Alle Schritte in einem Skript automatisieren
Falls du alle Schritte mit nur einem Befehl erledigen willst, kannst du das folgende Skript verwenden:

Speichere es als **setup_and_create_event.sh** und führe es aus:

```bash
#!/bin/bash

# Projektverzeichnis definieren
PROJECT_DIR="/Users/ivanappl/DevOpsKalenderProjekt"
DOCKER_COMPOSE_FILE="infra/docker-compose.yml"

# Google Calendar API Event-Daten
EVENT_TITLE="Docker Meeting"
EVENT_DATE="2025-02-12"
EVENT_TIME="10:00"
EVENT_DESCRIPTION="Besprechung über das Docker-Projekt"
USER_INPUT="Gabriel Simon"
DAY="WE"
DURATION="60"
RECURRENCE="RRULE:FREQ=WEEKLY;BYDAY="

# Sicherstellen, dass sich das Skript im richtigen Verzeichnis befindet
cd "/Users/ivanappl/DevOpsKalenderProjekt" || { echo "Fehler: Projektverzeichnis nicht gefunden!"; exit 1; }

# Neueste Version vom Repository abrufen
echo "Aktualisiere das Repository..."
git pull origin main

# Docker-Container neu starten
echo "Starte Docker-Container..."
docker-compose -f "" down
docker-compose -f "" up --build -d

# Prüfen, ob API läuft
echo "Überprüfe, ob die API läuft..."
sleep 5  # Warte, bis der Container hochgefahren ist
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)

if [ "$API_STATUS" -ne 200 ]; then
    echo "Fehler: API nicht erreichbar. Überprüfe die Docker-Logs."
    docker logs smartcalendar-api
    exit 1
fi

echo "API läuft erfolgreich!"

# Kalendereintrag erstellen
echo "Erstelle einen Google-Kalendereintrag..."
RESPONSE=$(curl -s -X POST http://localhost:8000/calendar/create_event/ \
    -H "Content-Type: application/json" \
    -d "{
          \"title\": \"\",
          \"date\": \"\",
          \"time\": \"\",
          \"description\": \"\",
          \"user_input\": \"\",
          \"day\": \"\",
          \"duration\": \"\",
          \"recurrence\": [\"\"]
        }")

echo "API Antwort:"
echo "$RESPONSE"

# Erfolg prüfen
if echo "$RESPONSE" | grep -q "message"; then
    echo "Kalendereintrag erfolgreich erstellt!"
fi
```

## 7. GitHub-Update – Datei pushen
Führe die folgenden Befehle aus, um die Datei ins Repository hochzuladen:

```bash
git add docs/DockerAndCalender.md
git commit -m "Added Docker and Calendar documentation"
git push origin main
```
