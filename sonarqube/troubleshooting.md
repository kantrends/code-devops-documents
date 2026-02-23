# Troubleshooting / FAQ

## SonarQube Analysis Failure Due to OutOfMemoryError

**Issue Summary**:
When running the SonarQubeAnalyze task in an Azure DevOps pipeline, the analysis process failed with the following error:
```
ERROR: Error during SonarScanner execution
java.lang.OutOfMemoryError: Java heap space
```
The error indicated that the Java Virtual Machine (JVM) used by the SonarQube Scanner ran out of heap memory while processing the project.

**Root Cause**:
The JVM, used internally by the SonarQube Scanner, did not have sufficient heap memory to handle the analysis of the codebase. This is typically caused by:

- Large codebases with many files.
- High memory requirements for certain files.
By default, the heap size allocated to the SonarQube Scanner is limited, and for large projects, this can lead to OutOfMemoryError.

**Pipeline Task Involved**:
- Task: SonarQubeAnalyze@7

**Solution**:
1. Increase Heap Size for the SonarQube Scanner:
 - Add the following environment variable in the SonarQubeAnalyze@7 task to increase the maximum heap size:
   ```
   - task: SonarQubeAnalyze@7
     env:
       SONAR_SCANNER_OPTS: "-Xmx4096m"
   ```
   The SONAR_SCANNER_OPTS environment variable is used to pass JVM options to the SonarQube Scanner. Setting -Xmx4096m increases the maximum heap size to 4096 MB (4 GB).


# Excluding specific rules from specific files
## Analysis Scope => D. Issue Exclusions => Ignore Issues on Multiple Criteria

- You can prevent specific rules from being applied to specific files by combining one or more pairs of strings consisting of a `rule key pattern` and a `file path pattern`.

- The key for this parameter is `sonar.issue.ignore.multicriteria`, however, because it is a multi-value property, we recommend that only be set through the UI.
- To exclude any rule we need two patterns
  - Rule Key Pattern
  - File Path Pattern

## For example: 
- Rule Key Pattern --> `Web:S6853` (Indicates it's related to a java based web application)

- File Path Pattern --> `**/*.html` (Indicates pattern targetting html files in a web application)

  - Login to [SonarQube](https://sonarqube.premierinc.com/) -->  Select your `project/Application` --> Select `Project Settings "General"` --> Search for `Ignore Issues on Multiple Criteria` and add both `Rule Key Pattern` & `File Path Pattern` to exclude the rule targetting html files of a web application as shown in below snapshot.
![image](https://github.com/user-attachments/assets/77e2b523-dbf3-4cd7-83d0-e3ee78f43e99)
