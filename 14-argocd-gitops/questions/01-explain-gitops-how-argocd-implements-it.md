---
id: 1
title: Explain GitOps — how does ArgoCD implement it?
difficulty: medium
week: 14
topics: [argocd, gitops, kubernetes, cd]
tags: [argocd, gitops, sync, drift, continuous-delivery]
author: pravinmishraaws
reviewed: true
---

## Question
Explain GitOps. How does ArgoCD implement it?

## Short Answer
GitOps means Git is the single source of truth for what should be running in the cluster. ArgoCD watches a Git repo and continuously reconciles the cluster to match. If the cluster drifts from Git — someone scales a deployment manually, deletes a ConfigMap — ArgoCD detects it and corrects it.

## Deep Dive
The GitOps loop has four steps:

1. **Developer merges a PR** — a new image tag, a config change, a new service
2. **CI pushes to ECR and commits the new image tag to Git** — the `helm-values/` directory is updated
3. **ArgoCD detects the Git change** — it polls the repo (or receives a webhook) and sees the diff
4. **ArgoCD syncs the cluster** — it applies the change; dev auto-syncs, prod requires manual approval

```
GitHub Actions → build image → push to ECR → commit image tag to helm-values/
                                                        ↓
                                              ArgoCD detects commit
                                                        ↓
                                         Auto-sync (dev) / Manual sync (prod)
```

**Drift correction:** If someone runs `kubectl scale deployment api-gateway --replicas=5` directly on the cluster, ArgoCD marks the application as `OutOfSync` and reverts it to the 2 replicas specified in Git. The cluster always converges to Git.

**Why manual sync for prod?** Because prod deployments always need a human gate. You want someone to look at what ArgoCD is about to apply before it touches production.

## Pitfalls
- Disabling auto-sync without a process for manual syncs — Git and the cluster drift indefinitely
- Storing secrets in Git — use External Secrets Operator or Sealed Secrets instead
- Not setting `prune: true` in the sync policy — deleted resources in Git remain running in the cluster

## References
- [ArgoCD Docs — Core Concepts](https://argo-cd.readthedocs.io/en/stable/core_concepts/)
- [ArgoCD Docs — Sync Policies](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)

## From the Project

The Petclinic Platform's full GitOps loop:

1. Developer pushes code → GitHub Actions builds the Docker image, pushes to ECR with the commit SHA as the tag
2. GitHub Actions commits the new image tag to `helm-values/api-gateway/dev.yaml` in the `petclinic-platform` repo
3. ArgoCD detects the new commit (polls every 3 minutes or via webhook) and applies the updated Helm release to the `petclinic-dev` namespace
4. If someone manually scales a deployment in the cluster — `kubectl scale deployment api-gateway --replicas=5` — ArgoCD detects the drift on the next sync and reverts it back to the declared state

Dev is auto-sync. Prod is manual sync — a human must approve the sync in the ArgoCD UI. That is the human gate for production.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
