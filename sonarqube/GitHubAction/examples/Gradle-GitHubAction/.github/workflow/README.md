# SonarQube Setup for Gradle with GitHub Actions
This document outlines the essential steps to integrate SonarQube with a Gradle project using GitHub Action for continuous code quality inspection.

## Official Documentation
For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 

## Prerequisites
Before you start configuring the pipeline for SonarQube integration, ensure you meet the following prerequisites:

GitHub Repository Setup:

- Your repository must have a .github/workflows/ directory.
- The pipeline YAML file should be placed in .github/workflows/sonarqube.yaml.

## Gradle Build Configuration
To enable SonarQube scanning in your Gradle project, add the SonarQube plugin to your build.gradle file.

```
plugins {
    id "org.sonarqube" version "4.0.0.2929"
}
```
## GitHub Action Tasks for Gradle
### 1. Checkout the Code
This step checks out the project's code from the repository to the runner .
- fetch-depth: 0: This setting ensures that the entire Git history is cloned, not just the latest commit. SonarQube may use the full Git history for accurate analysis, particularly for blame-based analysis.
```
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Disable shallow clone for better analysis accuracy
```
### 2. Set up JDK 
This step sets up JDK  as the default Java version for the workflow. It configures the environment so that Java-based tools like Gradle can find the JDK.
```
- name: Set up JDK 17
  uses: actions/setup-java@v4
  with:
      distribution: 'temurin'
      java-version: 17
      overwrite-settings: false  # Add this line to prevent overwriting ~/.m2/settings.xml
```
### 3. Cache SonarQube Packages
This step caches SonarQube analysis components, like plugins or other downloaded files. These components are stored in the .sonar/cache directory on the runner.
```
- name: Cache SonarQube packages
  uses: actions/cache@v4
  with:
    path: ~/.sonar/cache
    key: ${{ runner.os }}-sonar
    restore-keys: ${{ runner.os }}-sonar
```
### 4. Cache Gradle Packages
This step caches Gradle’s dependency and build output files, which are stored in the .gradle/caches directory. The cache action will check if the cache exists and, if so, restore it to avoid re-downloading dependencies or rebuilding everything from scratch.
```
- name: Cache Gradle packages
  uses: actions/cache@v4
  with:
    path: ~/.gradle/caches
    key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle') }}
    restore-keys: ${{ runner.os }}-gradle
```
### 5. Build and Analyze with SonarQube
This step runs the Gradle build and triggers SonarQube analysis. The gradlew script is used to execute Gradle commands, ensuring that the correct Gradle version is used regardless of the runner's environment.
```
- name: Build and analyze
  env:
   SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
   SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  run: ./gradlew build sonar --info
```
Building the project is necessary to compile the code, run tests, and prepare the application. The SonarQube analysis step scans the code for quality issues (bugs, vulnerabilities, code smells), and the results are sent to the SonarQube server for review.

- SONAR_TOKEN: The token provides secure access to SonarQube.
- SONAR_HOST_URL: This is the URL of the SonarQube server where the analysis results will be sent.

## Example pipeline for Gradle
[gradle-sonarqube-pipeline-setup](./sonarqube.yaml)

