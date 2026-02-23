# GitHub Best Practices

## Open VS Code in Browser
Just press . (dot) on your keyboard when browsing any GitHub repository and it will open it in VS Code IDE on the browser.  This helps in editing multiple files and make a single commit without the need to clone the repository. 

## Commit Message
Giving a proper commit message helps you to debug the issue & find the changes made easily.  Trust me, it helps and looks Professional.

## Pull Request
- Always do merge the changes from the target branch to your branch before creating Pull Request. 
  
  - For example, if you are going to create a Pull Request from feature branch to develop branch, make sure you pull the latest code of develop branch to your local and merge it with your feature branch, resolve merge conflict if present, test your feature branch and then create Pull Request. 

- Give proper Title to your Pull Request. Add **AB#[ADO Work Item Number]** so that the PR gets integrated with your ADO Work Items.


## Squash vs Merge Pull Request
- When you merge **feature** branch to **develop** branch, use **Squash Commit** so all your unwanted commits are squashed into single commit with proper commit message. For example, _AB#1234: Changed Login Form Submit Button color since my Boss hates blue_.

- When you merge **develop** branch to **main** branch, use normal **Merge Commit** which adds all the commits to main branch. 

By this way, your **main** & **develop** branches looks clean and you can revert a particular commit if needed.

## Handling Branches

| Name | Purpose | TTL | Naming standard |
| --- | --- | --- | --- |
| main | default Branch. Production branch. | forever | main |
| develop | integration branch | forever | develop |
| release | ready for releases | short-lived or long lived based on use cases | release/v1.0.x |
| feature | new features | short lived and delete after PR | feature/ui-button or feature/[ticketNo] |
| bugfix | fixing bugs | short lived | bugfix/ui-button or bugfix/[ticketNo]
| hotfix | fixing issues in production releases | short lived | hotfix/v1.0.x |

- Please do delete the feature branches after a PR or after a Prod release so your repository looks clean
- Giving proper names to the branches helps the team to understand the purpose of the branch.

## GitHub Branch Protection
- Use [safe-settings](https://github.com/PremierInc/code-safe-settings/wiki/Concepts) to handle repository permissions and settings.
- Always protect the branch that goes into Production or else you will be caught during Audit. By default, main branch is protected and if needed, apply branch protection in other branches using safe-settings.


## What should not go into GitHub?

- Passwords, Tokens, and Secrets must not be committed. In case if committed, make sure you delete the Branch and create a new branch or try to delete the commit history from GitHub.
- Do not commit `node_modules`, `build` directory in case of Gradle, `target` directory in case of Maven.  Instead add them to the `.gitignore` so that it gets excluded when you commit to GitHub.
- Do not commit **large files** to GitHub. Use Git LFS if needed and only if the large files cannot be stored in Nexus or anywhere else. 

## Team Monitoring
- Regularly, check the users in GitHub Teams and remove users who does not belong to your project to protect your repositories. 

