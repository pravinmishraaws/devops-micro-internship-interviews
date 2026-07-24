---
id: 1
title: Resource Groups, VNets, Subnets, NSGs — how they fit
difficulty: entry
week: 05
topics: [azure, networking]
tags: [azure, resource-groups, vnet, subnet, nsg]
author: pravinmishraaws
reviewed: false
---

## Question
Explain the relationship between RG, VNet, Subnet, and NSG and common patterns.

## References
- Microsoft Learn — Virtual Networks
## From the Project

The Petclinic Platform is deployed on AWS, not Azure. The AWS equivalents of Azure's core networking constructs:

| Azure | AWS Equivalent |
|---|---|
| Resource Group | Tags + separate AWS accounts per environment |
| VNet | VPC (Virtual Private Cloud) |
| Subnet | Subnet — same concept, same CIDR notation |
| NSG | Security Group (stateful) + Network ACL (stateless) |
| Azure Bastion | AWS Systems Manager Session Manager |

If you are interviewing for an AWS role after Azure experience — lead with the concept, then name the AWS tool. Interviewers value engineers who understand the pattern, not just the product name.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
