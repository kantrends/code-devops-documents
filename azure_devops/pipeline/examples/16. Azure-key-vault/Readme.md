# Azure DevOps Pipeline for Updating Key Vault Secrets

This repository contains a pipeline for syncing secrets from an Azure DevOps Library Group to an Azure Key Vault. It ensures that secrets in the Azure Key Vault are updated only if their values have changed.


This pipeline automates the process of syncing secrets stored in Azure DevOps Library Groups with Azure Key Vault. It updates secrets in the Key Vault only when their values have changed, helping to keep your Key Vault secrets in sync with the values defined in Azure DevOps.

The pipeline supports multiple environments: `dev`, `perf` and `prod`. For each environment, you can specify the corresponding secrets to sync with the Azure Key Vault.

## Pipeline Configuration

- It advised to have a repository `[proj]-azure-operations`.  Use this repository for all azure related operations.  Create a folder called `keyvault` in it and put the azure-pipeline.yml file and keyvault.sh file

- Modify the ado library group name, azure ARM service connection names in the azure-pipeline.yaml file

## How to add new secrets
- Add the secret in the ADO library group
- Add the secret name in the azure-pipeline.yaml file

## Sample ADO Library group
| Name | Value |
| --- | --- |
| var_az_keyvault | code-np |
| secret1 | NoWay (masked) | 
