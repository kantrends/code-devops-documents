# Ansible Deployment
Ansible is a configuration Management tool which helps to configure the VM for application deployment.  
- This involves installing packages needed for the app to run. 
- Create required directories & files.
- Configure SystemD services for the apps to run as a service

### Files & Directories
- **hosts**: contains server information. If you want to add/remove server, do it here. 
- **vm-deploy.yaml**: first file that gets executed.
- **install-app.yaml**: Install app & run it as a service
- **install-java.yaml**: Install JAVA on the server
- **group_vars**:
  - **all.yaml**: common variables for all environments
- **templates**: template files that is needed on the server
  - **ae-provision.service**: systemd file to run app as a service
  - **startup.sh**: startup file to run your application


### How to upgrade JAVA?
- Currently, we are installing JRE of JAVA.
- Update the JAVA download URL & the extracted folder name in the `group_vars/all.yaml` file. 


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
