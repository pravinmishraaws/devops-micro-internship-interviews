---
id: 5
title: How do you roll back a broken deployment in a GitOps workflow?
difficulty: medium
week: 14
topics: [argocd, gitops, rollback, incident-response]
tags: [argocd, rollback, git-revert, incident-response, self-heal, prod]
author: pravinmishraaws
reviewed: true
---

## Question
A bad deployment just went to prod. How do you roll back using GitOps? What is different from a traditional `kubectl rollout undo`?

## Short Answer
In GitOps, rollback is a git revert. You revert the commit that updated the image tag, push it, and ArgoCD redeploys the previous version. The rollback itself is a commit — auditable, reviewable, and tracked in history like any other change.

## Deep Dive
**Traditional rollback:**
```bash
kubectl rollout undo deployment/customers-service -n petclinic-prod
```
- Fast, but not in Git
- The cluster state is now out of sync with what Git says it should be
- If ArgoCD has `selfHeal: true`, it will immediately revert the `kubectl` rollback, fighting the operator
- No audit trail — you know it happened but not who did it or why

**GitOps rollback:**
```bash
# Find the last good commit
git log helm-values/prod/customers-service.yaml

# Revert the bad image tag commit
git revert abc1234

# Push — ArgoCD detects the new commit and re-syncs to the previous image tag
git push origin main
```

ArgoCD re-deploys the previous image SHA. The cluster is in sync with Git. The revert commit is the audit trail.

**Why revert, not reset?** `git revert` creates a new commit that undoes the change — safe to push to a shared branch. `git reset --hard` rewrites history — dangerous on a branch other people are working from.

**Time-to-rollback:** the limiting factor is how fast the revert commit lands and ArgoCD syncs. In practice: 30 seconds to write and push the revert, plus ArgoCD's polling interval (default 3 minutes) or webhook (near-instant). Total: under 5 minutes.

**If the bad deploy broke the cluster and ArgoCD is also affected:** fall back to `kubectl apply -f` with the previous known-good manifest. But this should be the exception — normal rollbacks always go through Git.

## Pitfalls
- Using `kubectl rollout undo` when ArgoCD `selfHeal` is enabled — ArgoCD reverts the rollback immediately, making the incident worse
- Not knowing the previous good image tag — this is why you tag images with the commit SHA, not `latest`
- Reverting the wrong file — in a multi-service repo, make sure you revert only the service that regressed
- Not communicating during the rollback — in a team, announce in the incident channel before pushing the revert so no one pushes conflicting changes

## References
- [ArgoCD Docs — Rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/)
- [ArgoCD Docs — Sync Policy — Self Heal](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-self-healing)

## From the Project

The Petclinic Platform's GitOps rollback process is documented in `docs/runbook.md`. The process:

1. Identify which service is broken and the commit SHA of the bad image
2. `git revert <commit>` in the `helm-values/prod/` path for that service
3. Push to `main`
4. ArgoCD detects the revert and re-syncs prod to the previous image SHA
5. Verify the rollback with `kubectl rollout status deployment/<service> -n petclinic-prod`

Prod does not have auto-sync — so step 4 requires a manual sync trigger in the ArgoCD UI. That is intentional: even the rollback is a deliberate human action, not an automatic one.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
