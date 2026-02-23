# Troubleshooting

### How to get GitHub CoPilot License?
**Solution 1**: Kindly submit a snow ticket [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=276df6d1930a9a94487cba1e1dba10e0)

**Solution 2**: Follow the steps given in the [self-service](https://github.com/PremierInc/code-self-service?tab=readme-ov-file#github-copilot-license-request) document. 

> Note: License will be revoked if unused for 30 days

---
### Why did I lose my GitHub CoPilot License?
We have an automation job that runs on the second-to-last day of each month. This job removes the license for users who have not used Copilot in the past 30 days

---
### Unable to view Copilot Models in IDE?
- Make sure you have GitHub Copilot Business License. Go to [https://github.com/settings/copilot/features](https://github.com/settings/copilot/features) to check if you have Copilot Business License. 
- Sign out from GitHub in IDE
- Close the IDE
- Open IDE and Sign in to GitHub.
- If you're still having issues, raise a support ticket [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=276df6d1930a9a94487cba1e1dba10e0)

---
### Copilot Login Issue or GitHub MCP Start Issue
- **Possible Problem 1:** You don't have GitHub Copilot license
  
  **Solution:** Check if you have GitHub Copilot license and if you don't, follow the steps to get copilot license given above

- **Possible Problem 2:** Netskope is installed on your laptop/VDI. Netskope is a middleware that provides a custom CA certificate to the outside world from your laptop. 
  
  **Solution**: 
  - Download `nscert_bundle1.pem` file from __http://servers.premierinc.com/certs/__ and save it in your User Home Directory.
  - Set the NODE_EXTRA_CA_CERTS environment variable and nscert_bundle1.pem file location path as env value 
    - For windows, set it in system environment variable. 
      ```
      NODE_EXTRA_CA_CERTS=E:/aselvara/nscert_bundle1.pem
      ```
    - For Mac, add it to your `~/.zshrc` file
      ```
      export NODE_EXTRA_CA_CERTS=$HOME/nscert_bundle1.pem
      ```
  - Restart your IDE. 

