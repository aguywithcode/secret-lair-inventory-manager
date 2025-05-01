# Main Terraform configuration file for MTG Inventory Manager

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  # Uncomment this block to use Terraform Cloud for state management
  # backend "azurerm" {
  #   resource_group_name  = "terraform-state-rg"
  #   storage_account_name = "mtginventorytfstate"
  #   container_name       = "tfstate"
  #   key                  = "terraform.tfstate"
  # }
}

provider "azurerm" {
  features {}
}

# Resource group for all MTG Inventory Manager resources
resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = var.location
  
  tags = {
    environment = var.environment
    project     = "MTG Inventory Manager"
  }
}

# Include other module configurations
module "app_service" {
  source              = "./modules/app_service"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  prefix              = var.prefix
  environment         = var.environment
}

module "cosmos_db" {
  source              = "./modules/cosmos_db"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  prefix              = var.prefix
  environment         = var.environment
}

module "function_app" {
  source              = "./modules/function_app"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  prefix              = var.prefix
  environment         = var.environment
}
