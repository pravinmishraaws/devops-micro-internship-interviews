---
id: 4
title: How does the image tag update flow work in a GitOps pipeline?
difficulty: medium
week: 14
topics: [argocd, gitops, cicd, github-actions, ecr, helm]
tags: [gitops, image-tag, github-actions, argocd, ecr, helm-values, commit-sha]
author: pravinmishraaws
reviewed: true
---

## Question
Walk me through the full flow from a developer pushing code to the new image running in Kubernetes. How does ArgoCD know what version to deploy?

## Short Answer
GitHub Actions builds the image, tags it with the commit SHA, and pushes to ECR. Then it commits the new image tag to a values file in the Git repo. ArgoCD detects that commit and re-syncs the deployment with the new tag. The deployment history is in Git — every deploy is a commit.

## Deep Dive
The flow has two separate GitHub Actions workflows:

**Workflow 1 — Build and push (`build-push.yml`):**
```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    file: docker/Dockerfile
    platforms: linux/arm64
    push: true
    tags: |
      ${{ env.ECR_REGISTRY }}/petclinic-customers-service:${{ github.sha }}
      ${{ env.ECR_REGISTRY }}/petclinic-customers-service:latest
```

Image tag is the commit SHA — `abc1234`. Not `latest` alone. Using `latest` makes rollbacks impossible because you cannot tell which commit `latest` points to.

**Workflow 2 — Update image tag (`update-image-tags.yml`):**
```yaml
- name: Update image tag in helm-values
  run: |
    sed -i "s|tag: .*|tag: ${{ github.sha }}|" helm-values/dev/customers-service.yaml
    git config user.email "ci@github.com"
    git config user.name "GitHub Actions"
    git add helm-values/dev/customers-service.yaml
    git commit -m "ci: update customers-service tag to ${{ github.sha }}"
    git push
```

This commit to `helm-values/dev/` is what ArgoCD watches. The moment it lands, ArgoCD detects the repo is `OutOfSync` and (in dev) auto-syncs — pulling the new image tag and rolling out the updated deployment.

**Why separate workflows?** CI (build + push) and CD (tag update) have different concerns. The build workflow runs on every push. The tag update runs only when the build succeeds and the image is verified. Separating them gives you a clean gate between "image exists" and "image is deployed."

**Rollback:** revert the image tag commit in Git. ArgoCD re-syncs. The deployment rolls back to the previous image — no `kubectl rollout undo` required. The rollback is auditable in Git history.

## Pitfalls
- Using `latest` as the only tag — ArgoCD sees no change in the values file and does not re-sync; deployments appear stuck
- Committing the image tag update in the same workflow as the build — if the push fails halfway, the tag update may still run, pointing to a non-existent image
- Not using commit SHA — timestamp tags (`v1.2.3-20240101`) are harder to trace back to a specific code change
- Granting the GitHub Actions bot write access to the entire repo instead of just the `helm-values/` path

## References
- [GitHub Docs — GitHub Actions — docker/build-push-action](https://github.com/docker/build-push-action)
- [ArgoCD Docs — Tracking Strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/)
- [GitHub Docs — GITHUB_SHA](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables)

## From the Project

The Petclinic Platform uses this exact two-workflow pattern:

- `.github/workflows/build-push.yml` — builds all eight service images for `linux/arm64`, tags with the commit SHA, and pushes to ECR
- `.github/workflows/update-image-tags.yml` — commits the new SHA to the relevant file in `helm-values/dev/` (one YAML file per service)

The `helm-values/` directory is the handoff point between CI and CD. GitHub Actions writes to it; ArgoCD reads from it. Neither system needs to know how the other works — they communicate through a Git commit.

When an interviewer asks "how does ArgoCD know what to deploy?" — the answer is: a commit in `helm-values/`. Not a webhook, not a direct API call. Git is the source of truth.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
