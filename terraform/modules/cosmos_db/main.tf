# Cosmos DB module configuration for MTG Inventory Manager

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmos-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  tags = {
    environment = var.environment
    component   = "database"
  }
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = "mtg-inventory"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  throughput          = var.cosmos_throughput
}

resource "azurerm_cosmosdb_sql_container" "secret_lairs" {
  name                = "secret-lairs"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_paths = ["/drop_number"]
  throughput          = 400
}

resource "azurerm_cosmosdb_sql_container" "user_collections" {
  name                = "user-collections"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_paths = ["/userId"]
  throughput          = 400
}
