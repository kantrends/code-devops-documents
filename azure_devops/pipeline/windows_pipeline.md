# Azure DevOps Linux Pipeline
This document contains various pipeline steps that can be followed in Azure DevOps Pipeline for different use cases when you are using **Premier Self Hosted Windows Agents**.

# Table of Contents

- [Pre-requisite](#pre-requisite)
- [Environment Variables](#environment-variables)
- [Pipeline Steps](#pipeline-steps)
  - [DotNet](#dotnet)
  - [NuGet](#nuget)
  - [Python](#python)
- [Appendix](#appendix)

# Pre-requisite
Premier Agents are hosted within the Premier network that provides access to other applications that are hosted within Premier. For example, **[Nexus](https://nexus.premierinc.com/artifacts)** application.  In order to use Premier Agents in your pipeline, specify the Pool name in the pipeline YAML code.  

### Pipeline level
If you want your entire pipeline to be executed in Premier agents, then specify
```YAML
pool:
  name: "Premier Windows Agents"
```

### Stage level
If you want to run a specific stage in Premier agents, then specify
```YAML
stages:
- stage: Build
  pool: "Premier Windows Agents"
  jobs:
  - job: ...
```

### Job Level
If you want to run a specific job in Premier agents, then specify
```YAML
jobs:
- job: ABC
  pool: "Premier Windows Agents"
```

# Environment Variables
The following environment variables are available on the agent. 
| Env Variable | Value | 
| --- | --- |
| SYSTEM_CHROMEDRIVER_EXE | c:\seleniumdrivers\chromedriver.exe |
| SYSTEM_MSEDGEDRIVER_EXE | c:\seleniumdrivers\msedgedriver.exe |
| SYSTEM_JDK_11 | C:\Program Files\Eclipse Adoptium\jdk-11 |
| SYSTEM_JDK_17 | C:\Program Files\Eclipse Adoptium\jdk-17 |
| SYSTEM_JDK_8 | C:\Program Files\Eclipse Adoptium\jdk-8 |
| SYSTEM_MAVEN_3 | C:\ProgramData\chocolatey\lib\maven\apache-maven-3\bin\mvn |
| SYSTEM_MAVEN_3_HOME | C:\ProgramData\chocolatey\lib\maven\apache-maven-3 |
| SYSTEM_PYTHON_310_HOME | D:\Packages\Python310 | 
| SYSTEM_PYTHON_310_USER_SCRIPTS | C:\Users\svc_code_ado\AppData\Roaming\Python\Python310\Scripts | 
| SYSTEM_PYTHON_314_HOME | D:\Packages\Python314 | 
| SYSTEM_PYTHON_314_USER_SCRIPTS | C:\Users\svc_code_ado\AppData\Roaming\Python\Python314\Scripts | 
| SYSTEM_NUGET_CONFIG | C:\Program Files (x86)\NuGet\Config\NuGet.config |
| SYSTEM_PYTHON | python | 
| SYSTEM_SQLPACKAGE | D:\Packages\SqlPackage\sqlpackage.exe | 

# Packages on the Agent

## Packages
- JDK 8/11/17
- Apache Maven 3
- DotNet Framework 4.5/4.6/4.7/4.8
- Visual Studio 2022 Community
- Visual Studio 2019 Community
- Python
- Az Copy
- Azure CLI
- DotNet
- DotNet Core
- Browsers
  - Google Chrome
  - Microsoft Edge
- Git
- Powershell Core
- DAC Framework 18
- SQL Package
- made2010

## Powershell Modules
- MicrosoftPowerBIMgmt
- AzureAD
- MSOnline
- SQL Server

# Pipeline Steps

## DotNet

**Option 1:** Command line
```YAML
- powershell: dotnet restore
```

**Option 2:** DotNetCore ADO Task
```YAML
- task: DotNetCoreCLI@2
  displayName: 'dotnet restore'
  inputs:
    command: 'restore'
    feedsToUse: 'config'
    nugetConfigPath: $(SYSTEM_NUGET_CONFIG) # uses NuGet.Config file on the Agent.
    projects: '**/*.csproj'
    includeNuGetOrg: false 
```

## NuGet

**Option 1:** Command line
```YAML
- task: NuGetToolInstaller@1
  displayName: Install NuGet

- powershell: nuget restore abc.sln
  displayName: NuGet Restore
```
**Option 2:**  NuGet Command ADO Task
```YAML
- task: NuGetToolInstaller@1
  displayName: Install NuGet

- task: NuGetCommand@2
  inputs:
    command: 'restore'
    restoreSolution: '**/*.sln'
    includeNuGetOrg: false
    feedsToUse: 'config'
    nugetConfigPath: $(SYSTEM_NUGET_CONFIG) # uses NuGet.Config file on the Agent.
```

## Python
We have python installed on the build agents. You have to configure it to the PATH as below. 
```YAML
- powershell: |
    Write-Host "##vso[task.prependpath]$(SYSTEM_PYTHON_314_HOME)"
    Write-Host "##vso[task.prependpath]$(SYSTEM_PYTHON_314_HOME)\Scripts"
    Write-Host "##vso[task.prependpath]$(SYSTEM_PYTHON_314_USER_SCRIPTS)"
  displayName: 'Set python in path'

- powershell: python --version
- powershell: python -m pip install -r requirements.txt
- powershell: python file.py
```

# Appendix
- To upload packages to Nexus, please check [this document](./upload_nexus_artifacts.md)
- Sample `NuGet.Config` file pointing to Nexus can be found [here](../../nexus/repository_manager/nexus_in_local.md#nuget)
