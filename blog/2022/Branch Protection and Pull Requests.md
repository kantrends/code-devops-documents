# Branch Protections and Pull Requests

Starting in **January 2022**, all development projects must use pull requests as a branch protection for main/master branches for all project repos. This protection requires:

1. At least 1 reviewer before the main/master branch merge.
2. The requestor cannot be the reviewer.
_Note: The best practice is at least 2 reviewers and a dedicated lead(s) to review merges to main/master branch._

**Why main/master?**
This satisfies the Separation of Duties compliance requirement on the production code base. Most application teams deploy to production from a main/master/release/hotfix branch, but in all cases the main/master branch represents the running production code, whether pre- or post
deployment.
![image](https://user-images.githubusercontent.com/51210529/148256879-3e4de081-9a03-405b-9aec-5af72e591d91.png)

**What do you have to do?**
Starting on Feb 1st 2022, this branch protection will be applied automatically to all repos in

* CODE/BitBucket  <https://code.premierinc.com/source>
* GitHub  <https://github.com/premierinc>

To avoid impact, Dev teams need a branching strategy that requires a pull request approval to merge to main/master. Please review the following branching guides and pull request documents below.

**Who to contact?**
"CODE DevOps Office Hours" will be hosted to answer questions, or you may ask question in the Teams channel below.

 [CODE Teams Channel CODE Team - Branch Protections](https://teams.microsoft.com/l/channel/19%3a361ea6284dcd493187133acb26d33cf1%40thread.skype/Branch%2520Protections?groupId=8f684385-ec4d-4cee-8112-05826709b0ee&tenantId=b110eddf-23ae-457c-a6f3-734d592b2847)

**Branching and Pull Request Guides:**

* [Pull Requests in Bitbucket](https://confluence.atlassian.com/bitbucketserver/pull-requests-776639997.html)
* [Pull Requests in GitHub](https://docs.github.com/en/get-started/quickstart/github-flow)
* [Premier Branching Models](https://github.com/PremierInc/code-devops-documents/wiki/CODE-Team-Recommended-Branching-Models)
* [Azure DevOps Branching Strategy](https://github.com/MicrosoftDocs/azure-devops-docs/blob/master/docs/repos/git/git-branching-guidance.md)
