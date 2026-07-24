---
id: 1
title: Rebase vs Merge — why and when?
difficulty: easy
week: 02
topics: [git, branching]
tags: [git, rebase, merge, history]
author: pravinmishraaws
reviewed: false
---

## Question
When should you use `git rebase` vs `git merge`? Trade-offs?

## Short Answer
- Merge: preserves history; safer for shared branches.
- Rebase: linear history; cleaner but rewrites commits; avoid rebasing shared branches.

## Deep Dive
- Example flows: feature→main with merge commit vs rebase+FF.

## Pitfalls
- Rebasing pushed branches breaks collaborators.

## References
- Git Book — Rebasing

## From the Project

The Petclinic Platform uses a GitOps delivery model — Git history quality directly affects incident response speed:

- **In `petclinic-platform` (infra repo):** rebasing feature branches onto main before merging keeps a linear history. When an alert fires, `git log --oneline helm-values/` immediately shows what changed and when.
- **In the GitOps loop:** ArgoCD tracks commits to the `helm-values/` directory. A clean, rebased history makes it trivial to identify which commit introduced a bad image tag — and which `git revert` will fix it.

Linear history is not just aesthetic — it is operational. Merge commits create noise that slows down incident response.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
