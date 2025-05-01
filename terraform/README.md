# MTG Inventory Manager Infrastructure

This directory contains Terraform configuration files for deploying the MTG Inventory Manager to Azure.

## Infrastructure Components

- **App Service**: Hosts the web application
- **Function App**: Handles data processing tasks
- **Cosmos DB**: Stores card and user collection data
- **Storage Account**: Stores Function App code and data

## Getting Started

1. Install [Terraform](https://www.terraform.io/downloads.html)

2. Configure Azure credentials:
   ```
   az login
   ```

3. Initialize Terraform:
   ```
   terraform init
   ```

4. Plan the deployment:
   ```
   terraform plan -out=tfplan
   ```

5. Apply the deployment:
   ```
   terraform apply tfplan
   ```

## Environment Variables

To customize the deployment, you can set the following environment variables:

- `TF_VAR_prefix`: Prefix for resource names (default: "mtginv")
- `TF_VAR_location`: Azure region for resources (default: "eastus")
- `TF_VAR_environment`: Environment name (default: "dev")

## Notes

- The default configuration is suitable for development environments
- For production, modify the variables.tf file to use appropriate resource sizes
- Consider using Azure Key Vault for storing secrets in production
