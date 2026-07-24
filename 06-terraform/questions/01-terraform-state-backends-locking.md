---
id: 1
title: Terraform remote state, backends, and locking
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, state, s3, dynamodb, backend]
author: pravinmishraaws
reviewed: false
---

## Question
Why use remote state? How does locking work?

## Short Answer
- Remote state centralizes outputs and prevents drift.
- S3 backend + DynamoDB lock: prevents concurrent applies.

## References
- Terraform Docs — Backends

## From the Project

The Petclinic Platform's Terraform configuration uses exactly this setup:

- **Backend:** S3 bucket with separate keys per environment
  - Dev: `petclinic/dev/terraform.tfstate`
  - Prod: `petclinic/prod/terraform.tfstate`
- **Locking:** DynamoDB table `petclinic-terraform-locks` — prevents concurrent applies from corrupting state
- **Encryption:** state files encrypted at rest with SSE-S3
- **Versioning:** S3 versioning enabled — recover a previous state file if an apply goes wrong

These are not theoretical values. They are the exact paths used in the course project.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
