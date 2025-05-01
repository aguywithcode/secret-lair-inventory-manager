# Output values from the Terraform deployment

output "app_service_url" {
  description = "URL of the deployed App Service"
  value       = module.app_service.app_service_url
}

output "function_app_url" {
  description = "URL of the deployed Function App"
  value       = module.function_app.function_app_url
}

output "cosmos_db_endpoint" {
  description = "Endpoint of the CosmosDB account"
  value       = module.cosmos_db.cosmos_db_endpoint
  sensitive   = true
}
