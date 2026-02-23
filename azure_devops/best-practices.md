# Best Practices

### Project Description
Give Proper Description to your project. This must include detailed information about your project whether it belongs to SDC16. Project Portfolio / Department / Point of Contact.

### Users
Go through the Permissions & Teams and remove unwanted users. 

### Teams vs Permissions
ADO Team = ADO Board.  Create Teams only if you think you need dedicated ADO Board for them. Or else, create new Permissions group and add users. 

### Boards
TBD

### Pipeline Environments
Create **dev, qa, uat, prod** and reuse the same environments for all pipelines so that you can manage the approvers easily.  Create separate environments only if you think you need different set of approvers or you add VMs to the environments. 

> [!WARNING]
> <p style="color:Red;"> <b>Note:</b> Adding approvers to uat & prod is mandatory to prevent users from accidentally deploying to them.</p>

### Pipeline Library Groups
- Create separate library groups for each environment. 
- Create a shared library group for variables that can be shared by multiple pipelines. For example: `docker-np-creds`, `docker-prod-creds`

### Pipeline Conditions
- Write conditions to the pipeline stages, so that it gets skipped. 
- For example, write condition in prod stage, that only main, release* branch must be deployed.

```yaml
# For Prod & UAT
condition: and(
    succeeded(),
    or(
        eq(variables['Build.SourceBranch'], 'refs/heads/main'),
        startsWith(variables['Build.SourceBranch'], 'refs/heads/release'),
        startsWith(variables['Build.SourceBranch'], 'refs/heads/hotfix')
    )
)

# QA
condition: and(
    succeeded(),
    or(
        in(variables['Build.SourceBranch'], 'refs/heads/main', 'refs/heads/develop'),
        startsWith(variables['Build.SourceBranch'], 'refs/heads/release'),
        startsWith(variables['Build.SourceBranch'], 'refs/heads/hotfix')
    )
)
``` 

### Pipeline Approvals
In addition to environment approvals, you can also have approvers in library groups, service connection for additional security.

### Pipeline Deploy to Specific Environment
Use Parameters to choose the environment to deploy and do not use "Stages to Choose" while you manually run pipeline.

```yaml
pool: Premier Linux Agents
parameters:
- { name: dev, default: true, type: boolean }
- { name: prod, default: false, type: boolean }
 
stages:
- stage: ci
  jobs:
  - job: build
    steps:
    - bash: echo 'hi'
 
- stage: dev
  dependsOn: ci
  condition: and(succeeded(), eq('${{ parameters.dev }}', 'true') )
  jobs:
  - job: build
    steps:
    - bash: echo 'hi'
 
- stage: prod
  dependsOn: ci
  condition: and(succeeded(), eq('${{ parameters.prod }}', 'true'), eq(variables['Build.SourceBranch'], 'refs/heads/main') )
  jobs:
  - job: build
    steps:
    - bash: echo 'hi'
```

### Pipeline VM deployments
- If you are writing a pipeline to deploy to VM or making changes to existing pipelines to deploy to a VM, as a pre-requisite log a [⁠snow ticket](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=3ac535e84f278600f9c58b8d0210c754) to take a VM snapshot before doing deployment.  So that, in case if you unintentionally removed or modified files on the server, you can restore it from snapshot. 

- Also, before every prod deployment, it is best to take a VM snapshot. 
