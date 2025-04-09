# 🌐 Terraform Infrastruktur Setup für SmartCalender (Stand: 2025-04-08)

Diese Dokumentation beschreibt das vollständige Setup der AWS-Infrastruktur für den SmartCalender-Dienst mittels Terraform. Ziel ist es, die gesamte Infrastruktur als Code (IaC) reproduzierbar, versionskontrolliert und automatisierbar zu gestalten.

---

## 📁 Projektstruktur

```bash
infra/
└── terraform/
    ├── main.tf              # Hauptressourcen: ECS, Task Definition, Service
    ├── variables.tf         # Eingabevariablen
    ├── outputs.tf           # Wichtige Outputs nach dem Apply
    ├── provider.tf          # AWS Provider Konfiguration
    └── terraform.tfvars     # Konkrete Werte für Variablen (z. B. Account ID)
```

---

## 🔧 Verwendete Ressourcen

### 1. `aws_ecr_repository`

Ein privates Container-Registry in ECR mit automatischem Security-Scan bei jedem Push.

```hcl
resource "aws_ecr_repository" "this" {
  name                 = "smartcalender-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
```

---

### 2. `aws_ecs_cluster`

Ein Fargate-kompatibler Cluster für unsere Container.

```hcl
resource "aws_ecs_cluster" "this" {
  name = "smartcalender-cluster-v2"

  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
```

---

### 3. IAM Execution Role

Diese Rolle erlaubt es Fargate, Container-Images zu pullen und Logs zu schreiben.

```hcl
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })

  tags = { ManagedBy = "Terraform" }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
```

---

### 4. `aws_ecs_task_definition`

Die Definition unserer Laufzeitumgebung.

```hcl
resource "aws_ecs_task_definition" "this" {
  family                   = "smartcalender-task-v2"
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = "1024"
  memory                  = "3072"
  execution_role_arn      = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name  = "smartcalender-container",
    image = "<ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com/smartcalender-api:latest",
    essential = true,
    portMappings = [{
      containerPort = 8000,
      hostPort      = 8000
    }]
  }])
}
```

---

### 5. `aws_ecs_service`

Verknüpft Task, Cluster und Netzwerk.

```hcl
resource "aws_ecs_service" "this" {
  name            = "smartcalender-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = true
    security_groups  = var.security_group_ids
    subnets          = var.subnet_ids
  }

  deployment_controller {
    type = "ECS"
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}
```

---

## 📤 Outputs

```hcl
output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  value = aws_ecs_service.this.name
}

output "ecs_task_definition_arn" {
  value = aws_ecs_task_definition.this.arn
}
```

---

## 📌 Hinweise

- Alle Ressourcen werden mit Tags versehen, um die Verwaltung zu erleichtern.
- `terraform.tfvars` enthält sensible Werte wie `aws_account_id`, `subnet_ids`, `security_group_ids` – niemals öffentlich teilen.
- `terraform apply` sollte nur nach vorherigem `terraform plan` und Review erfolgen.

---

## ✅ Status

- [x] ECR Repository erstellt und importiert
- [x] ECS Cluster + Service über Terraform provisioniert
- [x] IAM Rolle korrekt zugewiesen
- [x] Task Definition erzeugt und bereitgestellt
