# Deploy JAR file to a Linux VM using Ansible

If you like to deploy your JAVA application on a VM using Ansible, you are in the right spot.  Just copy the examples we have here and change as needed. 

- Build: JAR file and push to Nexus
- Deployment:  Using Ansible script to deploy the application on Server. Check [ansible readme doc](./deploy/playbooks/README.md)
  - Ansible script connect to VM and install JAVA
  - Creates the SystemD file to run the JAVA JAR as a Linux Service
  - Downloads the JAR from Nexus
  - Start the Linux Service

