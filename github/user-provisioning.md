# Purpose
This document explains the procedure to onboard user to GitHub and to a GitHub Team.

# Description
- Repositories are linked to GitHub Team.
- GitHub Team = Project in ADO
- Each GitHub Team is linked to Azure Active Directory Group (AD Group). So if you want to add or remove members from GitHub Team, you have to do it in Azure Active Directory Group (AD Group).
- Procedure to add/remove members to the AD Group is covered [here](../azure_devops/user_provisioning.md)

> **Note**: It usually takes an hour to sync the AD Group with GitHub. 

## New user to GitHub
- If the user is new to GitHub, adding users to the AD Group will trigger an email that sends a GitHub invitation to the user. Wait for 1 hour for the sync to happen.
- The user must create a new GitHub account using the Premier Email address and must accept the invitation within 7 days and 
- If the user fails to accept the invitation within 7 days, then you have to send the invitation again. To do that, use the [self service](https://github.com/PremierInc/code-self-service#code-self-service) option we created.
- Once the user accepted the invitation, he/she will see few repositories. Wait for 1 hour for the sync to finish and then he/she will be able to see all GitHub Team repositories.

## Existing User in GitHub
- If you are trying to add an existing user to a new project (GitHub Team), after adding the users to the AD Group, the user is automatically added to the GitHub Team and has access to all repositories in the GitHub Team. 

