# Outputs from Cosmos DB module

output "cosmos_db_endpoint" {
  description = "Endpoint of the CosmosDB account"
  value       = azurerm_cosmosdb_account.main.endpoint
}

output "cosmos_db_primary_key" {
  description = "Primary key of the CosmosDB account"
  value       = azurerm_cosmosdb_account.main.primary_key
  sensitive   = true
}

# Updated to use the current recommended approach instead of deprecated connection_strings
output "cosmos_db_primary_connection_string" {
  description = "Primary connection string of the CosmosDB account"
  value       = azurerm_cosmosdb_account.main.primary_sql_connection_string
  sensitive   = true
}

output "cosmos_db_secondary_connection_string" {
  description = "Secondary connection string of the CosmosDB account"
  value       = azurerm_cosmosdb_account.main.secondary_sql_connection_string
  sensitive   = true
}
