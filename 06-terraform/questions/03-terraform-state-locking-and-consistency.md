---
id: 3
title: Terraform remote state, backends, and locking
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, state, s3, dynamodb, backend]
author: Emmanuel Ulu
reviewed: false
---

## Question
When working in a team, how can you ensure no state conflict occurs when using a remote backend stored in an S3 bucket?

## Short Answer
- Use a remote backend (S3) for centralized state storage.
- Enable state locking using DynamoDB.
- Encourage team members to run terraform plan before apply to check for conflicts.

## References
- Terraform Docs — Backends

## From the Project

State consistency is a real concern on the Petclinic Platform — two engineers working on different modules (say, VPC changes and EKS node group changes) could both run `terraform apply` in the same environment simultaneously.

The DynamoDB lock prevents this. The lock is acquired before reading state, held during plan and apply, and released after apply completes. If the apply crashes mid-run, the lock remains. Clear it with `terraform force-unlock <lock-id>` — only after confirming no other apply is actually running.

Consistent state is what makes it safe for a team to share infrastructure. Without it, the second apply works on stale state and may destroy resources the first apply just created.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
