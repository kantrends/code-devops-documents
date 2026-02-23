# SonarQube .NET Setup

This document outlines the steps to integrate SonarQube with a .NET project for continuous code quality inspection. It also includes a sample pipeline configuration for automated analysis.

## Official Documentation

For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 

## Prepare SonarQube Analysis

The SonarQubePrepare@6 task configures the SonarQube analysis parameters before the build process starts. This task sets up the SonarQube scanner to analyze the project and report results back to the SonarQube server.
```
- task: SonarQubePrepare@6
  inputs:
    SonarQube: '$(SERVICE_CONNECTION)'  # Name of the SonarQube service connection configured in Azure DevOps
    scannerMode: 'MSBuild'              # Scanning mode for .NET projects
    projectKey: 'your-project-key'      # Unique key for the project in SonarQube
    projectName: 'your-project-name'    # Name of the project in SonarQube
    projectVersion: '$(Build.BuildId)'  # Version of the project, typically the build ID
 ```
## Build the .NET Project

The dotnet build command is used to build the .NET project.
```
dotnet build --configuration Release $(solutionFile)
```
**Explanation:**

-configuration Release: Specifies that the project should be built in Release configuration. You can adjust this to Debug if needed.
-$(solutionFile): This variable represents the path to your solution file. Ensure this variable is correctly defined in your pipeline or script.

## SonarQube Quality Gates

SonarQube's Quality Gates help ensure that your code meets specific quality standards before being integrated into the main branch. These gates define pass/fail criteria based on metrics such as:

- Code coverage
- Duplications
- Bugs and vulnerabilities
- Maintainability and reliability

```
 - task: SonarQubeAnalyze@6
```

## Viewing the Analysis Results

After the analysis, you can view the results in the SonarQube dashboard:

1. Navigate to Your Project: Go to the SonarQube server and find your project under the "Projects" tab.
2. Analyze Reports: Review the bugs, code smells, vulnerabilities, code duplications, and coverage metrics.

```
- task: SonarQubePublish@6
```
## Example pipeline for dotnet 
[dotnet-sonarqube-pipeline-setup](./ci.yaml)
