# Verwende das offizielle Python-Image
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere nur die requirements.txt zuerst, um Caching zu nutzen
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Code ins Containerverzeichnis /app
#COPY . .  # <— Kommentar wurde außerhalb der Codezeile gesetzt
COPY . /app


# Starte die FastAPI-Anwendung mit Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
