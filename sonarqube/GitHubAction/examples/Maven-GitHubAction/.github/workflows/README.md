# SonarQube Setup for Maven with GitHub Actions

This document outlines the essential steps to integrate SonarQube with a Maven project using GitHub Action for continuous code quality inspection.

## Official Documentation

For more detailed information on integrating SonarQube with Azure DevOps, refer to the [official documentation](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/azure-devops-integration/) 

## Prerequisites
Before you start configuring the pipeline for SonarQube integration, ensure you meet the following prerequisites:

GitHub Repository Setup:

- Your repository must have a .github/workflows/ directory.
- The pipeline YAML file should be placed in .github/workflows/sonarqube.yaml.

Maven Wrapper Setup:

- Your project must include a Maven wrapper 
- To generate a Maven wrapper, follow the instructions provided in the official documentation: 
  [Maven Wrapper Documentation](https://maven.apache.org/wrapper/).

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
## SonarQube Analysis in GitHub Actions

### 1. Set JAVA_HOME

This task sets up the JDK for the Maven build. JAVA_HOME is an environment variable used to define the location of the Java installation. Without this variable, the Maven build would not be able to locate the JDK, and the build process would fail.
```
- name: Set up JDK 17
  uses: actions/setup-java@v4
  with:
      distribution: 'temurin'
      java-version: 17
      overwrite-settings: false  # Add this line to prevent overwriting ~/.m2/settings.xml
```

### 2. Cache SonarQube Packages
  This task caches the SonarQube analysis components. During the SonarQube analysis, various dependencies and packages are downloaded (e.g., plugins or libraries required by SonarQube to analyze the code). Caching these files helps avoid downloading them repeatedly in each build.
```
- name: Cache SonarQube packages
  uses: actions/cache@v4
  with:
    path: ~/.sonar/cache
    key: ${{ runner.os }}-sonar
    restore-keys: ${{ runner.os }}-sonar
```
### 3. Cache Maven Packages
This task caches the Maven dependencies. Maven uses a .m2 directory to store downloaded libraries and dependencies for the project. Over time, these dependencies don't change much, so caching them helps avoid downloading the same libraries every time the build runs.
```
- name: Cache Maven packages
  uses: actions/cache@v4
  with:
    path: ~/.m2
    key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
    restore-keys: ${{ runner.os }}-m2
```
### 4. Build and Analyze with SonarQube
This task performs the Maven build and SonarQube analysis. It runs a Maven command that:
- Builds the project: Using the mvn verify command, which compiles the code, runs tests (if configured), and verifies the build.
- Triggers SonarQube analysis: By adding org.sonarsource.scanner.maven:sonar-maven-plugin:sonar, this command initiates SonarQube’s static code analysis.

```
- name: Build and analyze
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  run: mvn -B verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
```
## Example pipeline for maven
[maven-sonarqube-pipeline-setup](./sonarqube.yaml)

