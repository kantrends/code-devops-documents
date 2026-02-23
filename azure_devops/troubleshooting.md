# Troubleshooting / FAQ

## New Project in Azure DevOps
- Check if you can use any existing projects. Prefer creating new project only if you are going to use "Azure Boards" in that project. If not, use an existing project itself. 
- Create a support ticket [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=d7f4cf011bbd3450be08975e034bcb58) if you want to create a new project. 

## User unable to view project even though part of AD group
- Microsoft mentioned the sync occurs every 1 hour and sometimes every 24 hours.
- **Solution**: Open this URL in browser: `https://dev.azure.com/premierinc/_usersSettings/permissionsRefresh` and hit `Re-evaluate permissions` which will refresh permissions. After that, open the ADO portal in Incognito or In-Private window.

## Update Service Line in ADO Project
- Kindly follow our self-service [document](https://github.com/premierinc/code-self-service?tab=readme-ov-file#update-service-line-in-ado-project) to update the service line in your ADO project.
- Please do not modify the ADO project description manually, it needs to be done as mentioned in the document.
- If you think your service line is missing, then kindly send email to **Application Delivery** Email DL
