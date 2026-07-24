---
id: 2
title: How do you roll back a deployment in a GitOps setup?
difficulty: medium
week: 14
topics: [argocd, gitops, rollback, kubernetes]
tags: [argocd, gitops, rollback, git-revert, deployment]
author: pravinmishraaws
reviewed: true
---

## Question
A bad release went to production. How do you roll back in a GitOps setup?

## Short Answer
Git revert. Revert the commit that updated the image tag. ArgoCD detects the revert and redeploys the previous image automatically. No `kubectl` commands, no emergency access to the cluster.

## Deep Dive
In a GitOps setup, the cluster state is defined by Git. Rolling back means reverting Git to a previous state — ArgoCD does the rest.

```bash
# Find the commit that updated the bad image tag
git log --oneline helm-values/api-gateway.yaml

# Revert it
git revert <commit-sha>
git push origin main
```

ArgoCD sees the new commit (the revert), detects that the cluster is out of sync with Git, and re-applies the previous image tag. The rollback happens without anyone touching `kubectl`.

**Why this matters in an interview:** The rollback is auditable. It is a Git commit with a timestamp and an author. You can see exactly what was reverted, when, and by whom. Compare that to running `kubectl set image` — that change exists only in cluster state, with no record in your source of truth.

**What about ArgoCD's built-in rollback UI?** ArgoCD has a rollback button that reverts to a previous sync. Avoid it for production — it puts the cluster in a state that disagrees with Git, which means ArgoCD will try to re-sync forward on the next cycle. Always use `git revert`.

## Pitfalls
- Using `kubectl rollout undo` — this bypasses Git entirely, the cluster and Git are now out of sync
- Using the ArgoCD rollback UI button for production — same problem, Git and cluster diverge
- Not having image tags in Git (using `latest`) — you cannot revert what was not recorded

## References
- [ArgoCD Docs — Application History and Rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/app_deletion/)
- [GitOps Principles — OpenGitOps](https://opengitops.dev/)

## From the Project

On the Petclinic Platform, a bad deployment is rolled back with two Git commands:

```bash
# Find the commit that updated the image tag
git log --oneline helm-values/api-gateway/

# Revert it
git revert <commit-sha>
git push origin main
```

ArgoCD detects the revert commit and applies the previous image tag — without any kubectl access, without any manual cluster changes, with a full audit trail in Git.

Why not `kubectl rollout undo`? It works once, but ArgoCD will overwrite it on the next sync. Git revert is permanent, traceable, and the correct answer in a GitOps system.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
