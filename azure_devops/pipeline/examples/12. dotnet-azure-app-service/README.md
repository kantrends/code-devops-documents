# Purpose
Deployment of sample dotnet microservice to azure cloud service without container

# Pre-requisite
- Follow steps [here](../../troubleshooting.md#azure-arm-service-connection) to create ARM Service Connection.

- App service name will be provided by cloud devops team. No need Service connection for this in ADO. 


# Steps
- Templatized the pipeline build and deployment.
- We push the image to ACR during the deploy step and then deploy to Azure app service. Refer to `pipeline/deployment.yaml` file.
- We need library groups to store **configurations** for your app services.
  - in this example, we have created "library group" `cqdoc-provision-dev-azure` that contains the key/value pairs. The below keys are mandatory as they are used in `deployment.yaml` file. 
    | Name | Value | 
    | --- | --- |
    | AASPNETCORE_ENVIRONMENT | Development |
    | DB_CONNECTION_STRING | ConnectionString |
    | var_az_app_service_rg | RG_CommonEast_LMS | 
    | var_az_app_service | lms_config_service | 
    | var_app_insights | AppInsightsName |
    | var_app_insights_rg | RGAppInsightsName |
    

- This example allows you to do `blue_green` deployment model. 
- We have templatized the pipeline files and check the `pipeline` directory.
- Adjust the appsettings.json file with the correct DB_Connection_String.

