output "ecr_repository_url" {
  description = "URL of the ECR repository (use this in CI/CD)"
  value       = aws_ecr_repository.iris_classifier.repository_url
}

output "ecr_repository_arn" {
  description = "ARN of the ECR repository"
  value       = aws_ecr_repository.iris_classifier.arn
}

output "aws_region" {
  description = "AWS region used for deployment"
  value       = var.aws_region
}

output "lambda_function_url" {
  description = "Public HTTPS URL of the Lambda function"
  value       = aws_lambda_function_url.iris_classifier.function_url
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.iris_classifier.arn
}