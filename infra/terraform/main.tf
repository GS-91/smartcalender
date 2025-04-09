# 0. ECR Repository (bestehendes Repository wird erhalten!)
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

# 1. ECS Cluster erstellen
resource "aws_ecs_cluster" "this" {
  name = "smartcalender-cluster-v2"
  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# 2. IAM Rolle für Task-Ausführung (wird von ECS benötigt)
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    ManagedBy = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# 3. Task Definition
resource "aws_ecs_task_definition" "this" {
  family                   = "smartcalender-task-v2"
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = "1024"
  memory                  = "3072"
  execution_role_arn      = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "smartcalender-container"
      image = "${var.aws_account_id}.dkr.ecr.eu-central-1.amazonaws.com/smartcalender-api:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

# 4. ECS Service
resource "aws_ecs_service" "this" {
  name            = "smartcalender-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnet_ids
    assign_public_ip = true
    security_groups = var.security_group_ids
  }

  lifecycle {
    ignore_changes = [task_definition] # Damit `terraform apply` nicht jedes Mal neu deployed
  }

  deployment_controller {
    type = "ECS"
  }
}
