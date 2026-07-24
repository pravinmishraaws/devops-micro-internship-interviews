---
id: 3
title: Benefits of Using Azure Bastion in a Three-Tier Architecture
difficulty: entry
week: 05
topics: [azure, networking, security, architecture]
tags: [azure-bastion, ssh, three-tier]
author: Tanisha Borana
reviewed: false
---

## Question
What are the benefits of using **Azure Bastion** in a **three-tier architecture**, and why is it used instead of directly connecting via SSH?

## References
- [Microsoft Azure Documentation - What is Azure Bastion?](https://learn.microsoft.com/en-us/azure/bastion/bastion-overview)
- [Microsoft Learn - Securely connect to VMs using Bastion](https://learn.microsoft.com/en-us/azure/bastion/connect-vm-bastion)


## From the Project

The Petclinic Platform avoids bastion hosts entirely. On AWS, the equivalent approach is AWS Systems Manager Session Manager:

- No open inbound port — no SSH, no RDP
- Full audit trail in CloudTrail — every session recorded with user identity and commands
- IAM-controlled access — same role-based model as the rest of the platform
- Works from AWS Console or CLI: `aws ssm start-session --target <instance-id>`

For EKS nodes specifically, direct node access is almost never needed — `kubectl exec` into the pod is faster and more targeted. Treat nodes as cattle.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
