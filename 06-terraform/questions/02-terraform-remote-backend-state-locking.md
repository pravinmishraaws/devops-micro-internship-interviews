---
id: 2
title: Terraform remote backend state locking
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, backend, state-locking]
author: Mobarak Hosen
reviewed: false
---

## Question

When working in a team how can you ensure no state conflict on remote-backend?

## Short Answer

- using state locking feature in terraform remote backend

## Deep Dive

When working in a team, we need the same state file for everyone to provisioning infrastructures. But it can happen that two members are running the `terraform apply` command at the same time and conflict arises.

To overcome such conflict, we can use terraform State locking that prevents team to modify terraform state file simultaneously, avoid corruption and conflicts.

For example: with `s3` remote backend, we can implement this way:

```hcl
terraform {
    backend "s3" {
        bucket         = "imshakil-bkt-tfstate"
        key            = "terraform.tfstate"
        region         = "ap-southeast-1"
        use_lockfile   = true
    }
}
```

Here we have used:

- `s3` as the remote backend
- `use_lockfile` to allow state-locking

### How does state-locking work?

- Terraform acquires a lock before state operations

- DynamoDB stores the lock with a unique ID

- S3 creates a lock file in the same bucket

- Other operations are blocked until the lock is released

- Lock automatically cleans up on normal completion

## Pitfalls

- Major drawback is someone can use `force-unlock` to break the state-lock with carelessly

- It can be time consuming due to network latency

## References

- [Official Docs](https://developer.hashicorp.com/terraform/language/state/locking)

## From the Project

The Petclinic Platform backend block in `terraform/environments/dev/main.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "petclinic-terraform-state"
    key            = "petclinic/dev/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "petclinic-terraform-locks"
    encrypt        = true
  }
}
```

When `terraform apply` runs in dev, Terraform acquires a lock in DynamoDB before modifying state. If a second engineer runs apply at the same time, they see: `Error: Error acquiring the state lock`. The lock entry tells you who holds it and when they started.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
