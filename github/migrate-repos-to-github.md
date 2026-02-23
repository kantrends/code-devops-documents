# Purpose
This document covers steps on how to migrate repositories to GitHub from any SCM (Bitbucket/GitLab).


# Scenarios
- Scenario 1: A simple repository with no large files. 
- Scenario 2: The repository have large files but those files are not needed in GitHub anymore. 
- Scenario 3: The repository have large files (>100 MB) and you need them in GitHub but without history

> Note:  After migrating to GitHub, make sure you change the linked repository in Bamboo to point GitHub if you are going to use Bamboo. Refer the [reference](#reference) section. 

# Pre-requisite
No matter what the Scenario is, you need an empty repository in GitHub. Use the [self-service](https://github.com/PremierInc/code-self-service#github-repository) to create the empty repository in GitHub

## Scenario 1: Migrate Repository to GitHub with Histories
### Pre-Requisite
- Make sure you create a empty github repository and that is tied to a GitHub Team you have access to. Use Self Service.
- Make sure you have the access to both old SCM and new GitHub repository.

### Steps

- Git mirror clone the repository 
    ```bash
    git clone --mirror https://code.premierinc.com/source/scm/dmm/scs_db.git
    ```
- Remove remote origin pointing to old SCM
    ```bash 
    cd scs_db.git 
    git remote remove origin 
    ```

- Rename the master branch to main branch and point origin to GitHub
    ```bash
    git branch  # shows current branch name 
    git branch -m main # this will rename current branch (master) to main branch 
    git remote add origin https://github.com/PremierInc/example-temp.git # provide the github origin URL
    ```

- Verify Origin change to the Github Repository and push to GitHub
    ```bash
    git remote -v
    git push --mirror 
    ```

## Scenario 2: Migrate Repository (LFS) with Histories 
You have large files in your repository but you no longer need them in GitHub or in Histories. Then follow the below steps:
### Pre-Requisite
- Make sure you create a empty github repository and that is tied to a GitHub Team you have access to. Use Self Service.
- Make sure you have the access to both old SCM and new GitHub repository.
- Make sure you installed "Git-LFS" from internet. 
- Make sure you downloaded [BFG Cleaner](https://rtyley.github.io/bfg-repo-cleaner/#usage) Executable from internet. 

### Steps

- Clone the repository using mirror clone
    ```bash
    git clone --mirror https://code.premierinc.com/source/scm/dmm/some-big-repo.git
    ```
- Use bfg.jar to remove files greater than 100 MB.
    ```bash
    java -jar bfg.jar --strip-blobs-bigger-than 100M some-big-repo.git
    ```
- Do Garbage Pruning and push to GitHub
    ```bash
    cd some-big-repo.git
    git remote remove origin
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
    git branch -m main # this will rename current branch (master) to main branch 
    git remote add origin https://github.com/PremierInc/example-temp.git # provide GitHub Origin URL
    git push --mirror
    ```

## Scenario 3: Migrate Repository (LFS) without Histories 
You have large files in your repository and you need them in GitHub but without Histories. Then follow the below steps:

### Pre-requisite
- Make sure you installed "Git-LFS" from internet. 

- Clone a repository
    ```bash
    git clone remote url
    ```
- cd to repo root level

- Create a new empty branch with expected name by using below command. It will create a new empty branch
    ```bash
    git checkout --orphan branchname
    ```
- Initialize Git LFS by running below command:
    ```bash
    git lfs install
    ```
- In each Git repository where you want to use Git LFS, select the file types you'd like Git LFS to manage (or directly edit your .gitattributes). You can configure additional file extensions at anytime.
    
    ```bash
    git lfs track "*.fileextension"
    git lfs track "*.avi"
    ```

- Now make sure .gitattributes is tracked
    ```bash
    git add .gitattributes
    ```

- Let's check whether LFS tracking under attributes files or not by running below command
    ```bash
    git lfs track
    ```

- Now let's commit LFS files first with attributes to track LFS Files and then commit remaining files and push using below command:
    ```bash
    git commit -m 'added attributes file'
    git add --all
    git commit -m 'added all files'
    git push origin --all
    ```


# Reference
- [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [Link GitHub in Bamboo](https://github.com/PremierInc/code-devops-documents/wiki/Integrate-GitHub-with-Bamboo)
- Configure [Github in Bamboo](https://confluence.atlassian.com/bamboo/github-289277001.html)

