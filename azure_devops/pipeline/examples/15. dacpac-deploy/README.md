# Purpose
Follow this document to deploy your dacpac file to MS SQL Server. 

# Pre-requisite
- Target MS SQL Server version must be 2022 or more than that.  Anything below, this example won't work. 
- ARM Service Connection in Azure DevOps Project.  
  - If you are already using Azure cloud for deploying your other apps, then the ARM service connection will be already present. Mostly the name of SP will be like (SP_ADO_[PROJECTNAME]\_NP and SP_ADO_[PROJECTNAME]_Prd). If you are unsure of the name of the SP, find the SP object ID in ARM Service Connection & search for it in Microsoft Entra in Member Tenant.
  - If ARM is not present, then submit two snow tickets [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=dd18f4381bbb3050be08975e034bcb37). One for NP and One for Prd
    - Name: SP_ADO\_[projectName]_SQL\_NP and SP_ADO\_[projectName]_SQL_Prd
    - Subscription: If not there, just put "None"
    - Tenant: Member
- Add the ARM Service Connection Service Principal to SQL Server. To do this, submit a [snow ticket](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=1d7003e64f3e9200f9c58b8d0210c76e)
  - Select "Add account"
  - Provide the name of the Service Principal.
- Create library group. For example: repo1-dev, repo1-qa, repo1-prod

    | Name | Value |
    | --- | --- |
    | var_db_host | c3dicxdb01 | 
    | var_db_name | dacpac | 


# Steps
- Copy the `pipelines` directory to your source code
- Create pipeline in ADO
- In case, if you get connection error, then submit a Firewall ticket. Check our [troubleshooting doc](../../troubleshooting.md)



> For any issues, reach us at ApplicationDelivery@premierinc.onmicrosoft.com
