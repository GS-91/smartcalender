# Ordnerstruktur erstellen
import os

folders = [
    "app/api", "app/ui", "app/utils", "config", "tests", "infra/k8s", "infra/terraform", "scripts", "docs"
]

files = {
    "app/main.py": "# Haupt-Entry für die FastAPI-App\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {\"message\": \"API läuft!\"}\n",
    "app/api/calendar_api.py": "# Google Calendar API-Funktionen\ndef create_calendar_event():\n    pass",
    "app/api/openai_api.py": "# OpenAI API-Funktionen\ndef generate_funny_response():\n    pass",
    "app/utils/speech.py": "# Text-to-Speech-Funktion\ndef speak(text):\n    pass",
    "infra/Dockerfile": "# Dockerfile für die App\nFROM python:3.9\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
    "infra/docker-compose.yml": "version: '3.8'\nservices:\n  api:\n    build: .\n    ports:\n      - \"8000:8000\"",
    "infra/k8s/deployment.yaml": "# Kubernetes Deployment\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: devops-calendar-api\nspec:\n  replicas: 2\n  selector:\n    matchLabels:\n      app: devops-calendar\n  template:\n    metadata:\n      labels:\n        app: devops-calendar\n    spec:\n      containers:\n      - name: api\n        image: devops-calendar:latest\n        ports:\n        - containerPort: 8000",
    "tests/test_api.py": "# Tests für API\ndef test_dummy():\n    assert True",
    "scripts/deploy.sh": "#!/bin/bash\necho 'Deployment-Skript wird noch implementiert.'",
    "docs/README.md": "# DevOps Kalender Projekt\nDies ist eine FastAPI-basierte Kalender-App mit DevOps-Integration."
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

print("Projektstruktur erfolgreich erstellt!")
