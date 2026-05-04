variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "eu-west-1"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository for the iris classifier"
  type        = string
  default     = "iris-classifier"
}

variable "project_name" {
  description = "Project name used for tagging resources"
  type        = string
  default     = "giar20-mlops-pipeline"
}