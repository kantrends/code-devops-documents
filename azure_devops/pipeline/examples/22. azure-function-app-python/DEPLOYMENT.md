# Azure Function App Deployment Guide

## Overview
This Azure Function App processes Azure DevOps webhook events and synchronizes work items with GitHub issues.

## Setup and Deployment

### 1. Prerequisites
- Azure CLI installed
- Azure Functions Core Tools v4
- Python 3.13+ 
- GitHub Personal Access Token

### 2. Local Development Setup

1. Install Azure Functions Core Tools:
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

2. Create Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure local settings:
   Update `local.settings.json` with your GitHub token:
   ```json
   {
     "Values": {
       "GITHUB_TOKEN": "your-personal-access-token",
       "GITHUB_ORG": "YourOrgName",
       "DEFAULT_GITHUB_REPO": "your-default-repo"
     }
   }
   ```

### 3. Local Testing

Run the function locally:
```bash
func start
```

Test endpoint will be available at: `http://localhost:7071/api/AdoGitHubSync`

### 4. Deploy to Azure

1. Create a Function App in Azure:
   ```bash
   az functionapp create --resource-group myResourceGroup \
     --consumption-plan-location westus2 \
     --runtime python --runtime-version 3.9 \
     --functions-version 4 \
     --name myFunctionApp --storage-account mystorageaccount
   ```

2. Deploy the function:
   ```bash
   func azure functionapp publish myFunctionApp
   ```

3. Configure application settings:
   ```bash
   az functionapp config appsettings set --name myFunctionApp \
     --resource-group myResourceGroup \
     --settings GITHUB_TOKEN="your-token" \
                GITHUB_ORG="YourOrg" \
                DEFAULT_GITHUB_REPO="your-repo"
   ```

### 5. Azure DevOps Webhook Configuration

1. Go to your Azure DevOps project settings
2. Navigate to Service Hooks
3. Create a new subscription for "Work item" events
4. Set the URL to: `https://myFunctionApp.azurewebsites.net/api/AdoGitHubSync?code=your-function-key`
5. Configure events for "Work item created" and "Work item updated"

## Function Behavior

### Supported Events
- `workitem.created`: Creates a new GitHub issue
- `workitem.updated`: Updates existing GitHub issue or creates new one if not linked

### Environment Variables
- `GITHUB_TOKEN`: GitHub Personal Access Token (required)
- `GITHUB_ORG`: GitHub organization name (default: PremierInc)
- `DEFAULT_GITHUB_REPO`: Default repository name (default: code-aakash-test)

### Response Format
```json
{
  "status": "success|error",
  "message": "Description of what happened",
  "workItemId": "ADO work item ID",
  "githubIssueNumber": 123
}
```

## Troubleshooting

1. Check Application Insights logs for detailed error information
2. Verify GitHub token has proper permissions
3. Ensure webhook URL is accessible from Azure DevOps
4. Check function app logs using Azure CLI:
   ```bash
   az functionapp logs tail --name myFunctionApp --resource-group myResourceGroup
   ```