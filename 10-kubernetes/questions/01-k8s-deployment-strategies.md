---
id: 1
title: Rolling vs Blue/Green vs Canary in Kubernetes
difficulty: medium
week: 10
topics: [kubernetes, deployments]
tags: [rolling, blue-green, canary, argocd]
author: pravinmishraaws
reviewed: false
---

## Question
Compare the three strategies and when to use each. Include example manifests or tools.

## References
- Kubernetes Docs — Deployments
- Argo Rollouts

## From the Project

The Petclinic Platform uses rolling update strategy for all eight microservices:

- **Dev environment:** 1 replica per service — rolling update replaces the single pod; new pod starts, passes the readiness check, old pod terminates
- **Prod environment:** 2+ replicas — rolling update ensures at least 1 replica is always serving traffic during the update
- **Readiness probes:** every service exposes `/actuator/health/readiness` — Kubernetes waits for the new pod to pass the check before sending traffic to it and before terminating the old one

Blue/green and canary are not used in this project. The GitOps rollback model (git revert → ArgoCD re-deploys) provides the safety net instead of parallel environments.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
