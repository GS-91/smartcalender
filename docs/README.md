# SmartCalendar – DevOps-Kalender mit Google API & FastAPI

SmartCalendar ist eine FastAPI-Anwendung zur Verwaltung von Google-Kalendereinträgen. Sie nutzt die Google Calendar API und OpenAI, um Termine automatisch mit humorvollen Titeln zu erstellen. Zusätzlich stellt das Projekt eine vollständige CI/CD-Qualitätssicherung über GitHub Actions bereit.

## Funktionen

- Erstellen von Kalendereinträgen
- Auflisten von Kalendereinträgen
- Auflisten von verbundenen Google-Kalendern
- Generieren humorvoller Titel via OpenAI

## Installation

### 1. Lokales Setup

```bash
git clone https://github.com/GS-91/smartcalender.git
cd smartcalender
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Die API ist erreichbar unter: `http://localhost:8000`

### 2. Docker Setup

```bash
docker-compose -f infra/docker-compose.yml up --build -d
```

---

## API-Endpunkte

| Methode | Pfad                        | Beschreibung                                |
|--------|-----------------------------|---------------------------------------------|
| GET    | /                           | API-Status                                  |
| POST   | /calendar/create_event/     | Neuen Termin erstellen                      |
| GET    | /calendar/list_events/      | Kommende Termine abrufen                    |
| GET    | /calendar/list_calendars/   | Verfügbare Google-Kalender abrufen          |
| POST   | /generate_funny_response/   | Humorvollen Titel erzeugen via OpenAI       |

### Beispiel-Request

```json
{
  "user_input": "Team Meeting",
  "day": "WE",
  "time": "10:00",
  "duration": 2
}
```

---

## Qualitätssicherung mit GitHub Actions

Dieses Projekt enthält eine GitHub Actions Pipeline, die bei jedem Push auf `main` sowie bei Pull Requests automatisch folgende Prüfungen durchführt:

- **Code Style Check** – mit flake8
- **Unittests** – mit pytest
- **Security Scan** – mit bandit

👉 Details findest du in der Dokumentation [`ci_cd_quality_pipeline.md`](docs/ci_cd_quality_pipeline.md)

---

## Infrastruktur mit Terraform

Die Bereitstellung in AWS (ECS, Fargate, ECR) erfolgt mithilfe von Terraform.

👉 Anleitungen:
- [`terraform_infra_setup.md`](docs/terraform_infra_setup.md)
- [`terraform_ecr_setup_2025-04-08.md`](docs/terraform_ecr_setup_2025-04-08.md)

---

## Docker-Dokumentation

👉 Schritt-für-Schritt-Anleitungen:
- [`docker_setup.md`](docs/docker_setup.md)
- [`docker_installation.md`](docs/docker_installation.md)
- [`DockerAndCalender.md`](docs/DockerAndCalender.md)

---

## Weitere Ressourcen

- [`ci_cd_pipeline_2025-04-08.md`](docs/ci_cd_pipeline_2025-04-08.md) – ältere CI/CD-Doku
- [`README_smartcalendar.md`](docs/README_smartcalendar.md) – Feature-Überblick
- `doc.pdf` – Schritt-für-Schritt AWS Cluster Einrichtung (mit Screenshots)

---

## Autor

Gabriel Simon  
GitHub: [GS-91](https://github.com/GS-91)
