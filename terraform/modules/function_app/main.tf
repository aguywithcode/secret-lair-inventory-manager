# Function App module configuration for MTG Inventory Manager

# Storage account for Function App
resource "azurerm_storage_account" "main" {
  name                     = "${var.prefix}fnstor${var.environment}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = var.environment
    component   = "function-storage"
  }
}

# App Service Plan for Function App
resource "azurerm_service_plan" "function" {
  name                = "${var.prefix}-fn-asp-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "EP1" # Premium plan that supports Linux

  tags = {
    environment = var.environment
    component   = "function"
  }
}

# Function App for data processing
resource "azurerm_linux_function_app" "main" {
  name                       = "${var.prefix}-function-${var.environment}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_service_plan.function.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"
    }
    # Adding CORS support for web application integration
    cors {
      allowed_origins = ["https://${var.prefix}-app-${var.environment}.azurewebsites.net"]
      support_credentials = true
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"    = "python"
    "APPINSIGHTS_INSTRUMENTATIONKEY" = var.app_insights_key
    # Add configuration for Cosmos DB connection
    "COSMOSDB_ENDPOINT"           = var.cosmos_db_endpoint
  }

  tags = {
    environment = var.environment
    component   = "function"
  }
}
