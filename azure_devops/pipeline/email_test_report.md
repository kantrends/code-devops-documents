# Purpose
This document covers steps to email the test results & reports after pipeline execution.

# Pre-requisite
A Generic Service Connection must be created that must contain the SMTP details. 
- Check if any service connection in the name `Premier_Email_*` is present in your project. To do so, **Project -> Settings -> Service Connections**. If it is not present, please raise a SNOW Ticket on our team to create the service connection.
  > Note: ADO Admins must follow [this document](https://dev.azure.com/premierinc/CODE/_wiki/wikis/AzureDevOps.wiki/2283/Email-Test-Results-Report-via-Pipeline) to create service connection. Only ADO Admins have access to this document. 
- Once the Admins completed this request, you will see the Service Connection in your project. 

# Add Email Task To Pipeline
Create a new job like `Email Automation` and add below configuration to pipeline.

> **Note: EmailReport@1 task works only from windows agents. Hence specify the pool name.**

```YAML
  - job: EmailAutomation
    pool:
      name: 'Premier Windows Agents'
    displayName: Email Automation
    dependsOn: ['job1'] # provide the job name which produces the test results
    steps:
      - task: EmailReportV2@2
        inputs:
          sendMailConditionConfig: 'Always'
          subject: '[{environmentStatus}] {passPercentage} tests passed in for $(Build.BuildNumber)'
          includeInToSectionStr: ''
          toAddress: 'email1@premierinc.com;email2@premierinc.com'
          defaultDomain: 'premierinc.com'
          groupTestResultsBy: 'run'
          includeCommits: true
          maxTestFailuresToShow: '15'
          includeOthersInTotal: false
          usePreviousEnvironment: false
          enableTLS: true
          smtpConnectionEndpoint: 'PremierInc_Email_SC-PincAI' # service connection name created in Pre-requisite
```

# Reference
- [Email Report Extension](https://marketplace.visualstudio.com/items?itemName=epsteam.EmailReportExtension) official document.
