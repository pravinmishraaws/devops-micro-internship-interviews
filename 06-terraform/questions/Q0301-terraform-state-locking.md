---
id: Q0301
title: How does Terraform state locking work and what happens when it breaks?
difficulty: hard
week: 03
topics: [terraform, iac, state-management]
tags: [terraform, state, locking, s3, dynamodb, backend]
author: JulietChinenyeDuru
reviewed: false
---

## Short Answer
Terraform uses a state lock to prevent concurrent applies from corrupting infrastructure state. With an S3 + DynamoDB backend, S3 stores the state file and DynamoDB holds the lock record. A broken lock requires manual intervention to avoid split-brain infrastructure.

## Deep Dive
When you run `terraform apply`, Terraform:
1. Acquires a lock (writes a record to DynamoDB with a `LockID`)
2. Reads current state from S3
3. Plans and applies changes
4. Writes updated state back to S3
5. Releases the lock (deletes the DynamoDB record)

If a process crashes mid-apply, the lock remains. This causes `Error: Error locking state` for all subsequent runs.

**Backend config:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Force-unlock (use with extreme caution):**
```bash
# Get the Lock ID from the error message
terraform force-unlock <LOCK_ID>
```

**State file corruption recovery:**
- S3 versioning must be enabled — roll back with `aws s3api get-object --version-id`
- Never edit state files manually unless using `terraform state` subcommands

## Pitfalls
- Running `terraform force-unlock` when another legitimate apply is in progress — causes state corruption
- Not enabling S3 versioning — no recovery path if state is corrupted
- Sharing one state file across environments — use workspaces or separate backends per environment
- Using local state in CI/CD — no locking, no shared visibility, guaranteed drift

## References
- https://developer.hashicorp.com/terraform/language/settings/backends/s3
- https://developer.hashicorp.com/terraform/cli/commands/force-unlock