# Purpose
Deployment of sample NodeJS app to app service without container.  For example, we used simple express framework and PNPM to handle dependencies

# Pre-requisite
- Follow steps [here](../../troubleshooting.md#azure-arm-service-connection) to create ARM Service Connection.


# Steps
- Templatized the pipeline build and deployment.
- In ci.yaml file, (build)
  - we install PNPM dependencies and package the application as a zip file.
  - create artifact of the zip file.
- In deploy.yaml, (deploy)
  - we deploy to native apps.
  - Default `StartUpCommand`: npm start in Azure App service. You may need to make changes to the `StartUpCommand` in the deploy.yaml file if required as it varies for each framework. 

- Create ADO Library Group 

| Name | Value |
| --- | --- |
| var_app_insights | qualadv-webui-dev_webinsight |
| var_app_insights_rg | qualadv-east |
| var_az_app_service | qualadv-webui-dev |
| var_az_app_service_rg | qualadv-east |

