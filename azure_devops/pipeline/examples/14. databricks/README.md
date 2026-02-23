# Databricks DevOps Document

Welcome! This repository contains all the documents to automate Databricks workspace management and deployments.

# Pre-requisite:
- The service principal used in Azure Resource Manager service connection needs to be added to Databricks by Databricks Admin.
- The Databricks Admin needs to generate OAuth Client Secret. That is used to configure it in the pipeline.
- Details of **azure_subscription_sc**
- **Workspace host link** to connect with the databricks host.

# Steps to follow:
- Create the pipeline as given in the [example](./pipelines/)
- This is how **Variable group** in pipeline's **Library** looks like:
  ![{FCEE1818-B930-4EF5-81D2-7C47659DE398}](https://github.com/user-attachments/assets/c762da1c-920b-401a-b165-ceee52db0fc1)
- Update **azure_subscription_sc** and Variable name for: **Database client secret** in the pipeline to authenticate into their databricks workspace.
- Confirm the path from the reporter.
- Create a **databricks.yml** file as [this](./databricks.yml) and update the **Workspace host link**.
- Create a Bundle file in resource folder [like this](./resources/) which gives command to databricks cli.
- Create a sample python notebook and place it in notebooks directory to check the execution [like this](./notebooks).
- Cross check with the app team whether the file is uploaded to the desired location.
