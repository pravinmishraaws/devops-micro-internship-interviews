---
id: 1
title: AWS IAM Permission
difficulty: easy
week: 4
topics: [aws iam]
tags: [aws IAM policy permission]
author: Raji
reviewed: false
---

## Question
Why does chaining multiple AssumeRole operations cause token expiration even if the parent role has valid permissions

## Short Answer

## References
- AWS IAM Policy Permission docs

## From the Project

The Petclinic Platform uses IAM roles — never IAM users or access keys — for all service-to-service access:

- **GitHub Actions → AWS:** OIDC federation — no long-lived credentials, IAM role assumed at runtime via trust policy
- **EKS pods → AWS services:** IRSA (IAM Roles for Service Accounts) — pods assume scoped roles via OIDC without any credentials stored in the pod
- **Terraform → AWS:** run locally with AWS CLI credentials, or via CI using the OIDC role

Every identity gets exactly the permissions it needs for exactly the resources it touches. No wildcard policies, no `*` on sensitive actions.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
