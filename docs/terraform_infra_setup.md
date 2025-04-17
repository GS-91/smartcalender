# Terraform Infrastruktur Setup

Diese Datei beschreibt auf einfache und professionelle Weise die Terraform-Konfiguration zur Erstellung der AWS-Infrastruktur für die SmartCalendar-App. Sie richtet automatisch die nötige Cloud-Umgebung ein, um die Anwendung auf Fargate (AWS ECS) zu betreiben.

Siehe Konfigurationsdatei: [`infra/terraform/main.tf`](../infra/terraform/main.tf)

---

## Komponenten

1. **ECS Cluster** (`aws_ecs_cluster`)
   - Erstellt einen neuen ECS-Cluster mit entsprechenden Tags.
   - Beispielname: `smartcalender-cluster-v2`

2. **IAM Rolle für ECS Task Execution**
   - Ressource: `aws_iam_role.ecs_task_execution_role`
   - Funktion: Erlaubt ECS-Tasks, benötigte AWS-Dienste wie Logs oder ECR zu verwenden.
   - Inklusive Standard-Policy: `AmazonECSTaskExecutionRolePolicy`

3. **Task Definition**
   - Ressource: `aws_ecs_task_definition`
   - Plattform: FARGATE
   - Netzwerkmodus: `awsvpc`
   - Container-Konfiguration:
     - Port 8000

4. **ECS Service**
   - Ressource: `aws_ecs_service`
   - Bindet die Task Definition an den ECS Cluster.
   - Führt Container in einem öffentlichen Subnetz aus.
   - Konfiguration mit Security Groups und Subnets.

---

## Hinweise

- Die Konfiguration nutzt `ignore_changes`, um Task-Definitionen bei kleinen Änderungen nicht unnötig neu zu erstellen.
- Das Container-Image wird aus einem ECR-Repository geladen, z. B. `smartcalender-api:latest`.

- Die Konfigurationen befinden sich im Verzeichnis `infra/terraform/`.
- Zentrale Datei: `infra/terraform/main.tf`
- Optional: Umgebungsvariablen über `.tfvars` einbinden

##  Weitere Ressourcen
- [Terraform-Dokumentation](https://developer.hashicorp.com/terraform/docs)
- [AWS ECS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service)
