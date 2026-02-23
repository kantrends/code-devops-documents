# Add Security Scan for GitHub Actions

To create GitHub Actions for Nexus IQ we need to have access to actions in GitHub. Open the actions tabs in your repository and choose "New workflow."

---
**Note:** GitHub Actions for Sonatype Nexus is NOT OFFICIALLY SUPPORTED by Sonatype; hence, you will not find it in the marketplace; instead, select "Simple Workflow" and customize it as needed.

---

Now to add Nexus-IQ Scan for your repo you need to adjust your main.yml which is located in `.github/workflows/`

  ```yaml
name: Nexus scan

on:      
  workflow_dispatch:
  push:

jobs:
  Nexus-Lifecycle-Scan:
    runs-on: [self-hosted, Linux, premierinc] #change the runner accordingly. Either Windows or Linux.

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Use Nexus Scan Template
        uses: PremierInc/shield-gh-templates/nexusiq-scan@main
        with:
          username: ${{ secrets.SYSTEM_NEXUSIQ_USERNAME }} # Mandatory: already pre-configured at ORG level
          password: ${{ secrets.SYSTEM_NEXUSIQ_PASSWORD }} # Mandatory: already pre-configured at ORG level
          target: '.' # optional
          repositoryNameSuffix: '' #optional
  ```
---

**Note:** Stage will be selected automatically. If you are using `main`, `hotfix` or `release` branch then stage will be `stage-release` and for any other branch stage will be `build`.

**Note:** Target will also be "." as it will scan the entire repository. If you want to override it you can change the target you want to use. But if the target won't exist there it will throw an error so select a directory which exists.

**Note:** Application-ID will be picked from the repository name so the application-id and the repository name must be the same to perform nexus scan.
