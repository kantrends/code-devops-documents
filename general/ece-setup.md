# Purpose
ECE (Elastic Cloud Enterprise) stack setup for your application.  This document explains the steps to configure ECE stack in ECE portal

# Architecture 
This is our Cloud ECE portal: https://eceadminui.premierinc.com/deployments 

In this we have created two deployments: 
- ImpaQT-NP 
- ImpaQT-Prod 

Each deployment is a stack that has ElasticSearch, Kibana.   Once you created the deployment, you can find the elastic search & kibana URL like below. 

| Env | ElasticSearch | Kibana |
| --- | --- | --- |
| NP | https://5abcdoahd.ece.premierinc.com:443/ | https://asdads.ece.premierinc.com:443/ 
| Prod | https://adfasdfa.ece.premierinc.com:443/ | https://adsfasdddde.ece.premierinc.com:443/ 

 
# Authentication 
By default each stack has an Admin account with username: "elastic" and save the password securely (for ex: 1password)

In addition to this admin account, we can configure Azure AD SAML setup (official doc in reference section). You need to submit snow ticket to request [SAML setup](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=0cc4c7ec870d7150822b8409dabb3592) in Microsoft Entra.

 
| Env | Enterprise Application | App Registration |
| --- | --- | --- |
| NP | IMPAQT-NP-ECE-STACK | IMPAQT-NP-ECE-STACK 
| Prod | IMPAQT-PROD-ECE-STACK | IMPAQT-PROD-ECE-STACK 


# Authorization: 
For application teams, Authorization is handled using Azure AD Groups. In the Kibana portal, the following "RoleMapping" has been configured 

| Azure AD Groups | Roles |
| --- | --- |
| impaqt-ece-admins | superuser |
| Devops_impaqtgateway | viewers |

 
For Filebeat to send data to elastic search, we have created the following in the Kibana portal: 

- custom Role: "FILEBEAT-ROLE" 

  ![Filebeat Role](./resources/filebeat-ece-role.png)

- Create user "filebeat_user1" and assigned the above role to it.


This user credentials is configured in ADO pipeline: "ece-np-creds" and "ece-prod-creds". 

Save the password securely.
 

# Troubleshooting 
- QQ: Whom to reach for any issues in ECE stack? 
  
  Venu Kalva's Team is responsible for the ECE platform.  

- Aakash Selvaraj helped ImpaQT Team in setting up the deployments.  

 
# Reference: 
- [Azure AD SAML official document](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/saml-entra)

 