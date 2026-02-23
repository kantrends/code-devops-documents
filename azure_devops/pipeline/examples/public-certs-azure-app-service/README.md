# Purpose
Find steps on how to add Public Certificates to Azure App Service.  

In App Service, your application runs on HTTP (non-TLS) mode. By default, Azure has default trust certificates like Digicert. So if your app wants to talk to another HTTPS service which has Digicert certificate, it will work without any issue. 

But, if your application wants to communicate with another service that is running on HTTPS and is using custom certificate provided by PremierInc CA or custom CA, then you need to add the PremierInc CA certificate or custom CA certificate to Azure app service. 

>Note: This is useful for non-Container based deployments. For Container based, add the truststore as part of Docker Image. 

# Steps to add Public Certificates to App Service
- The logic for preparing and uploading certificates resides in the `update-ca.yaml` file.
- Copy the `update-ca.yaml` template.  This job runs only on windows agents.
- `Includes PremierPKI root CA certificates` stored in the `certs/`directory.
- Add the `update-ca.yaml` job as a template in your `deploy.yaml` file.

# How to update SSL Certificate
- SSL Issue happens when the external URL you are trying to access has updated their SSL certificate.
- In this scenario, you need to update the new SSL certificate to your application.
- If the SSL issue happens in Azure App service, then open the `update-ca.yaml` file in your pipeline repo.
  - Locate the openssl s_client command under the task Generate CA Certificates using OpenSSL..
  - Update the hostname to point to the target service whose certificate has changed.
- Commit the changes and trigger your pipeline.

The pipeline will:
- Regenerate the certificate.
- Delete old certificates from the Azure App Service.
- Upload the new certificate automatically.

- Once done, build the app & deploy to production. this updates the SSL certificate in Azure App Service.
