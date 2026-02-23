# Troubleshooting

## 400 Bad Request while uploading package to Nexus
  - `Problem`: It looks like the version you are trying to upload is already present in Nexus.
  - `Solution`: Change the version or add `-SNAPSHOT` to the version. You can push `-SNAPSHOT` versions multiple times whereas you can push non-snapshot versions only once to Nexus when it comes to Maven.

## 404 Not Found or Quarantine
  - `Problem`: The package is blocked by Nexus Firewall as it has vulnerabilities. 
  - `Solution`: Use a non-vulnerable version of the package or use a different package. 

## Pipeline fails due to Connectivity Issue or Network not found or Timeout issue.
  - `Problem`: Firewall issue between our agents and your server.
  - `Solution`: Follow [this document](./agents.md) to raise a Firewall request. 

## Pipeline fails in SSH step and error as All configurated authentication methods failed
  - `Problem`: SSH keys are not configured properly
  - `Solution`: Follow [this document](./ssh-keys-vm-deployment.md) to configure the SSH keys on the server & in ADO service connection 

## Pipelines fails application is not found/invalid in NexusIQ
- `Problem`: The application ID is not present in NexusIQ
- `Solution`: Follow [this document](https://github.com/PremierInc/code-self-service#nexus-iq-application-id-creation) to create app ID in NexusIQ.

## Azure ARM Service Connection
- If your pipeline wants to deploy application to Azure Cloud, we need a Service Connection of type **Azure Resource Manager** for your subscription. 
  - For example, if your subscription name is `SUB_LMS_PROD`, then we need a service connection of type "Azure Resource Manager" in Azure DevOps as `SC_ARM_LMS_PROD`. 

- Only Cloud security team can do this. Open snow ticket with cloud security team for this [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=dd18f4381bbb3050be08975e034bcb37)

  | Field | Value |
  | --- | --- |
  | Requested For | [your name] | 
  | Name | SP_ADO_[project]_NP , SP_ADO_[PROJECT]_PRD (usually this is the SP already available in Azure cloud for each project) | 
  | Purpose | Create ARM Service Connection in Azure DevOps Project: [ADO Project Name] with name SC_ARM_SUB_[PROJECT]_NP, SC_ARM_SUB_[PROJECT]_PRD |
  | Subscription | SUB_LMS_NP, SUB_LMS_PROD |
  | Azure Tenant | Members.  Mostly Members unless you have subscription in CORP Tenant |

## SSH Service Connection
This is used for establishing communication with Linux VM. If you want to copy files to any VM or want to run scripts on remote VM, then you need this service connection. To create SSH Service Connection for a VM:
- Go to Project Settings
- Under pipelines, Select **Service Connection**
- Add New
- Search for `SSH` and select it.
- Fill values
- Make sure the service connection name is in format `[username]_[hostname]`. For example: **scauser_c3duabc1**

## Unauthorized to push Images to ACR
- `Problem`: The Service Connection may not have access to push Images to ACR.
- `Solution`: Please work with Cloud DevOps Team and request them to create the necessary permissions for the SC (Service Connection) to push Images to ACR.


## exec /usr/bin/sh: exec format error in Azure App service Container Logs
- `Problem`: App service accepts only amd64 image. To find architecture, use `docker image inspect [image] | grep -i Archi`. it should be amd64
- `Solution`: Use amd64 Docker Base image.

## large file is not showing or missing after ado pipeline build
- `Problem`: If you have large files in your project and using Git LFS to store it in the repository, then we need to explicitly mention in the pipeline yaml file.
- `Solution`: Add the **checkout** ado task in all build jobs and have `lfs: true` set
  ```yaml
  steps:
  - checkout: self
    lfs: true

  - MavenTask: ..
  ```

## Pipeline fails because of RAM issue
- `Problem`: By default all agents are provided with minimum RAM for the pipeline jobs to run.  Some apps require high RAM to build/deploy their application.
- `Solution`: We have increased RAM on few agents. Configure your pipeline in such a way it picks up the agent that has high RAM using `demands` that demands `SYSTEM_HIGH_RAM`. It's best if you add this specific demand only for the job that requires High RAM and not for all jobs to avoid being in queue since only few agents have high RAM.  for example,
  ```yaml
  jobs:
  - job: build
    pool:
      name: Premier Linux Agents
      demands:
      - SYSTEM_HIGH_RAM
    steps:
    ...
  ```
  Reference: [Specify pool name at jobs level](./linux_pipeline.md#pre-requisite)

## Azure app deployment fails or taking long time
- `Possible Scenario`: 
  - When Previous azure cloud deployment is cancelled in the middle of deployment.
  - When the Azure resource does not have enough compute resource. Like CPU, Memory in App service plan. 
- `Solution`: 
  - Stop the app service & manually restart it from Azure Cloud. Usually for NP, you can do this on own.
  - If the Azure resource does not have enough compute,  work with Cloud DevOps Team to sort it out. 
  - If nothing solves the problem, trigger a new pipeline enabling the "system diagnostics" option. 

## Azure App Service switching slots pipeline fails in Blue/Green deployment
**Scenario 1**:
  - `Problem`: If your staging slot is not healthy, then the switching slot deployment will take a long time or fail
  - `Solution`: Before switching slots, you need to make sure the staging slot application (Blue) is healthy & the URL is reachable. Once it is confirmed, then run the switching slot stage (Green/prod Live) in pipeline.

**Scenario 2**:
  - `Problem`: If your App service plan has insufficient resources, then also switching slots fail.
  - `Solution`: Check the CPU & RAM usage of your app service plan. If anything hits more than 80% or 90%, then reach out to Cloud DevOps to fix the problem.

## Pipeline from Project B unable to download artifacts from project A
- `Problem`: The Project B does not have access to read/download artifacts from Project A pipelines.
- `Solution`: Go to Project B -> Settings -> Settings (Under Pipelines) and disable the "Limit job authorization scope to current project for release pipelines" and "Limit job authorization scope to current project for non-release pipelines" options. 

## Request Microsoft Support for Azure DevOps or Azure Cloud
- Follow the steps given [here](../troubleshooting.md#request-microsoft-support-for-azure-devops-or-azure-cloud) to create a support ticket.

## UseDotNet ADO Task is not installing right DotNet version
- `Problem`: Even though you provide a dotnet version in UseDotNet task, the dotnet CLI is using different DotNet version. This is because Microsoft is not replacing all files when it rolls back to older DotNet versions
-	`Solution`: Provide the installationPath in the task.
 ```yaml
- task: UseDotNet@2
  inputs:
    version: '8.x' 
    installationPath: '$(Agent.ToolsDirectory)/dotnet8' # if you are installing dotnet 9, provide as dotnet9
 ```

## Steps to resolve SSL issue in Azure CLI login
- `Problem`: Unable to run Azure CLI commands and getting SSL Certificate error. This happens because of **NetSkope** installed on your machine that provides a Netskope internal certificate to all outgoing traffic, and that certificate is **not trusted by Azure CLI**. We need to add the NetSkope certificate to the Azure CLI CA Bundle to make the Azure CLI trust the Netskope certificate.
- `Solution`: Download the NetSkope CA certificate from the [http://servers.premierinc.com/certs/] URL and then append the contents of the NetSkope CA PEM file to the Azure CLI CA PEM file located at the paths given below.
### Azure CLI CA PEM File Locations
#### **Windows:**
C:\Program Files\Microsoft SDKs\Azure\CLI2\Lib\site-packages\certifi\cacert.pem
#### **Mac (Intel-based):**
/usr/local/Cellar/azure-cli/<cli_version>/libexec/lib/python<version>/site-packages/certifi/cacert.pem
#### **Mac (Apple Silicon):**
/opt/homebrew/Cellar/azure-cli/<cliversion>/libexec/lib/python<version>/site-packages/certifi/cacert.pem