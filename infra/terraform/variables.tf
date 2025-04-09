variable "aws_account_id" {
  description = "Your AWS Account ID"
  type        = string
}

variable "subnet_ids" {
  description = "List of Subnet IDs in the VPC"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of Security Group IDs for ECS"
  type        = list(string)
}


variable "aws_region" {
  description = "AWS region for deploying resources"
  type        = string
  default     = "eu-central-1"
}
