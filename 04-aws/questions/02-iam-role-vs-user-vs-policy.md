---
id: 2
title: IAM Role vs User vs Policy — differences and use cases
difficulty: easy
week: 04
topics: [aws, iam]
tags: [aws, iam, security]
author: pravinmishraaws
reviewed: false
---

## Question
Contrast IAM users, roles, and policies with examples.

## Short Answer
- User: long-lived identity for a person/app (avoid keys if possible).
- Role: assumed, short-lived creds; preferred for workloads and cross-account.
- Policy: permissions JSON attached to identities/resources.

## References
- AWS IAM docs

## From the Project

The Petclinic Platform has zero IAM users for machine access. Every non-human identity is an IAM role:

| Identity | Role | Trust |
|---|---|---|
| GitHub Actions | `petclinic-github-actions` | OIDC — `token.actions.githubusercontent.com` |
| External Secrets Operator | `petclinic-eso-role` | IRSA — specific service account + namespace |
| ALB Ingress Controller | `petclinic-alb-role` | IRSA |
| Karpenter | `petclinic-karpenter-role` | IRSA |

Policies are scoped per role — the ESO role can only read from Secrets Manager, the ALB role can only manage load balancers. No role can do everything.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
