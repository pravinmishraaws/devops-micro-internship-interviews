---
id: 5
title: IaaS vs PaaS - VM vs App Service
difficulty: entry
week: 05
topics: [azure, compute, app-service]
tags: [Azure, compute, iaas, paas, vm, app-service]
author: [Syedsaleha]
reviewed: false
---

## Question

When would you choose to deploy an application on an Azure Virtual Machine (VM) versus an Azure App Service?

## References

- Microsoft Learn: Choose an Azure compute service

## From the Project

The Petclinic Platform uses neither Azure VMs nor Azure App Service — it runs containerised workloads on Amazon EKS. The AWS equivalent decision matrix:

| Option | Azure | AWS |
|---|---|---|
| Managed Kubernetes | AKS | Amazon EKS |
| Managed containers | Azure Container Apps | AWS Fargate / ECS |
| Full VM control | Azure Virtual Machines | Amazon EC2 |

The petclinic choice — EKS — prioritises control and portability. Standard Kubernetes manifests work on any cluster, not a platform-specific configuration.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
