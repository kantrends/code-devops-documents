# Purpose
This document covers steps for generating SSH key pairs for deploying the applications to the Target VM from the Pipeline.

## Table of contents
  * [Purpose](#Purpose)
  * [Pre-requisite](#pre-requisite)
  * [Generate SSH Keys](#Generate-SSH-Keys)
    * [Test SSH Keys](#Test-SSH-Keys)
  * [Configure SSH Keys in Pipeline](#Configure-SSH-Keys-in-Pipeline)
    * [Bamboo](#Bamboo)
    * [ADO](#ADO) 

## Pre-requisite
- It is best practise to take a VM snapshot before making any changes on the VM.  If you are writing pipeline scripts to deploy to any VM or before doing any VM deployment,  please take a VM snapshot by creating a snow ticket [here](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=3ac535e84f278600f9c58b8d0210c754)
- Once VM snapshot taken, you will receive an email, after that do your changes/deployment.
- if there is any issue, then you can revert easily by requesting the Infra Team to restore the VM from the snapshot. 

## Generate SSH Keys
- First, we need server access. To get server access to raise the SNOW - [Add/Revoke Server Access](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=38f6b8d6db449090765f1d89139619d7)
Also mention, that we need Privileged Access (dzdo/sudo) = dzdo permissions needed for [server username]

- Once access is granted, log in to the server using your username from the command prompt and switch to the user using dzdo
  ```
  ssh username@server
  dzdo su - username
  ```

- Create a directory **.ssh** if it doesn't exist
  ```sh
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  cd ~/.ssh
  ```

- Command to Generate SSH key pair
  ```bash
  ssh-keygen -t rsa -m pem -f ~/.ssh/id_rsa_created
  ```
- Press Enter if it prompts for password.
- Once the key pairs, you can view the content of the key pairs using **cat** command
- To view the public key: `cat ~/.ssh/id_rsa_created.pub`
- To view the private key: `cat ~/.ssh/id_rsa_created`
- Copy RSA private keys and save them locally as a text file.
- Copy public keys from id_rsa_created.pub to authorized_keys
  ```bash
  cat ~/.ssh/id_rsa_created.pub >> ~/.ssh/authorized_keys
  ```
- Finally set the permission of authorized_keys
  ```bash
  chmod 600 ~/.ssh/authorized_keys
  ```

## Test SSH Keys
- In order to test the SSH key, open a terminal (command prompt or powershell) in your local workstation. 
- Change to the directory where the Private Key created in previous stage has been stored. 
- Connect server via SSH
  ```bash
  chmod 600 <private-key.txt> # to set the permission
  ssh -i <private-key.txt> <username>@<servername>
  ```
- If there is an issue, or it prompts for password, it means you haven't configured the key pair properly on the server


## Configure SSH Keys in Pipeline

## Bamboo
- In the bamboo SSH Task or in SCP Task, you can upload the private key file as shown in below image

  ![adding-ssh-pvt.png](./resources/adding-ssh-pvt.png)

## ADO
- Open Project settings in ADO and select service connections under _Pipeline_.
- Click "New Service Connection", search SSH and Next.
- Add required information in all fields and upload SSH private keys from local.
- Name the Service connection as [username]_[servername] format.

  ![ado-pvt.png](./resources/ado-pvt.png)


