# Purpose
Deploy app to AKS using HELM Charts files.

## Pre-requisite
- Make sure the ARM connection is present
- Make sure the ARM connection has access to AKS. (If not working, submit ticket with cloud devops team)
- Make sure the ARM connection has access to push images to ACR. (If not working, submit ticket with cloud devops team)
- Make sure the Ingress Controller is already deployed. If not, refer to that example. 

## Steps
- Copy the `helm-charts` and `pipeline` directory and update it accordingly
- Create variable groups for each environment.

> Note: You can also have one ado library group that contains the details about AKS and re-use the same in multiple pipelines.

| Name | value |
| --- | --- |
| var_acr_name | codenp |
| var_aks_rg | |
| var_aks_name | |
| var_aks_namespace | |

- Feel free to add custom helm chart yaml under `helm-charts/templates` directory.
- Commonly used values are saved in `values.yaml` or you can have it in `environments/dev.yaml` which override environment specific values. 

- To find the AKS KV Managed identity ID, run the below command and retrieve the clientId
```bash
az aks show --resource-group  "RESOURCEGROUP" --name "AKS_cluster_NAME" --query addonProfiles.azureKeyvaultSecretsProvider.identity

# EXAMPLE
az aks show --resource-group  CODENP --name code-np-eastus-01 --query addonProfiles.azureKeyvaultSecretsProvider.identity
```

- If you are going to use Azure file share, then make sure the kubelet identity of cluster is added to storage account. Retrieve the client ID using below command. If you are unsure, just give this command to Cloud DevOps Team, they will take care. 
```bash
az aks show --resource-group  "RESOURCEGROUP" --name "AKS_cluster_NAME" --query 'identityProfile.kubeletidentity.clientId'

az aks show --resource-group  CODENP --name code-np-eastus-01 --query 'identityProfile.kubeletidentity.clientId'
```

## Reference
- [Azure key vault mount](https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-identity-access?tabs=azure-portal&pivots=access-with-a-user-assigned-managed-identity)
