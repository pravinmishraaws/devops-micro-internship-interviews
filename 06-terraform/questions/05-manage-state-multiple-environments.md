---
id: 5
title: How do you manage Terraform state for multiple environments?
difficulty: medium
week: 06
topics: [terraform, state, s3, dynamodb]
tags: [terraform, state, s3, dynamodb, backend, environments]
author: pravinmishraaws
reviewed: true
---

## Question
How do you manage Terraform state for multiple environments (dev, prod)?

## Short Answer
Use a single S3 bucket with separate state keys per environment. DynamoDB handles locking to prevent concurrent applies from corrupting state.

## Deep Dive
S3 backend with separate state keys per environment. Dev state lives at `petclinic/dev/terraform.tfstate` and prod at `petclinic/prod/terraform.tfstate`. Same S3 bucket, different keys.

```hcl
terraform {
  backend "s3" {
    bucket         = "petclinic-tfstate"
    key            = "petclinic/dev/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "petclinic-tfstate-lock"
    encrypt        = true
  }
}
```

DynamoDB handles locking — if two engineers run `terraform apply` at the same time, one gets a lock error instead of corrupted state.

**What to say in the interview:** Say the bucket path. Say DynamoDB. Specificity signals hands-on experience. Anyone can say "we use remote state." Not everyone says "separate state keys per environment with DynamoDB locking."

## Pitfalls
- Using the same state key for dev and prod — a destroy in dev wipes prod state records
- Forgetting `encrypt = true` — state files contain secrets (passwords, keys) in plaintext
- No S3 versioning — without it you cannot recover from accidental state deletion

## References
- [Terraform Docs — S3 Backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
- [Terraform Docs — State Locking](https://developer.hashicorp.com/terraform/language/state/locking)

## From the Project

This is the exact setup used in the Petclinic Platform. The `terraform/environments/` directory has two root modules:

```
terraform/environments/
├── dev/    ← backend key: petclinic/dev/terraform.tfstate
└── prod/   ← backend key: petclinic/prod/terraform.tfstate
```

Both environments share the same S3 bucket and DynamoDB table, but separate state keys ensure dev changes never touch prod state. Running `terraform apply` in `environments/dev/` cannot affect `environments/prod/` — by design.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
