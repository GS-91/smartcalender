# SmartCalendar – DevOps Project with Google Calendar API & OpenAI

SmartCalendar is a personal DevOps project aimed at automating calendar entries via REST API. The FastAPI application creates Google Calendar events and generates humorous titles using GPT-4 from OpenAI. The project emphasizes Clean Code, CI/CD pipelines, Infrastructure as Code (IaC), and Docker.

## Technologies & Tools

- **Python** (FastAPI, Pydantic, Pytest)  
- **Google Calendar API & OpenAI API**  
- **Docker & Docker Compose**  
- **GitHub Actions** (CI/CD with linting, tests, security scans)  
- **Terraform** (AWS ECS, Fargate, ECR Deployment)  
- **Bandit, Flake8, Coverage Report**  
- **Secrets Management via GitHub Secrets**

## DevOps Focus

- Fully automated deployment process with GitHub Actions  
- Quality assurance using flake8, pytest, bandit  
- Real API integration and secrets management in the CI/CD context  
- Declarative provisioning of AWS infrastructure using Terraform  
- Clean project structure following DevOps best practices

## Why this project?

Driven by a personal interest in modern DevOps principles, I initiated this project to implement a practical API scenario. The goal was to apply and deepen my understanding of key DevOps components, such as CI/CD, containerization, and cloud infrastructure, through a concrete use-case.

## Features

- Creating calendar entries
- Listing calendar entries
- Listing connected Google calendars
- Generating humorous titles via OpenAI

## Installation

### 1. Local Setup

```bash
git clone https://github.com/GS-91/smartcalender.git
cd smartcalender
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API is accessible at: `http://localhost:8000`

### 2. Docker Setup

```bash
docker-compose -f infra/docker-compose.yml up --build -d
```

---

## API-Endpunkte

| Methode | Pfad                        | Beschreibung                                |
|--------|-----------------------------|---------------------------------------------|
| GET    | /                           | API-Status                                  |
| POST   | /calendar/create_event/     | create new calender event                    |
| GET    | /calendar/list_events/      | Retrieve upcoming events                  |
| GET    | /calendar/list_calendars/   | Retrieve available Google calendars          |
| POST   | /generate_funny_response/   | Generate humorous title via OpenAI       |

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
