output "lambda_function_url" {
  description = "Public HTTPS URL of the Lambda function"
  value       = aws_lambda_function_url.iris_classifier.function_url
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.iris_classifier.arn
}