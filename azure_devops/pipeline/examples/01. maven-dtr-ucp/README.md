# Maven DTR Build & UCP Deploy

Example pipeline configuration to build and push Docker Images to DTR using Maven and deploy to UCP.

# YAML Files

### Root file
- pipelines/azure-pipelines.yml

### Templates
- pipelines/ci_build.yml (Stage template for CI Build & Scan)
- pipelines/deploy.yml (Stage template for UCP deployment)

# Pre-requisite
Complete the below steps before writing YAML pipelines for maven ucp deployment type projects.

- Added the below configurations to the pom.xml file which is needed to extract maven properties at the build time. 

    ```xml
        <build>
            <plugins>
                <!-- This Plugin is used to retrieve the Maven Project ID, Artifact ID, Version -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-help-plugin</artifactId>
                    <version>3.2.0</version>
                </plugin>
            </plugins>
        </build>
    ```

- create two variable groups in Azure DevOps for holding DOCKER credentials as per [this document](https://github.com/PremierInc/code-devops-documents/blob/main/azure_devops/pipeline/library.md#variable-groups).

- create variable groups that holds environment variables for particular environments (dev, qa, uat, prod) as per [this document](https://github.com/PremierInc/code-devops-documents/blob/main/azure_devops/pipeline/library.md#use-case-2-deployments).

- create environments in Azure DevOps for each environment (dev, qa, uat, prod). Read  [this document](https://github.com/PremierInc/code-devops-documents/blob/main/azure_devops/pipeline/environments.md) for more information about environments. 

- create `docker-compose.yml` file and add variables whereever required. For example, 
  ```yaml
  version: '3.8'
  services:
    abc-project:  
      image: dtr.premierinc.com/code_org/image:${APP_VERSION}
      environment:
      - DB_USER=${DB_USERNAME}
  ```
