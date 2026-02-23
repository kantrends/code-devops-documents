# Purpose

This example covers pipeline configuration for build and deploying to nextjs-container-app-service

# Steps:

* We have created a Dockerfile using PNPM configuration 
* [azure-pipeline.yml](pipelines%2Fazure-pipeline.yml) is the root file
* Templatized build & deployment.
* [ci.yml](pipelines%2Fci.yml) has two jobs
    1. Build
       - Build image using defined SERVICE_NAME and VERSION_TAG
       - Save the docker image
       - Publish artifact
    2. Security Scan
       - Checkmarx
       - Lifecycle
* In [deploy.yml](pipelines%2Fdeploy.yml), we deploy the native apps using blue-green deployment. 
