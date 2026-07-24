---
id: 8
title: How do you authenticate GitHub Actions to AWS without storing credentials?
difficulty: medium
week: 06
topics: [terraform, cicd, oidc, github-actions, iam, security]
tags: [oidc, github-actions, iam, assume-role, no-credentials, security, ci]
author: pravinmishraaws
reviewed: true
---

## Question
How do you give a GitHub Actions workflow permission to call the AWS API (to run Terraform, push to ECR, etc.) without storing AWS access keys as GitHub secrets?

## Short Answer
GitHub Actions supports OIDC — the workflow requests a short-lived JWT from GitHub's identity provider, exchanges it for temporary AWS credentials using `sts:AssumeRoleWithWebIdentity`, and uses those credentials for the job. No long-lived access keys stored anywhere.

## Deep Dive
**Setup — one-time in Terraform:**

1. Create an OIDC provider in IAM for GitHub:
```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}
```

2. Create an IAM role with a trust policy scoped to your specific repo:
```hcl
resource "aws_iam_role" "github_actions" {
  name = "petclinic-github-actions"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = aws_iam_openid_connect_provider.github.arn }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:pravinmishraaws/petclinic-platform:*"
        }
      }
    }]
  })
}
```

**In the workflow:**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/petclinic-github-actions
      aws-region: eu-central-1
```

The `id-token: write` permission allows the workflow to request a JWT from GitHub. `configure-aws-credentials` exchanges it for temporary STS credentials that last for the duration of the job.

**Why this is better than access keys:**
- Credentials are short-lived (15 minutes to 1 hour) — no rotation needed
- Scoped to a specific repo and branch — another repo cannot assume the same role
- No secrets to leak in logs, commits, or pull requests
- Revoked instantly by deleting the OIDC provider or the IAM role

## Pitfalls
- Missing `permissions: id-token: write` in the workflow — the JWT request fails silently and the assume-role call gets "not authorized"
- Over-scoping the trust policy condition — `repo:org/*:*` allows any repo in the org to assume the role; scope it to the specific repo and optionally the specific branch
- Giving the role `AdministratorAccess` — give it only what the workflow needs: ECR push, S3/DynamoDB for Terraform state, EKS describe for deployments
- Thumbprint rotation — AWS manages this automatically now, but if you hardcode the thumbprint and AWS rotates it, the OIDC provider breaks

## References
- [GitHub Docs — Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
- [AWS Docs — Creating OpenID Connect identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)

## From the Project

The `petclinic-github-actions` IAM role is provisioned in `terraform/modules/eks/` alongside the cluster. It has a trust policy locked to `repo:pravinmishraaws/petclinic-platform:*`.

The role has two policy attachments:
- ECR push permissions — to push built images to the eight petclinic ECR repositories
- S3 + DynamoDB access scoped to the `petclinic-tfstate` bucket and `petclinic-tfstate-lock` table — to run `terraform plan` and `terraform apply` from CI

Every workflow in `.github/workflows/` starts with the `aws-actions/configure-aws-credentials` step using this role. No `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` secrets exist in the GitHub repository settings.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
