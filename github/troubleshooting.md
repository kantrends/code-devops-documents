# Troubleshooting
This document covers common issues that can be resolved by application teams on their own.

## SSL Clone issue in Intellij 
- **Problem**: I am having an SSL certificate issue (unable to get a Local issuer certificate). I am unable to clone the code from Git to IntelliJ.
- **Solution**:
  1. Open Intellij, Go to File -> Settings -> Advanced Settings
  2. Check  the "Use Windows Certificate Store" option

## SSL Clone Issue in Visual Studio
**Solution**: Within Visual Studio, click the Git→Settings menu item, then change the Credential Helper Select Element to Secure Channel

## How do I get answers for GitHub Copilot?
- Check our Copilot [troubleshooting document](./copilot/troubleshooting.md)

## User has not received the GitHub invitation
- **Problem**: After adding user to AD group, I waited for an hour. Still invitation hasn't received. In that case,follow the solution here. 
- **Solution**: Use [Self Service](https://github.com/PremierInc/code-self-service#code-self-service) option to send the GitHub invite manually again.

## User unable to access Premier repositories after GitHub invite
- Login to https://github.com/premierinc using the premier email address
- Now try to accept the invitation
- Now they can access the premier repository.

## User unable to see repositories of one project
- **Problem**: The user may not be part of the project AD group. For example, if the user is unable to view repositories of the WFM project, then the user may not be part of the "devops_wfm" AD group.
- **Solution**: So the solution is to add the user to the project AD group in Azure Active Directory. (Ref: [GH user provisioning](./user-provisioning.md)) Only owners of the AD group can add the users to the AD group in Azure Active Directory. 

## Create New Repository
- **Problem**: Only GitHub Admins have the option to create repositories in GitHub
- **Solution**: Use [Self Service](https://github.com/PremierInc/code-self-service#code-self-service) to create new repositories and add them to your Team Project in GitHub.

## Archive GitHub Repository
- **Problem**: Only GitHub Admins have the option to archive repositories in GitHub
- **Solution**: Use [Self Service](https://github.com/PremierInc/code-self-service#code-self-service) to archive repositories in GitHub.

## External Users in GitHub
Add external users at the repo level and not at the ORG level. Only Enterprise Admins can do that. 

## Lost access to your 2FA device
- **Problem**: If you able to login but, lost your two factor authentication codes you can download by following below steps,
- **Solution**: Access your GitHub profile -> Click on `Settings` -> Select `Password and authentication` -> Find `Recovery codes` -> click `View` and Download the list of recovery codes. 
- **Important points to remember**:
  1. Keep your recovery codes in a safe place, separate from your regular login information.
  2. If you lose access to your 2FA device, you can use these recovery codes to regain access to your account.
  3. Do not share your recovery codes with anyone.
    
## How to recover a GitHub Account

## CASE:1
- **Problem**: We can recover a GitHub account using recovery codes. But, How ?
- **Solution**: The quickest way to recover access would be by using one of the account recovery codes that we strongly encouraged be kept safe when 2FA was enabled. Even if you think you might not have them, you may have saved your recovery codes to a password manager or somewhere on one of your devices. The default filename for these codes is `github-recovery-codes` or `github-recovery-codes.txt`. For more information about using a recovery code, read [Using a two-factor authentication recovery code](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials#using-a-two-factor-authentication-recovery-code).

## CASE:2
- **Problem**: If you don't have the authenticator application or a valid recovery code
- **Solution**: In this situation, you can unlink your email address from the locked account. This will let you use your email address with a new GitHub account. To begin unlinking your email address, follow the steps in [Unlinking your email address from a locked account](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-personal-account/unlinking-your-email-address-from-a-locked-account).

## How to contact GitHub support
- You can reach our team or open a support ticket.
- To reach us either you can reach any individual in Application Delivery Team or send a email at [ApplicationDelivery](ApplicationDelivery@premierinc.onmicrosoft.com) team DL.
- To open a support ticket without any GitHub signin please refer [GitHub Support No Sign Needed](https://support.github.com/contact/cannot_sign_in) website link.
