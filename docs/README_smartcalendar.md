# Smart Calendar – Projektdokumentation

## 1. Projektübersicht

Das Projekt „Smart Calendar“ bietet eine API zur automatisierten Erstellung von Kalendereinträgen mit humorvollen Titeln auf Basis von Nutzereingaben. Die Anwendung kombiniert Google Calendar mit OpenAI, um Termine automatisiert zu planen und zu beschreiben. Ziel ist es, Nutzern das Terminmanagement auf unterhaltsame Weise zu erleichtern.

## 2. Systemarchitektur

Die Anwendung besteht aus folgenden Komponenten:

- Eine FastAPI-basierte Python-Anwendung, die die Business-Logik kapselt
- Ein Google Calendar API-Zugriff mittels Service Account (ohne OAuth-Interaktion)
- Eine Anbindung an OpenAI zur Generierung kreativer Texte
- Docker-Containerisierung für einheitliche Ausführung in jeder Umgebung
- CI/CD Pipelines zur Sicherstellung von Codequalität und automatischem Deployment
- Eine AWS-Infrastruktur mit ECS Fargate, ECR und Terraform

## 3. Lokale Entwicklung

### Voraussetzungen

- Python 3.10 oder höher
- Virtualenv oder venv
- Docker (optional)
- Zugriff auf `api_key.txt` und `credentials.json` für OpenAI bzw. Google Calendar

### Setup

```bash
# 1. Projekt klonen
git clone https://github.com/GS-91/smartcalender.git
cd smartcalender

# 2. Virtuelle Umgebung erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
pip install -r requirements-dev.txt  # für Tests und Linting

# 4. Entwicklungsserver starten
uvicorn app.main:app --reload
```

### Dateistruktur

```
smartcalender/
│
├── app/                     # Applikationslogik (FastAPI)
│   ├── api/                 # API-Endpunkte
│   └── main.py              # FastAPI Application Entry Point
│
├── tests/                  # Unit Tests
├── Dockerfile              # Container Build Definition
├── .github/workflows/      # CI/CD Workflows
└── infra/terraform/        # Infrastrukturdefinition für AWS
```

## 4. CI/CD Pipeline

Die GitHub Actions Workflow-Datei `.github/workflows/ci-quality-check.yml` sorgt bei jedem Commit oder Pull Request für automatische Prüfungen. Sie enthält folgende Schritte:

### Code-Qualität und Sicherheit

1. **Linting mit flake8**  
   Prüft den Code-Stil auf Basis des PEP8-Standards.

2. **Unittests mit pytest**  
   Führt automatisierte Tests im Verzeichnis `tests/` aus.

3. **Security Scan mit Bandit**  
   Sucht nach sicherheitskritischen Stellen im Python-Code.

### Workflow-Auszug

```yaml
name: CI Quality Check

on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run flake8
        run: flake8 app/ tests/

      - name: Run pytest
        run: pytest tests/

      - name: Run bandit
        run: bandit -r app/
```
