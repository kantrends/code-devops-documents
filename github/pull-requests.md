# Purpose
This document covers everything related to Pull Requests in GitHub.


# Create Pull Request
- To create Pull Request, Go to GitHub Repository. 
- Select **Pull Request** Tab. 
- Select **New Pull Request**
- Base: Target Branch, Compare: Source Branch.  For example, select "develop" as base branch, and "feature/abc" as compare branch, if you want to merge the changes from "Feature/abc" branch to "develop" branch.
- Select **Create Pull Request**
- Give Title to your Pull Request. If you would like to integrate your ADO Work Items to the pull request, then title must have `AB#<ado_work_item>`.
  - For example: Title:  UI Changes AB#12345
- Add Description. Best Practice is to include the following details in the description
  - Reason for creating the pull request
  - List of changes done.
  - ADO Work Item URL
  - Tests performed.
- In the right pane, under **Reviewers**, add the team members who you would like to review the Pull Request.
- In the right pane, under **Assignees**, click `assign yourself` to add your name as the person who created the Pull Request.
- In the bottom, you can find the list of files changed.  Verify that.
- Select **Create Pull Request**.


# Configure Default Reviewers for Pull Requests
- This is accomplished using the **CODEOWNERS** feature in GitHub.
- Under the root of the repository, create a file called _CODEOWNERS_.
- In the _CODEOWNERS_ file, provide the user id's who we want to make as default approvers for all the Pull Requests.
- Example 1: To add default reviewers
  ```
  *      @userid1 @userid2 @userid3
  ```
  <img width="683" alt="image" src="https://user-images.githubusercontent.com/109576418/218087953-d48b0f9a-93a5-4d4c-9536-e46571bf6b28.png">
  
- Example 2: To add entire GitHub team as default reviewers
  ```
  *   @premierinc/code
  ```

# Configure Minimum Approvers Count in PR
This change must be done at the Repository Settings and developers have no access to it except GitHub Admins. But there is a way for the GitHub users to manage the Repository Settings using Policy as a Code which we call it as **Safe Settings**.  

Follow the below steps:
- Search for repository called `admin`. 
- Under that repository, go to `.github/repos` directory.
- To manage repository settings, you must create a file ([repo_name].yml) in the same name as your repository name and write the settings in the form of policy as code. 
- In this yml we can apply this PR approvers count for the branches.
- For example, to set the default approvers count to 3, make "required_approving_review_count" as 3
- Also we need to change "dismissal_restrictions" section also for applying members who can dismiss a Pull Request.

  <img width="627" alt="image" src="https://user-images.githubusercontent.com/109576418/218086264-07f7a496-094c-4cb6-beb7-b7b95e36ae98.png">

# Reference
- GitHub docs on [Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- GitHub docs on [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Read about [Safe Settings in Premier](https://github.com/PremierInc/code-safe-settings/wiki)

