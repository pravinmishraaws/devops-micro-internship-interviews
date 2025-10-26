---
id: Q0627
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
