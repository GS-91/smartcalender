# Terraform Infrastruktur Setup

Diese Datei beschreibt die Terraform-Konfiguration zur Erstellung der AWS-Infrastruktur für den SmartCalendar.

## Komponenten

1. **ECS Cluster** (`aws_ecs_cluster`)
   - Erstellt einen neuen Cluster mit Tags.
   - Name: `smartcalender-cluster-v2`

2. **IAM Rolle für ECS Task Execution**
   - Ressource: `aws_iam_role.ecs_task_execution_role`
   - Zweck: Berechtigt ECS-Tasks, AWS-Dienste zu verwenden.
   - Bindung an Standardpolicy: `AmazonECSTaskExecutionRolePolicy`

3. **Task Definition**
   - Ressource: `aws_ecs_task_definition`
   - Verwendung von FARGATE mit Netzwerkmodus `awsvpc`.
   - Container-Konfiguration mit Port 8000.

4. **ECS Service**
   - Ressource: `aws_ecs_service`
   - Bindet Task Definition an ECS Cluster.
   - Läuft in einem öffentlichen Subnetz.
   - Sicherheit: Nutzung von Security Groups und Subnets.

## Hinweise

- Terraform ignoriert Task-Definition-Änderungen automatisch (`ignore_changes`).
- ECR wird mit Image `smartcalender-api:latest` verwendet.