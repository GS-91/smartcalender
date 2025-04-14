# SmartCalendar – DevOps-Projekt mit Google Calendar API & OpenAI

SmartCalendar ist ein persönliches DevOps-Projekt zur Automatisierung von Kalendereinträgen via REST API. Die FastAPI-Anwendung erstellt Google-Kalendereinträge und generiert humorvolle Titel mit GPT-4 von OpenAI. Das Projekt wurde mit Fokus auf Clean Code, CI/CD-Pipelines, Infrastructure as Code (IaC) und Docker umgesetzt.

## Technologien & Tools

- **Python** (FastAPI, Pydantic, Pytest)  
- **Google Calendar API & OpenAI API**  
- **Docker & Docker Compose**  
- **GitHub Actions** (CI/CD mit Linting, Tests, Security Scan)  
- **Terraform** (AWS ECS, Fargate, ECR Deployment)  
- **Bandit, Flake8, Coverage Report**  
- **Secrets Management via GitHub Secrets**

## DevOps-Fokus

- Vollautomatisierter Deployment-Prozess über GitHub Actions  
- Qualitätssicherung mit flake8, pytest, bandit  
- Echte API-Integration und Secrets Management im CI/CD-Kontext  
- AWS-Infrastruktur deklarativ provisioniert mit Terraform  
- Saubere Projektstruktur nach DevOps Best Practices

## Warum dieses Projekt?

Aus persönlichem Interesse an modernen DevOps-Prinzipien habe ich dieses Projekt gestartet, um ein praxisnahes API-Szenario umzusetzen. Ziel war es, zentrale DevOps-Komponenten wie CI/CD, Containerisierung und Cloud-Infrastruktur an einem konkreten Beispiel anzuwenden und besser zu verstehen.


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
