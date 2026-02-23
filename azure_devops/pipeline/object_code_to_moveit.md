# Purpose
This document contains steps on how to copy your object code (war/jar/etc.,) to MoveIT as part of the Enterprise License Agreement.

# Options
- **Option 1:** Copy a single object code to MoveIT as soon as the production deployment is successful.
- **Option 2:** A separate Pipeline that copies all the object code from Nexus to MoveIT.

## Option 1: Copy the object code to MoveIT as part of the Production pipeline
Use this method if you want to copy the object code to MoveIT once your prod deployment is successful.  Also, this method requires you to modify all your pipelines to add the sftp-to-moveit YAML template so that as soon as the prod deployment is successful, it copies the object code (war/jar/etc.,) to MoveIT.

### Pre-requisite
- Get access from **Geoff Vallano** to the MoveIT Server: `https://sdt.premierinc.com/`
- Ask Geoff to create a service user for you to use in your pipelines. You’ll need to give him an ssh key pair to associate with it. You can generate one with the command: 
  ```bash
  ssh-keygen -b 4096 -t rsa -m pem -f moveitkey
  ```
  This will create two files: `moveitkey` and `moveitkey.pub`. Give the .pub file to Geoff.
- Upload the private key `moveitkey` in **ADO Pipeline -> Library -> Secure File**. Give it a name: **moveit-private-key**
- If the Target directory in Moveit does not already exist, ask for Geoff to create your directory in moveit. 
- Make sure that your service user can overwrite files located in your moveit directory.

### Pipeline Step
- Use the `sftp-to-moveit.yaml` template file in [PremierInc/shield-ado-templates](https://github.com/PremierInc/shield-ado-templates) repository.
- Make sure the template is called after your production deployment. Set up your deployments to use your new task on deployment success.
- We’ve included a task yaml file as a baseline for what this task would look like. Feel free to use it and change it to your use case.  

```YAML
# Example

resources:
  repositories:
    - repository: sdlc_templates
      type: github
      endpoint: PremierInc
      name: PremierInc/shield-ado-templates

stages:
- stage: 'PROD'
  jobs:
  - deployment: 'PROD_DEPLOY'
    environment: PROD
    strategy:
      runOnce:
        deploy:
          steps: [
            # pretend some deployment steps are here
          ] 
        on:
          success:
            steps: 
            # Download the pipeline artifact that contains your object code. It stores in location $(Pipeline.Workspace)/drop
            - download: current
              artifact: drop # artifact name created during build stage
 
            # if the object code is in nexus. write a bash script to download it
            # - bash: |
            #           wget -O hello.jar https://<nexus download url>

            # Assuming the SFTP Private Key is stored in ADO Secure File in the name: "sftp-moveit-private-key"
            - template: sftp-to-moveit.yaml@sdlc_templates
              parameters:
                USERNAME: coderepomvit
                HOSTNAME: sdt.premierinc.com
                SFTP_IDENTITY_ADO_SECURE_FILE: sftp-moveit-private-key 
                FILES: 
                - SOURCE_FILE: $(Pipeline.Workspace)/drop/hello-$(PROJECT_VERSION).jar
                  TARGET_FILE: hello.jar
                  TARGET_DIRECTORY: "/Code_Repo/master/Workforce Management/OperationsAdvisor"

                - SOURCE_FILE: $(Pipeline.Workspace)/drop/hello-$(PROJECT_VERSION).jar
                  TARGET_FILE: hello.jar
                  TARGET_DIRECTORY: "/Code_Repo/master/Workforce Management/OperationsConsumer"
```

## Option 2: A separate Pipeline that copies all the object code to MoveIT.
In this option, you will have a separate repository to maintain a config file and a separate pipeline for copying all object code from Nexus to MoveIT.

> **Note: This option is possible only when all your object codes (war, jar, etc) are in Nexus**

### Pre-requisite
- Get access from **Geoff Vallano** to the MoveIT Server: `https://sdt.premierinc.com/`
- Ask Geoff to create a service user for you to use in your pipelines. Get the username & password for the service user. We need to save them in `Azure Pipelines -> Library`.
- Create a library group called `moveit-creds` and save the credentials in this key/value format. **Note**: Replace the Value column with your service user credentials. 

    | Key | Value |
    | --- | --- |
    | MOVEIT_USERNAME | service_user1 | 
    | MOVEIT_PASSWORD | iamironman |

- Create a new GitHub repository. For example, `code-moveit`.
- Create a `config.yaml` file with contents like below:
  - specify your product name
  - moveit directory full path. 
  - nexus coordinates. 
```YAML
# config.yaml
- product_name: "ABC" # without spaces
  moveit_directory: "/ObjectCode/WorkForceManagement"
  applications:
  # pip is for python. downloads from "premier-pypi"
  - pip: remitra-py-settings1:latest  # or remitra-py-settings:0.2.0
  # gav is for maven "releases"
  - gav: com.premierinc.shield:cx-wra1per-script:0.9:zip:Checkmarx
    bundle: true # default true. Accepted values true/false
  - gav: com.premierInc.shield:cx-wrapP1er-script:latest:zip
  # npm uses "premier-npm"
  - npm: ciam-idly-timeout:1.1.1
  - npm: ciam-idly-timeout:latest
  - gav: com.premierhelp.users.web:IAMRestStopper:latest

- product_name: "XYZ" # without spaces
  moveit_directory: "/ObjectCode/WorkForceManagement"
  applications:
  - gav: com.premierinc.shieldaget:cx-avengers-script:0.9:zip:Checkmarx
    bundle: true # default true. Accepted values true/false
  - gav: com.premierinc.shieldprotector:cx-wrappersin-script:latest:zip
  - npm: ciam-idly-timeoutPass:1.1.1
  - npm: ciam-idly-timeoutabc:latest
```

### Pipeline Steps
- Create the `azure-pipeline.yaml` pipeline file and have the below contents. In this pipeline, we are using a template file `moveit_template.yaml` from [PremierInc/code-nexustomoveit](https://github.com/PremierInc/code-nexustomoveit) repository that has the automation script to download the object code from Nexus and copying it to MoveIT.
```YAML
# azure-pipeline.yaml file
trigger: none 
pr: none 

pool: Premier Linux Agents

resources:
  repositories:
    - repository: moveit
      type: github
      name: PremierInc/code-nexustomoveit
      endpoint: PremierInc

variables:
- group: moveit-creds

steps:
- template: moveit_template.yaml@moveit
  parameters:
    # your repository name / <config> file name
    # in this example, repo name is code-moveit-sandbox and config file name is config.yaml
    config_file: code-moveit-sandbox/config.yaml
```
- Create a Pipeline in ADO. 
- Run the pipeline. This will download the object code from nexus, zip them and push to MoveIT. 