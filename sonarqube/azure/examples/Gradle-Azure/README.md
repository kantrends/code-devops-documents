# SonarQube Gradle Setup

This document outlines the steps to integrate SonarQube with a Gradle project for continuous code quality inspection.

## Official Documentation
For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 

## Gradle Build Configuration
To enable SonarQube scanning in your Gradle project, add the SonarQube plugin to your build.gradle file.

```
plugins {
    id "org.sonarqube" version "4.0.0.2929"
}
```

Specify Compiled Classes Location

Make sure to specify the path to the compiled classes in your pipeline or in the SonarQube properties. For a typical Gradle project, the compiled classes are located in:
```
build/classes/java/main
```
You can add this property in your pipeline configuration:

```
extraProperties: |
  sonar.java.binaries=gradle-project/build/classes/java/main
```
## Prepare SonarQube Analysis

The SonarQubePrepare@6 task configures the SonarQube analysis parameters before the build process starts. This task sets up the SonarQube scanner to analyze the project and report results back to the SonarQube server.
```
- task: SonarQubePrepare@6
  inputs:
    SonarQube: '$(SERVICE_CONNECTION)'           # Name of the SonarQube service connection configured in Azure DevOps
    scannerMode: 'CLI'                           # Scanning mode for Gradle projects
    projectKey: 'your project key'  # Unique key for the project in SonarQube
    projectName: 'your project name' # Name of the project in SonarQube
    extraProperties: |
      sonar.java.binaries=gradle-project/build/classes/java/main  # Path to compiled classes
```
## Build the Gradle Project

The Gradle build command is used to build the project and run SonarQube analysis.
```
- script: |
    chmod +x ./gradlew
    ./gradlew build  # Compile the project and run SonarQube analysis
  displayName: 'Run Gradle Build'
  env:
    JAVA_HOME: $(SYSTEM_JDK_17)
```

## SonarQube Quality Gates
SonarQube's Quality Gates are essential for ensuring that your code meets certain quality standards. These gates define pass/fail criteria based on various metrics, such as:

- Code Coverage: The percentage of code covered by unit tests.
- Duplications: Identifies duplicated blocks of code.
- Bugs and Vulnerabilities: Detects potential bugs and security issues.
- Maintainability and Reliability: Measures code complexity and robustness.

```
- task: SonarQubeAnalyze@6
```

## Viewing the Analysis Results
After running the analysis, you can view the results in the SonarQube dashboard:

- Navigate to Your Project: Access your SonarQube server and find your project under the "Projects" tab.
- Analyze Reports: Review the detailed reports that cover bugs, code smells, vulnerabilities, code duplications, and code coverage.

```
- task: SonarQubePublish@6
```
## Example pipeline for Gradle 
[Gradle-sonarqube-pipeline-setup](./ci.yaml)

