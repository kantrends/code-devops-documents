# Vault in ADO Pipeline
This document covers steps on the usage of vault in the ADO pipeline

# Vault Authentication
In order for pipeline to access vault and retrieve secrets, our team has created two library groups in Azure DevOps pipeline
- vault-authentication-np
- vault-authentication-prod

We will be using these library groups while fetching the secrets from vault based on the secret engine.  If you want to retrieve secrets from **np** secret engine, then use variable group **vault-authentication-np**


# Use KV secret in Linux pipeline

- Our team has written an ADO Tasks Template to retrieve secrets. To use that, first step is to add the template file to your pipeline yaml file.
  ```yaml
  resources:
    repositories:
      - repository: code_templates
        type: github
        name: PremierInc/code-ado-templates
        endpoint: PremierInc
  ```
- Add the vault authentication library group to the stage/job.
  ```yaml 
  stages:
  - stage: dev 
    variables: 
      - group: vault-authentication-np

  - stage: prod 
    variables:
      - group: vault-authentication-prod 
  ```
  or
  ```yaml
  jobs:
  - job: ci 
    variables: 
      - group: vault-authentication-np

- Add the template to your pipeline steps
  ```yaml
    steps:
    - template: vault-kv-template.yaml@code_templates
      parameters: 
        VAULT_ADDR: 'https://vault.premierinc.com'
        MOUNT_ENGINE: 'sandbox-np' 
        VAULT_PATH: 'pipeline-1/dev'
        VAULT_SECRETS: 
        - VAULT_FIELD: 'username'
        - VAULT_FIELD: 'password'
          OUTPUT_VAR: 'db_password'
        - VAULT_FIELD: 'user_json'
          OUTPUT_TYPE: 'SECRET_FILE'
          OUTPUT_VAR: 'user_json_data'
        - VAULT_FIELD: 'private_key'
          OUTPUT_TYPE: 'SECRET_FILE'
  ```
  - **VAULT_ADDR** (_Optional_): Vault Application URL.
  - **MOUNT_ENGINE**: Secret Engine. For example, _{project}-np_ or _{project}-prod_
  - **VAULT_PATH**: path to your secret inside the secret engine.
  - **VAULT_SECRETS**:  Array of secrets that needs to be retrieved.
    - **VAULT_FIELD**: Secret "key" name.  
    - **OUTPUT_VAR** (_Optional_): If you provide this, secret value is stored in this variable. If it is not specified, then the secret value is stored in the variable mentioned in the VAULT_FIELD.
    - **OUTPUT_TYPE** (_Optional_): Accepted values [SECRET_FILE or SECRET_VAR].   Default: SECRET_VAR.  
      - SECRET_VAR will store the secret as a variable. 
      - SECRET_FILE will store the secret in a file.  
        >**Note: We strongly recommend to use this if your secret contains multi-line statements like JSON file, Private key, Config files.** 

- You can use the retrieved secrets in the pipeline like below if the OUTPUT_TYPE is **SECRET_VAR**
  ```yaml 
  - task: SSH@0
    inputs:
      sshEndpoint: 'c3cuabc123'
      runOptions: 'inline'
      inline: |
        echo "dbb: $(username)"
        echo "DB_username: $(username)" > /tmp/a
        echo "DB_PASSWORD: $(db_password)" >>  /tmp/a 
      readyTimeout: '20000'
  ```
- You can use the retrieved secrets in the pipeline like below if the OUTPUT_TYPE is **SECRET_FILE**
  ```yaml
  - bash: ssh -i $(private_key) USER@IP whoami
  - bash: cat $(user_json_data)
  ```

- Below is the combined ADO PIpeline: the kv template will try to retrieve the secret from sandbox-np secret engine and use the vault path "pipeline-1/dev". At one shot, we pulled four secrets from vault and assign it to the variable/file. 

  ```yaml
  resources:
    repositories:
      - repository: code_templates
        type: github
        name: PremierInc/code-ado-templates
        endpoint: PremierInc

  stages: 
  - stage: ci 
    variables: 
    - group: vault-authentication-np
    jobs:
    - job: build
      steps:
      - template: vault-kv-template.yaml@code_templates
        parameters: 
            VAULT_ADDR: 'https://vault-np.premierinc.com'
            MOUNT_ENGINE: 'sandbox-np' 
            VAULT_PATH: 'pipeline-1/dev'
            VAULT_SECRETS: 
            - VAULT_FIELD: 'username'
            - VAULT_FIELD: 'password'
              OUTPUT_VAR: 'db_password'
            - VAULT_FIELD: 'user_json'
              OUTPUT_TYPE: 'SECRET_FILE'
            - VAULT_FIELD: 'private_key'
              OUTPUT_TYPE: 'SECRET_FILE'

      - task: SSH@0
        inputs:
          sshEndpoint: 'c3cucode01'
          runOptions: 'inline'
          inline: |
            echo "dbb: $(username)"
            echo "DB_username: $(username)" > /tmp/a
            echo "DB_PASSWORD: $(db_password)" >>  /tmp/a 
          readyTimeout: '20000'
  ```
