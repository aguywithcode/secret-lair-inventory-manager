# Variables for App Service module

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
}

variable "prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g. dev, test, prod)"
  type        = string
}

variable "app_service_plan_tier" {
  description = "App Service Plan tier"
  type        = string
  default     = "B" # Basic tier
}

variable "app_service_plan_size" {
  description = "App Service Plan size"
  type        = string
  default     = "1" # Size 1
}
