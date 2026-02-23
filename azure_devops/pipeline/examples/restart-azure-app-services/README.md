# Purpose
This document provides step-by-step instructions to manage Azure App Services using an Azure DevOps pipeline. It covers actions like restarting, starting, and stopping an App Service through an automated pipeline.

# Best Practices
It is advised to keep a separate repository to handle all Azure-related operations. This ensures better organization, security, and reusability.

**Recommended Approach**
- Create a dedicated repository: For example, if your project name is mii, create a repository named mii-azure-operations.
- Organize folders by operation: Within the repository, create a folder named restart-app-services to hold all related pipeline files.
- Use a dedicated pipeline: Set up a separate pipeline for this specific operation to manage Azure App Services efficiently.

# Prerequisites
- App Service Name and Resource Group: Identify the target App Service and its corresponding resource group.
- Service Connection in Azure DevOps: Ensure that a service connection is established in Azure DevOps with sufficient permissions within the Azure subscription.
- Azure CLI Installed: The pipeline uses Azure CLI for managing App Services.

# Explanation
The pipeline accepts parameters for the application name, environment, and action to perform. Based on the selected parameters, it performs the desired action (restart, start, or stop) on the specified App Service using the Azure CLI.

### Key Steps
- Select App and Environment: Choose the application (e.g., ems-app) and environment (e.g., dev, prd).
- Select Action: Pick restart, start, or stop.
- Run the Pipeline: The pipeline retrieves details and executes the selected action using Azure CLI.

### Example Commands
```
# Restart App Service
az webapp restart --name <appServiceName> --resource-group <resourceGroupName>

# Start App Service
az webapp start --name <appServiceName> --resource-group <resourceGroupName>

# Stop App Service
az webapp stop --name <appServiceName> --resource-group <resourceGroupName>
```
### Status Verification
The pipeline checks the App Service status to ensure the action was successful:
```
az webapp show --name <appServiceName> --resource-group <resourceGroupName> --query "state" -o tsv
```

