# Docker-Guide

## 1. Was ist Docker?
Docker ist wie ein magischer Behälter für deine Anwendung.  
Er packt alle nötigen Zutaten (deinen Code, Bibliotheken, Einstellungen) in einen Container.  
So läuft deine Anwendung überall gleich – egal, ob auf deinem Laptop, in der Cloud oder auf einem anderen Computer.

## 2. Was macht ein Dockerfile?
Das Dockerfile ist wie ein Kochrezept, das Docker sagt, wie der Container gebaut werden soll.

```dockerfile
# Verwende das offizielle Python-Image als Grundlage
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container auf /app
WORKDIR /app

# Kopiere zuerst die Datei "requirements.txt", um die Abhängigkeiten zu installieren
COPY requirements.txt .

# Installiere alle benötigten Bibliotheken
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Quellcode in das Arbeitsverzeichnis im Container
COPY . .

# Setze eine Umgebungsvariable, damit Python weiß, wo es nach Modulen suchen soll
ENV PYTHONPATH=/app

# Starte die Anwendung mit Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Erklärung der Schritte:
- **FROM python:3.9** → Basis-Image für Python 3.9  
- **WORKDIR /app** → Das Hauptverzeichnis im Container  
- **COPY requirements.txt .** → Kopiert die Abhängigkeiten  
- **RUN pip install -r requirements.txt** → Installiert benötigte Bibliotheken  
- **COPY . .** → Kopiert den gesamten Code in den Container  
- **ENV PYTHONPATH=/app** → Definiert den Suchpfad für Python-Module  
- **CMD ["uvicorn", "main:app", ...]** → Startet die FastAPI-Anwendung  

## 3. Was ist Docker Compose?
Docker Compose hilft uns, Container einfacher zu starten, zu stoppen und zu verwalten.

```yaml
version: '3.8'

services:
  api:
    build:
      context: /Users/ivanappl/DevOpsKalenderProjekt
      dockerfile: Dockerfile
    container_name: smartcalendar-api
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
    volumes:
      - /Users/ivanappl/DevOpsKalenderProjekt:/app  # Kopiert das ganze Projekt ins Containerverzeichnis /app
    restart: always
```

## 4. Docker und Docker Compose nutzen

### **A. Docker-Befehle**
**Image bauen:**
```bash
docker build --no-cache -t smartcalendar-api .
```

**Container starten:**
```bash
docker run -d -p 8000:8000 --name smartcalendar-api smartcalendar-api
```

**Container stoppen & entfernen:**
```bash
docker stop smartcalendar-api
docker rm smartcalendar-api
```

**Logs ansehen:**
```bash
docker logs smartcalendar-api
```

### **B. Docker Compose Befehle**
**Container (Service) mit Compose starten:**
```bash
docker-compose -f infra/docker-compose.yml up --build -d
```

**Container (Service) stoppen:**
```bash
docker-compose -f infra/docker-compose.yml down
```

## 5. Zusammenfassung
- Docker erstellt **Container**, in denen deine Anwendung isoliert läuft.  
- Das **Dockerfile** ist das Rezept für den Container.  
- **Docker Compose** erleichtert das Starten und Verwalten von Containern, besonders für komplexe Setups.  

Mit diesen Tools stellst du sicher, dass deine Anwendung überall gleich läuft! 🚀
