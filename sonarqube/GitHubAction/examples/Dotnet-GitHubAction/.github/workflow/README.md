# SonarQube .NET Setup
This document outlines the essential steps to integrate SonarQube with a Dotnet project using GitHub Action for continuous code quality inspection.

## Official Documentation
For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 

## Prerequisites
Before you start configuring the pipeline for SonarQube integration, ensure you meet the following prerequisites:

GitHub Repository Setup:

- Your repository must have a .github/workflows/ directory.
- The pipeline YAML file should be placed in .github/workflows/sonarqube.yaml.

## GitHub Action Tasks for Dotnet

### 1. Checkout the Code
This step checks out the project's code from the repository to the runner .
- fetch-depth: 0: This setting ensures that the entire Git history is cloned, not just the latest commit. SonarQube may use the full Git history for accurate analysis, particularly for blame-based analysis.
```
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Disable shallow clone for better analysis accuracy
```
### 2. Set up JDK 
This step sets up JDK  as the default Java version for the workflow.
```
- name: Set up JDK 17
  uses: actions/setup-java@v3
  with:
      distribution: 'temurin'
      java-version: 17
      overwrite-settings: false  # Add this line to prevent overwriting ~/.m2/settings.xml
```
### 3. Cache SonarQube Packages
This step caches SonarQube analysis components, like plugins or other downloaded files. These components are stored in the .sonar/cache directory on the runner.
```
- name: Cache SonarQube packages
  uses: actions/cache@v3
  with:
    path: ~/.sonar/cache
    key: ${{ runner.os }}-sonar
    restore-keys: ${{ runner.os }}-sonar
```
### 4. Cache SonarQube Scanner
This step caches  dependency and build output files, which are stored in the .net/caches directory. The cache action will check if the cache exists and, if so, restore it to avoid re-downloading dependencies or rebuilding everything from scratch.
```
- name: Cache SonarQube scanner
  id: cache-sonar-scanner
  uses: actions/cache@v3
  with:
    path: .\.sonar\scanner
    key: ${{ runner.os }}-sonar-scanner
    restore-keys: ${{ runner.os }}-sonar-scanner
```
### 5. Install SonarQube Scanner (if not cached)
This step installs the SonarQube scanner if it wasn’t restored from the cache.

- if: steps.cache-sonar-scanner.outputs.cache-hit != 'true': This condition checks if the cache was restored. If not, the scanner is installed.
- dotnet tool install dotnet-sonarscanner --tool-path .\.sonar\scanner: Installs the dotnet-sonarscanner tool locally in the .sonar/scanner directory.
- echo "$PWD\.sonar\scanner" >> $GITHUB_PATH: Adds the scanner’s directory to the system PATH.
```
- name: Install SonarQube scanner
  if: steps.cache-sonar-scanner.outputs.cache-hit != 'true'
  shell: powershell
  run: |
   New-Item -Path .\.sonar\scanner -ItemType Directory
   dotnet tool update dotnet-sonarscanner --tool-path .\.sonar\scanner
```
### 6: Build and Analyze with SonarQube
This step builds the .NET project and then runs the SonarQube analysis on the code. It uploads the analysis results to the SonarQube server for further review and reporting.

- .sonar\scanner\dotnet-sonarscanner begin: Starts the SonarQube analysis process.
  -  /k:"example": The SonarQube project key.
  - /d:sonar.token="${{ secrets.SONAR_TOKEN }}": Authentication token for SonarQube, securely stored in GitHub secrets.
  - /d:sonar.host.url="${{ secrets.SONAR_HOST_URL }}": URL of the SonarQube server, also securely stored in GitHub secrets.
- dotnet build: Builds the .NET project.
- .sonar\scanner\dotnet-sonarscanner end: Finalizes the analysis and sends the results to the SonarQube server.
```
- name: Build and analyze
  shell: powershell
  run: |
    .\.sonar\scanner\dotnet-sonarscanner begin /k:"example" /d:sonar.token="${{ secrets.SONAR_TOKEN }}" /d:sonar.host.url="${{ secrets.SONAR_HOST_URL }}"
    dotnet build
    .\.sonar\scanner\dotnet-sonarscanner end /d:sonar.token="${{ secrets.SONAR_TOKEN }}"
```

## Example pipeline for Dotnet
- [dotnet-sonarqube-linux-pipeline-setup](./sonarqube-linux.yaml)
- [dotnet-sonarqube-windows-pipeline-setup](./sonarqube-windows.yaml)
