Question:
What is Ansible, and how does it differ from other configuration management tools like Puppet or Chef?

Answer:
Definition: Ansible is an open-source automation tool for configuration management, application deployment, and task automation. It uses YAML playbooks to define infrastructure as code.

Key Differences:

Agentless: No need to install agents on managed nodes; communicates over SSH.
Push-based: Configurations are pushed from control node to managed nodes.
Simple & Lightweight: Uses human-readable YAML; easier than Puppet/Chef.
Extensible: Modules for multiple platforms, cloud providers, and tasks.
Example Use Case:
Install Nginx on multiple servers with one playbook instead of logging into each server individually.
