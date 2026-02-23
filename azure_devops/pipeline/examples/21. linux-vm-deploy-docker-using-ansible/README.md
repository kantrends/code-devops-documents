# Purpose
This document contains pipeline example to build your application. Create Docker Image and push to ACR (Azure Container Registry) and then deploy as containerized application to on-premises VM using Ansible. In addition to that, we use Filebeat to send Docker container logs to ECE (Elasticsearch) for the application teams to view the live & historical logs. 

# Advantage
- End-to-End automation
- No need server access for any developers.

# Pre-requisite
- Check [ansible readme doc](./deploy/playbooks/README.md) for pre-requisite setup on the Linux VM
- If you want to send logs to ECE stack, then follow the [ece-setup](../../../../general/ece-setup.md)
