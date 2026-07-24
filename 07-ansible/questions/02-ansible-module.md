---
id: 2
title: Ansible Modules — purpose and usage
difficulty: easy
week: 07
topics: [ansible, Modules]
tags: [ansible, Modules, reuse, galaxy]
author: rukevwe
reviewed: false

---

## Questio
what is Anible Modules?
How do module help  perform  configuration  tasks on managed hosts
How can you find or use build-in module


## References
- Ansible Docs — Modules

---

## From the Project

The Petclinic Platform does not use Ansible modules — infrastructure is provisioned with Terraform and application configuration is managed through Kubernetes ConfigMaps and AWS Secrets Manager.

In a fully containerised EKS deployment, the operations Ansible modules typically handle are done differently:

- Package installation → baked into the Docker image at build time
- Configuration files → ConfigMaps or Secrets mounted into pods
- Service management → Kubernetes Deployment restarts via `kubectl rollout restart`

If you work in a hybrid environment (some VMs, some containers), Ansible and Kubernetes coexist naturally — Ansible for the VM layer, Kubernetes for the container layer.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
