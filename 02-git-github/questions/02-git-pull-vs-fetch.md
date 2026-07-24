---
id: 2
title: git pull vs git fetch — difference
difficulty: easy
week: 02
topics: [git, branching]
tags: [git, pull, fetch, history]
author: mazpugo
reviewed: false
---

## Question
What is the difference between git pull and git fetch?




## From the Project

In the Petclinic Platform's GitOps workflow, fetch vs. pull has a practical implication:

- **ArgoCD** does a `git fetch` under the hood to check if the remote repo has new commits — it never auto-merges into a local branch. It compares the remote SHA against what is currently deployed.
- **Developers** running `git pull --ff-only` on `main` ensures local state is exactly in sync with the remote without accidentally creating a merge commit on a shared branch.

The rule: use `git fetch` to look, `git pull --ff-only` to sync. Never `git pull` with a merge on a branch ArgoCD is watching — the extra merge commit can confuse the diff.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
