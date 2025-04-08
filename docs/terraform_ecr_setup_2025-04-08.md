# 🛠️ Terraform Infrastructure Setup für Amazon ECR

Dieses Dokument beschreibt, wie wir das AWS Elastic Container Registry (ECR) mithilfe von Terraform eingerichtet und in unser DevOps-Projekt `smartcalender` integriert haben.

## 🎯 Ziel

Einrichtung und Management eines ECR-Repositories (`smartcalender-api`) über **Infrastructure as Code** mit Terraform.

---

## 📁 Projektstruktur

```bash
terraform/
├── main.tf          # Hauptkonfiguration für ECR
├── outputs.tf       # Output-Variablen wie repository_url
└── variables.tf     # (aktuell leer, bereit für spätere Nutzung)
```

---

## 📦 Verwendete Ressourcen

### `aws_ecr_repository`

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

## ✅ Schritte zur Nutzung

### 1. Repository importieren (falls schon vorhanden)

```bash
terraform import aws_ecr_repository.this smartcalender-api
```

### 2. Initialisieren

```bash
terraform init
```

### 3. Plan anzeigen

```bash
terraform plan
```

### 4. Anwenden

```bash
terraform apply
```

---

## 🧪 Test & Status

Die Konfiguration wurde erfolgreich ausgeführt. Das Repository ist bereits vorhanden und nun in Terraform eingebunden. Es wird jetzt vollständig von Terraform verwaltet.

---

## 🔐 Sicherheit & Best Practices

- **Scan on Push** ist aktiviert → automatische Sicherheitsprüfung beim Push von Docker-Images.
- Tags helfen bei Nachvollziehbarkeit (`Environment`, `ManagedBy`).

---

## 🔄 Nächste Schritte

- Erweiterung um ECS / Fargate Setup via Terraform.
- Automatisierung des gesamten Infrastructure-Provisioning durch CI/CD.
