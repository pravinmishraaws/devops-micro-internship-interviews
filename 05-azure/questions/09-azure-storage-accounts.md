---
id: 9
title: Azure Storage Accounts - choosing the right service for unstructured data
difficulty: easy
week: 05
topics: [azure, storage, blob]
tags: [azure, storage, blob, files]
author: https://github.com/Dudubynatur3
reviewed: false
---

## Question
Your application needs to store images and large unstructured files. Which Azure Storage service would you choose, and why?

## Short Answer


## Deep Dive


## Pitfalls


## References
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction
- https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview

## From the Project

The Petclinic Platform uses Amazon S3 as its equivalent to Azure Storage Accounts. S3 in this project:

- **Terraform remote state:** `petclinic-terraform-state` bucket stores state at `petclinic/dev/terraform.tfstate` and `petclinic/prod/terraform.tfstate`
- **Versioning enabled:** every state file change is versioned — rollback is possible if a bad apply corrupts state
- **Encryption:** server-side encryption with AWS-managed keys (SSE-S3)
- **Access control:** bucket policy allows access only from the Terraform IAM role — no public access

Conceptual mapping: Azure containers = S3 buckets, Azure blobs = S3 objects, Azure SAS tokens = S3 presigned URLs.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
