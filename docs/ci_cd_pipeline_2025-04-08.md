# CI/CD Deployment Documentation – SmartCalendar (Stand: 2025-04-08)

## 🎯 Zielsetzung

Diese Dokumentation beschreibt den Aufbau und die erfolgreiche Implementierung einer Continuous Integration / Continuous Deployment (CI/CD) Pipeline für die FastAPI-basierte SmartCalendar-Anwendung mit Deployment auf **AWS ECS Fargate** und Nutzung von **Amazon ECR** als Container Registry.

---

## 🧱 Architekturüberblick

```plaintext
  +---------+        +----------+         +-----------+         +-------------+
  | GitHub  |  --->  | GitHub   |  --->   | Docker    |  --->   | AWS         |
  | Actions |        | Workflow |         | Container |         | ECS Fargate |
  +---------+        +----------+         +-----------+         +-------------+
       |                                                    |
       |    🔐 Credentials via Secrets                      |
       |    📦 Build & Push Docker Image                    |
       |    🚀 Trigger ECS Deployment                       |
       |                                                    |
       +----------------------------------------------------+
```

---

## 🛠️ Komponenten im Überblick

- **GitHub Actions**: Automatisierte Ausführung beim Manuell-Auslösen (`workflow_dispatch`)
- **Docker Buildx**: Ermöglicht plattformübergreifende Docker-Images (`--platform linux/amd64`)
- **AWS CLI**: Aktualisiert den ECS-Service mit dem neuen Image
- **AWS ECR**: Registry zur Speicherung des Docker-Images
- **AWS ECS Fargate**: Orchestrierung und Ausführung des Containers
- **Secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`, `CREDENTIALS_JSON_B64`, `API_KEY_TXT_B64`

---

## 🔁 GitHub Actions Workflow

### Datei: `.github/workflows/docker-ci-cd.yml`

```yaml
name: Docker CI/CD

on:
  workflow_dispatch:

env:
  AWS_REGION: eu-central-1
  ECR_REPOSITORY: smartcalender-api
  IMAGE_TAG: latest

jobs:
  build-and-deploy:
    name: 🚀 Build & Push Docker image to ECR
    runs-on: ubuntu-latest

    steps:
      - name: 🔄 Checkout code
        uses: actions/checkout@v3

      - name: 🔐 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: 📄 Decode credentials.json from secret
        run: |
          mkdir -p app/api
          echo "${{ secrets.CREDENTIALS_JSON_B64 }}" | base64 -d > app/api/credentials.json

      - name: 📄 Decode api_key.txt from secret
        run: |
          echo "${{ secrets.API_KEY_TXT_B64 }}" | base64 -d > app/api_key.txt

      - name: 🧱 Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: 🔑 Log in to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1

      - name: 🐳 Build Docker image
        run: |
          IMAGE_URI="${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com/${{ env.ECR_REPOSITORY }}"
          docker buildx build --platform linux/amd64 -t $IMAGE_URI:$IMAGE_TAG -f Dockerfile .

      - name: 📦 Push Docker image to ECR
        run: |
          IMAGE_URI="${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com/${{ env.ECR_REPOSITORY }}"
          docker push $IMAGE_URI:$IMAGE_TAG

      - name: 🚀 Deploy to ECS
        run: |
          aws ecs update-service             --cluster smartcalender-cluster-v2             --service smartcalender-service             --force-new-deployment             --region $AWS_REGION
```

---

## 🧪 Validierung

- **Manueller Trigger** über GitHub Actions → erfolgreich ✅
- **Image Push nach ECR**: `latest`-Tag verfügbar und aktualisiert
- **ECS Deployment**: Task erfolgreich gestartet
- **API getestet via**:
```bash
curl http://<ECS_PUBLIC_IP>:8000/
# → { "message": "API läuft!" }
```

---

## 🏁 Fazit

Mit dieser Pipeline wurde ein vollständiger CI/CD-Prozess realisiert:
- Automatischer Build + Push eines Docker-Images via GitHub Actions
- Geheimnisverwaltung über GitHub Secrets (Base64-Encoded Files)
- ECS-Rollout durch `aws ecs update-service`
- Nutzung von Buildx zur Kompatibilität mit ECS (amd64)

Diese Struktur ist **branchfähig**, **skalierbar** und entspricht einem **industriellen Standard für cloud-native Microservices**.

✅ Continuous Deployment aktiv: Jeder Push auf `main` triggert automatischen Build & Deployment auf AWS Fargate.

---

## 📝 Autoreninfo

Erstellt von: **Gabriel Simon**  
Plattform: GitHub + AWS (ECR, ECS Fargate)  
Projekt: [SmartCalendar](https://github.com/GS-91/smartcalender)
