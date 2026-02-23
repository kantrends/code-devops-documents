# SonarQube Maven Setup

This document outlines the essential steps to integrate SonarQube with a Maven project for continuous code quality inspection.

## Official Documentation

For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 


## Maven POM Configuration

Add the SonarQube Scanner Plugin to your pom.xml file:

```
<build>
    <plugins>
        <plugin>
            <groupId>org.sonarsource.scanner.maven</groupId>
            <artifactId>sonar-maven-plugin</artifactId>
            <version>3.9.1.2184</version>
        </plugin>
    </plugins>
</build>
```

## Run Maven build with SonarQube analysis

You can run the SonarQube analysis with a simple Maven command:
```
- task: Maven@4
  inputs:
   mavenPomFile: 'maven-project/pom.xml'
   goals: 'clean verify'
   options: '-DskipTests=true -Dsonar.branch.name=' 
   publishJUnitResults: true
   javaHomeOption: 'Path'
   jdkDirectory: $(SYSTEM_JDK_17)
   mavenVersionOption: 'Path'
   mavenDirectory: $(SYSTEM_MAVEN_3_HOME)
   sonarQubeRunAnalysis: true # This enables SonarQube analysis during the build
```

Setting sonarQubeRunAnalysis: true in the Maven task enables the SonarQube analysis to be executed as part of the Maven build process. This integration allows SonarQube to analyze the code during the build phase, providing immediate feedback on code quality without needing a separate analysis step.

## Viewing the Analysis Results

After the analysis, you can view the results in the SonarQube dashboard:

1. Navigate to Your Project: Go to the SonarQube server and find your project under the "Projects" tab.
2. Analyze Reports: Review the bugs, code smells, vulnerabilities, code duplications, and coverage metrics.

```
- task: SonarQubeAnalyze@6
```

## Example pipeline for maven
[maven-sonarqube-pipeline-setup](./ci.yaml)
