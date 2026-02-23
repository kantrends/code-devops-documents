# Purpose
This document outlines the process for deploying an application to Azure Container Apps (ACA). It includes packaging the application into a Docker image, uploading the image to Azure Container Registry (ACR), mounting an Azure File Share to the container as a volume using System-Assigned Managed Identity for secure access (without using storage account keys) and configuring the Azure Container App to pull the image from ACR for deployment or updates.

# Pre-requisite

1. The Cloud DevOps Team must provision the Azure Container App (ACA) with the necessary permissions to pull container images from Azure Container Registry (ACR)

2. To use Azure File Share, ensure the Cloud DevOps Team assigns a managed identity between Azure Container Apps (ACA) and Azure File Share with the following role.
   - ROLE: `Storage File Data SMB Share Contributor`

- Create Library Group: `revelations-annotator-tool-dev`.  
    | Key                        | Value                 |  
    |----------------------------|-----------------------|  
    | DATABASE_PASSWORD          | *********       |  
    | DATABASE_USERNAME          | jade_adm             |  
    | spring_active_profile      | dev                  |  
    | var_acr_name               | pasrevdevamlacr      |  
    | var_az_containerapp        | annotator-tool-dev   |  
    | var_az_containerapp_env    | prodigy-dev          |  
    | var_az_containerapp_rg     | prodigy_aca_dev_rg   |  
    | var_az_keyvault            | PASREV-dev           |  
    | var_cpu                    | 0.5                  |  
    | var_max_replicas           | 1                    |  
    | var_memory                 | 1Gi                  |
    | var_storage_account_name   | codeacastoragenpe88y |


# Explanation
- `pipeline/azure-pipeline.yaml` This is the main pipeline file.
  
- `pipeline/ci.yaml` contains the CI part including building the application and creating a Docker image.
   - `Set Project Properties`: Extracts project details with Maven and sets them as pipeline variables.
   - `Build Job`: Builds the project JAR, creates a Docker image, and saves it as an artifact.
   - `Checkmarx Scan`: Runs a Checkmarx security scan for code vulnerabilities.
   - `Nexus Lifecycle Scan`: Conducts a NexusIQ scan for dependency vulnerabilities.
     
- `pipeline/deploy.yaml` is the template file that deploys to Azure ACA.
    - `Check Artifact Availability`: Ensures the Docker image artifact is ready for deployment.
    -  `Load and Tag Image`: Loads the image, tags it for ACR.
    - `Push Image to ACR`: Logs in to ACR and pushes the image.
    - `Update Azure Keyvault Secrets`: Updates secrets in Azure Keyvault (e.g., database credentials).
    - `Create Container App`: Uses a YAML configuration to create or update an Azure Container App with container settings and resource configurations including file share mount.
