# Purpose
This example covers pipeline steps to run katalon test case using pipeline. 

# Pre-requisite
- Configure test Suite to execute a test suite collection in sequential or parallel mode.
- Make sure to add unique "apiKey" for every projects.
- Create Generic service connection with SMTP details to send test reports email. Refer this [document](https://github.com/PremierInc/code-devops-documents/blob/feature/shema/azure_devops/pipeline/email_test_report.md) to create service connection.  

# Steps
1. `pipelines/smoke-test-az-pipeline.yaml` is the starting file.
2. `pipeline/test-template.yaml` will execute Katalon container to run test cases
    - Kill the existing Katalon container 
    - Run katalon container to run test cases
    - Copy katalon-test-case to Reports and remove katalon-test-case
    - Publish Test Results
    - Publish artifacts
    - Email Report - to send test case reports email using SMTP connection 