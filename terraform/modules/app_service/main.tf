# App Service module configuration for MTG Inventory Manager

# Service Plan (replacing deprecated App Service Plan)
resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-asp-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "${var.app_service_plan_tier}_${var.app_service_plan_size}"

  tags = {
    environment = var.environment
    component   = "web"
  }
}

# App Service for hosting the web application
resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-app-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = "3.9"
    }
    always_on        = true
    # Add health check path for better monitoring
    health_check_path = "/api/health"
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "WEBSITES_PORT"                  = "5000"
    "WEBSITE_HTTPLOGGING_RETENTION_DAYS" = "7"
  }

  tags = {
    environment = var.environment
    component   = "web"
  }
}
