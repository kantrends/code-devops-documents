# Ansible Deployment
Ansible is a configuration Management tool which helps to configure the VM for application deployment.  
- This involves installing packages needed for the app to run. In this case "DOCKER".
- Create required directories & files.
- Deploy application as Docker Containers.
  - Nginx Deployment for TLS termination (Optional). If you are not using, remove / comment out those Ansible steps
  - Application deployment as Docker Containers
  - Filebeat to send Docker container logs to ECE (Optional). If you are not using, remove / comment out those Ansible steps

### Files & Directories
- **hosts**: contains server information. If you want to add/remove server, do it here. 
- **vm-deploy.yaml**: first file that gets executed.
- **install-docker.yaml**: Install docker & run it as a service
- **deploy-app.yaml**: Deploy applications as docker container
- **group_vars**:
  - **all.yaml**: common variables for all environments
- **files**: template files that is needed on the server
  - **docker-daemon.json**: specify the docker storage location
  - **nginx.conf**: nginx specific configuration
  - **filebeat.yml**: configuration to send docker container logs to ECE stack


### How to configure new server?
- When you provision a new server/existing server, ask the infra team to do the below items:
  - Add `ansible` user account to this server.  Need to add dzdo centrify command for ansible user account. The following commands that require dzdo access from `ansible` user account are:  
    ```
    /bin/sh * /usr/libexec/platform-python *
    /bin/sh * /usr/bin/python *
    /bin/sh * /usr/bin/python3 *
    ```

- Other than this, no need to install any package on the VM. 
- Once `ansible` account is added, login as `ansible` user and configure the SSH keys. 
- Once you have created the SSH keys, add the private_key to the `ADO Library -> Secure Files` so that the pipeline passes this info to Ansible to deploy the application to your server. 
- If you are going to deploy to multiple servers in same environment, then configure same public/private key pair in all the servers. For example: same key pair configuration on c3sumcecc01, c3sumcecc02, c3sumcecc03. 


