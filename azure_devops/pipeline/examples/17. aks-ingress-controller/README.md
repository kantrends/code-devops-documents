# Ingress Controller in AKS
Example to deploy Nginx Ingress Controller in AKS. 

# Pre-requisite:
- ARM Service Connection in ADO
- AKS Cluster
- Azure KeyVault

# Steps
- It is advised to create this in a repository `[proj]-azure-operations` and create a folder `aks-ingress-controller` and put the contents in this example there. 
- Create a folder in ADO pipeline as `Azure Operations`. Create a azure pipeline within the folder and name it as `aks-ingress-controller`

# Files
- `pipeline` directory:
  - `azure-pipeline.yaml`: ADO Pipeline to deploy Ingress Controller.  create stages as many clusters you have. "np", "prod"
  - `helm-deploy.yaml`: ADO deploy template
- `environments` directory:
  - We are using HELM Charts to deploy Nginx Ingress Controller. 
  - Based on this official [document](https://github.com/kubernetes/ingress-nginx/blob/main/charts/ingress-nginx/values.yaml), we can override the Ingress Controller options.
  - `*.yaml` is created for each AKS cluster.
  - Make sure the Private IP mentioned in this file is unused and dedicated only for this.  Choose one Random Private IP from the AKS subnet.  Also remember, changing this IP in future, involves lot of changes in future.  Kindly, stay with one IP forever. 
  - Run the below command to find one available IP
  ```bash
  az login
  az account set --subscription "YourSubscriptionName"
  az network vnet check-ip-address --resource-group "YOUR_VNET_RG" --name "YOUR_VNET_NAME" --ip-address "ONE_OF_THE_IP_FROM_AKS_SUBNET"
  ```
- `templates` directory:
  - `ingress-tls.yaml`: For configuring SSL certificate on the Nginx Ingress Controller.  Check the Appendix section to create the SSL Certificate and save it in ADO Library Secure file. 
  - Note: If you don't want to have SSL certificate, remove this file and remove the SSL certificate step in `pipeline/helm-deploy.yaml` file

## Multiple Ingress Controller
- Most of the cases, one ingress controller per cluster is sufficient. 
- But if you want to have one ingress controller per environment. (one for dev, one for qa, one for uat, one for prod), in this scenario, add the below to the `environments/*.yaml` files
  ``` yaml
  controller:
    electionID: ingress-controller-leader-dev
    ingressClass: internal-nginx-dev  # default: nginx
    ingressClassResource:
      name: internal-nginx-dev # default: nginx
      enabled: true
      default: false
      controllerValue: "k8s.io/internal-ingress-nginx" 
  ```
- In addition to the above, you need to update the       
    ```yaml
    # azure-pipeline.yaml file 
      chartReleaseName: ingress-nginx-dev
      namespace: ingress-nginx-dev
    ```

## Adding DNS record for your cluster
- If you want to access your deployed app from outside AKS (like from your laptop or from other external services), then you need Ingress Hostname.  You need to create a [snow ticket to create DNS record](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=52ee46ba1b1e51d05daac99f034bcb89) for host_name.
  - Add `A` Record. DNS Name provide the full hostname like `*.code-aks-dev.premierinc.com` and IP, provide the Ingress Controller IP
  - Add `A` Record. DNS Name provide the full hostname like `*.code-aks-qa.premierinc.com` and IP, provide the Ingress Controller IP
- so that, whenever you add new app, you can configure your Ingress to be `app1.code-aks-dev.premierinc.com`
- The Hostname must be same as one in SSL certificate. 

## Appendix
### How to specify/upgrade Nginx Ingress Controller Version?
Based on the official [Nginx Ingress Controller](https://github.com/kubernetes/ingress-nginx?tab=readme-ov-file#supported-versions-table) specify the version in the `Chart.yaml` file. 

### How to create SSL certificate?
- [SSL Certificate Generation Steps](https://github.com/PremierInc/code-devops-documents/blob/main/general/ssl-certificate.md)
- Make sure the final PEM file contains both Certificate & PEM which you can generate by following above document.
- It is app team responsibility to remember the SSL certificate expiry date & renew it accordingly. 

# Reference
- [GitHub: Ingress Nginx](https://github.com/kubernetes/ingress-nginx/)
- [Ingress Nginx Doc](https://kubernetes.github.io/ingress-nginx/deploy/)
- [Multiple Ingress Controller](https://kubernetes.github.io/ingress-nginx/user-guide/multiple-ingress/)
