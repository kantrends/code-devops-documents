# Library

Use Library in Azure DevOps Pipeline to store variables and secret files.  You can then refer the variables & secret files in your YAML pipeline configuration.  This document explains how the variables groups and secret/secure files can be used in YAML pipeline configuration.

# Table of Contents
- [Variable Groups](#variable-groups)
- [Secure Files](#secure-files)
- [Reference](#reference)

# Variable Groups
There are multiple places where you can configure variables for your pipeline:
- In the YAML file, `variables` section.
- In the YAML, Edit UI (not preferred).
- In the Library as variable groups.

You can combine multiple variables into group and use that group in your pipeline.  Let's see some of the use cases where the `variable groups` makes more sense than normal variable declaration in the pipeline.

Let's see few use cases where variable groups are best used.

---

## Use Case 1: Docker Credentials
- We have two set of Docker credentials, one for non-prod (**docker-np-creds**) and one for prod (**docker-prod-creds**).  Each contains two variables `DOCKER_USERNAME` and `DOCKER_PASSWORD` as in below image:

  ![docker-np-creds](https://github.com/PremierInc/code-devops-documents/blob/main/azure_devops/pipeline/resources/docker-np-creds.PNG?raw=true)

- To use those two variables in pipeline, add yaml configuration as below: 
  ```YAML
  - jobs: 
    - job: np_deploy
      variables:
      # variable group declaration
      - group: docker-np-creds
      steps:
      - bash: echo $DTR_USERNAME ; echo $DTR_PASSWORD   # print non prod credentials
        env:
          DTR_USERNAME: $(DOCKER_USERNAME)
          DTR_PASSWORD: $(DOCKER_PASSWORD)

    - job: prod_deploy
      variables:
      - group: docker-prod-creds
      steps:
      - bash: echo $DTR_USERNAME ; echo $DTR_PASSWORD   # print prod credentials
        env:
          DTR_USERNAME: $(DOCKER_USERNAME)
          DTR_PASSWORD: $(DOCKER_PASSWORD)
  ```

- We can use the above two variable groups in the Continuous Integration (CI) process while building & pushing Docker Image to DTR and also for authenticating to UCP cluster during deployment.

---

## Use Case 2: Deployments
Variable Groups are most useful during the application deployments in different environments.  

**For example**, say you need 6 variables to be configured for Dev environment deployment.  The same 6 variables is needed for QA environment deployment but will hold different values.  In this case, you can create variable groups for each deployments and use it in the YAML pipeline configuration.

In the below YAML configuration, we have used two variable groups `example-dev` and `example-qa`.  Both group holds the same variable `DB_USER` but with different values.  Based on the variable group declaration at the stage/job level, right value is taken from right variable from right variable group. 

```YAML
stages:
- stage: dev
  jobs:
  - job: dev_deploy
    variables:
    - group: example-dev
    steps:
    - bash: echo $(DB_USER)   # print value of DB_USER variable stored in example-dev variable group

- stage: qa
  jobs:
  - job: qa_deploy
    variables:
    - group: example-qa
    steps:
    - bash: echo $(DB_USER)     # print value of DB_USER variable stored in example-qa variable group
```

> NOTE: When you configure any variable as secret (value hidden) in the variable group, then we need to explicitly pass then as ENV variable to the task. For example, assume you have DB_PASS variable and it is made secured (value hidden), then you have to pass them explicitly as mentioned in below yaml configuration

```YAML
jobs:
- job:
  variables:
  - group: example-dev      # this variable group has variable 'DB_PASS'
  steps:
  - bash: echo $DB_PASSWORD
    env:
      DB_PASSWORD: $(DB_PASS)       # explicitly assigning DB_PASS to DB_PASSWORD env variable.
```

# Secure Files

[Official Document](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/secure-files?view=azure-devops) from Microsoft explains about the usage of Secure Files. 

# Reference

- Official Microsoft Document on [Variables](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch)
- Official Microsoft Document on [Variable Groups](https://docs.microsoft.com/en-us/azure/devops/pipelines/scripts/cli/pipeline-variable-group-secret-nonsecret-variables?view=azure-devops)
- Official Microsoft Document on [Secure Files](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/secure-files?view=azure-devops)
