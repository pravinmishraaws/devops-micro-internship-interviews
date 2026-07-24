---
id: 1
title: Stages, Environments, and Approvals in Azure Pipelines
difficulty: medium
week: 08
topics: [azure-devops, pipelines]
tags: [azure-devops, pipelines, approvals]
author: pravinmishraaws
reviewed: false
---

## Question
Design a multi-stage pipeline with approvals and gates.

## References
- Azure Pipelines Environments

## From the Project

The Petclinic Platform uses GitHub Actions, not Azure Pipelines. The concepts of stages, environments, and approvals map directly:

| Azure Pipelines | GitHub Actions equivalent |
|---|---|
| Stage | Job with `needs:` dependency |
| Environment with approval | `environment:` with required reviewers |
| Service connection | OIDC role assumption — no stored credentials |
| Artifact | Docker image pushed to ECR, tagged with commit SHA |

In the petclinic CI pipeline: the build job produces a Docker image, pushes it to ECR, then commits the new image tag to `helm-values/`. ArgoCD picks up that commit and deploys — automatically to dev, manually approved for prod.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
