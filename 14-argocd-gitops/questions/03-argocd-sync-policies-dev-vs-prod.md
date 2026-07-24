---
id: 3
title: How do you configure ArgoCD sync policies differently for dev and prod?
difficulty: medium
week: 14
topics: [argocd, gitops, sync, environments, deployment]
tags: [argocd, sync-policy, auto-sync, manual-sync, prune, self-heal, prod-gate]
author: pravinmishraaws
reviewed: true
---

## Question
How do you configure ArgoCD sync policies for dev versus prod? Why would prod require a different approach?

## Short Answer
Dev uses auto-sync — ArgoCD detects a commit to the dev configuration and deploys immediately. Prod uses manual sync — a human must click "Sync" in the ArgoCD UI or run `argocd app sync` to deploy. Prod always needs a human gate because you want eyes on what is going to change before it hits real users.

## Deep Dive
ArgoCD sync policy is set in the `Application` CRD:

**Dev — auto-sync with self-heal and prune:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: petclinic-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/pravinmishraaws/petclinic-platform
    targetRevision: main
    path: helm-values/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: petclinic-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

- `automated:` — enables auto-sync
- `prune: true` — deletes resources in the cluster that no longer exist in Git
- `selfHeal: true` — reverts manual changes made directly to the cluster (drift correction)

**Prod — manual sync (no `automated:` block):**
```yaml
spec:
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```

No `automated:` key means sync only happens when triggered manually. The ArgoCD UI shows prod as `OutOfSync` when new changes are committed — it is the operator's decision when to apply them.

**RBAC for the human gate:** in a team, you can restrict who can trigger a prod sync using ArgoCD RBAC policies — only the ops team lead has `sync` permission on the prod Application.

**Sync windows:** ArgoCD supports sync windows to block automated syncs during maintenance windows or peak hours, even for dev. Useful for preventing accidental deploys on Friday afternoon.

## Pitfalls
- Enabling `selfHeal: true` in prod — if an operator manually adjusts a pod's resource limit to handle an incident, ArgoCD will revert it within minutes
- Enabling auto-sync in prod without a sync window — a bad commit can reach prod the moment it is merged
- Not enabling `prune: true` in dev — deleted services linger as ghost resources in the cluster
- Forgetting `CreateNamespace=true` on first deploy — ArgoCD cannot create the namespace and the sync fails

## References
- [ArgoCD Docs — Automated Sync Policy](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
- [ArgoCD Docs — Sync Options](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)
- [ArgoCD Docs — Sync Windows](https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/)

## From the Project

The Petclinic Platform has two ArgoCD Application CRDs — one per environment — in `k8s/argocd/applications/`:

- `k8s/argocd/applications/dev/` — auto-sync with prune and self-heal. When GitHub Actions pushes a new image tag to `helm-values/dev/`, ArgoCD picks it up and deploys within seconds.
- `k8s/argocd/applications/prod/` — no `automated:` block. After a dev deploy is verified, a team member manually triggers the prod sync. This is the human gate that prevents an untested build from reaching prod.

This pattern is what the specificity question in Lecture 17.2 points to: "ArgoCD detects that commit and auto-deploys to dev. Prod requires a manual sync — because prod always needs a human gate."

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
