# Purpose
Deploy app to AKS using Manifest files.  Use this if you don't want to try HELM.

## Pre-requisite
- Make sure the ARM connection is present
- Make sure the ARM connection has access to AKS. (If not working, submit ticket with cloud devops team)
- Make sure the ARM connection has access to push images to ACR. (If not working, submit ticket with cloud devops team)
- Make sure the Ingress Controller is already deployed. If not, refer to that example. 

## Steps
- Copy the aks_manifest_files directory and update it accordingly
- Create variable groups for each environment

| Name | value |
| --- | --- |
| var_acr_name | codenp |
| var_aks_rg | |
| var_aks_name | |
| var_aks_namespace | |
| var_host_name | code-sample-app-nginx-manifest.code-aks-dev.premierinc.com (Assuming *.code-aks-dev.premierinc.com DNS record created. If not, check README section of ingress-controller example) |
| var_az_kv_name | codenp (Required only if you use Azure key vault)  | 
| var_aks_kv_managed_identity | 8888-xxx-xxx (Required only if you use Azure key vault) | 
| var_pv_vol_handle | PQA_NP-pqastoragenpw3pe-aks-poc "pv unique volume handle name (unique across cluster). give it like combination of rg, sa-name,file-share-name" |
| var_pv_vol_name | sample-app-1-manifest-dev-azurefile-pv "pv volume name (unique across cluster)" |
| var_storage_account_file_share | aks-poc (file share name) | 
| var_storage_acc_name | pqastorageaccoutn |
| var_storage_acc_rg | pqa-np |


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
