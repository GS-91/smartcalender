# Ordnerstruktur erstellen
import os

folders = [
    "app/api",
    "app/ui",
    "app/utils",
    "config",
    "tests",
    "infra/k8s",
    "infra/terraform",
    "scripts",
    "docs",
]

files = {
    "app/main.py": (
        '# Haupt-Entry für die FastAPI-App\n'
        'from fastapi import FastAPI\n\n'
        'app = FastAPI()\n\n'
        '@app.get("/")\ndef read_root():\n'
        '    return {"message": "API läuft!"}\n'
    ),
    "app/api/calendar_api.py": (
        "# Google Calendar API-Funktionen\n\n"
        "def create_calendar_event():\n"
        "    pass\n"
    ),
    "app/api/openai_api.py": (
        "# OpenAI API-Funktionen\n\n"
        "def generate_funny_response():\n"
        "    pass\n"
    ),
    "app/utils/speech.py": (
        "# Text-to-Speech-Funktion\n\n"
        "def speak(text):\n"
        "    pass\n"
    ),
    "infra/Dockerfile": (
        '# Dockerfile für die App\n'
        'FROM python:3.9\n'
        'WORKDIR /app\n'
        'COPY requirements.txt .\n'
        'RUN pip install -r requirements.txt\n'
        'COPY . .\n'
        'CMD [\n'
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
        ']\n'
    ),
    "infra/docker-compose.yml": (
        "version: '3.8'\n"
        "services:\n"
        "  api:\n"
        "    build: .\n"
        "    ports:\n"
        "      - \"8000:8000\"\n"
    ),
    "infra/k8s/deployment.yaml": (
        "# Kubernetes Deployment\n"
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: devops-calendar-api\n"
        "spec:\n"
        "  replicas: 2\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: devops-calendar\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: devops-calendar\n"
        "    spec:\n"
        "      containers:\n"
        "      - name: api\n"
        "        image: devops-calendar:latest\n"
        "        ports:\n"
        "        - containerPort: 8000\n"
    ),
    "tests/test_api.py": (
        "# Tests für API\n\n"
        "def test_dummy():\n"
        "    assert True\n"
    ),
    "scripts/deploy.sh": (
        "#!/bin/bash\n"
        "echo 'Deployment-Skript wird noch implementiert.'\n"
    ),
    "docs/README.md": (
        "# DevOps Kalender Projekt\n"
        "Dies ist eine FastAPI-basierte Kalender-App mit DevOps-Integration.\n"
    ),
}

# Ordnerstruktur erstellen
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Dateien erstellen
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

print("Projektstruktur erfolgreich erstellt!")
