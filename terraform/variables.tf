# Variables for the MTG Inventory Manager Terraform configuration

variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "mtginv"
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment name (e.g. dev, test, prod)"
  type        = string
  default     = "dev"
}

variable "app_service_plan_tier" {
  description = "App Service Plan tier"
  type        = string
  default     = "Basic"
}

variable "app_service_plan_size" {
  description = "App Service Plan size"
  type        = string
  default     = "B1"
}
