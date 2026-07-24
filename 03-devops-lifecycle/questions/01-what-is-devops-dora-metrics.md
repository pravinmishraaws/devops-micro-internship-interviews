---
id: 1
title: What is DevOps? Explain DORA metrics.
difficulty: entry
week: 03
topics: [devops, dora]
tags: [devops, dora, metrics]
author: pravinmishraaws
reviewed: false
---

## Question
Define DevOps and the four DORA metrics. How do they guide improvement?

## Short Answer
- DevOps: collaboration + automation for faster, safer delivery.
- DORA: deployment frequency, lead time, change failure rate, MTTR.

## Deep Dive
- How to measure each; examples of improving DF/MTTR.

## References
- Accelerate (Forsgren et al.)

## From the Project

The Petclinic Platform is built to demonstrate exactly what DORA metrics measure:

- **Deployment frequency:** GitHub Actions triggers on every commit to main — a new image is built, pushed to ECR, and deployed to dev automatically
- **Lead time for changes:** from `git push` to running in dev takes under 5 minutes (build + push + ArgoCD sync)
- **Change failure rate:** every deployment is traceable — `git log` on `helm-values/` shows every image tag change with its timestamp and author
- **Mean time to restore:** a bad deployment is fixed with `git revert` — ArgoCD detects the revert and re-deploys the previous image automatically

This is what a DORA-optimised delivery pipeline looks like in practice.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
