# Azure Static Web App Deployment
Pipeline example for deploying static NPM static web app to Azure static web app

## Pre-requisite
- Make sure the azure static web app is created in azure cloud.  Work with Cloud DevOps Team for this.
- Copy the Static Web App API deployment token from Azure Cloud and create Library Group in Azure DevOps for each environment to store the Static Web App API Token. For example: static-web-app-dev
    | Name | Value |
    | --- | --- |
    | AZ_STATIC_WEB_APP_TOKEN | abcxys123 | 

## Steps
- Copy the templates from this example to your repository.
- In this example, we used PNPM to build the project. Customize it according to your project build tool.
- In this example, the generated static web app contents (index.html & other JS files) are stored in _webapp/static_ directory. Hence creating artifact for that location.  Customize it according to your project. 

## Reference:
- AzureStaticWebApp ADO Task [official document](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/azure-static-web-app-v0?view=azure-pipelines)
- Steps to retrieve [Azure Static API deployment Token](https://learn.microsoft.com/en-us/azure/static-web-apps/deployment-token-management#reset-a-deployment-token)
- Azure static web app [document](https://learn.microsoft.com/en-us/azure/static-web-apps/)
