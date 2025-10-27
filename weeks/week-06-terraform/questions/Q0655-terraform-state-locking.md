---
id: Q0655
title: Terraform Remote State, Backends, and Locking
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, state, s3, dynamodb, backend]
author: Emmanuel Ulu
reviewed: false
---

## Question
When working in a team, how can you ensure no state conflict occurs when using a remote backend stored in an S3 bucket?

## Short Answer
- Use a remote backend (S3) for centralized state storage.  
- Enable **state locking** using **DynamoDB**.  
- Encourage team members to run `terraform plan` before `terraform apply` to check for potential conflicts.

## Deep Dive
When multiple engineers work with Terraform, using a **remote backend** like Amazon S3 ensures everyone shares a single source of truth for infrastructure state.  
To prevent simultaneous modifications, **state locking** is enabled with **DynamoDB**.  
When one user runs `terraform apply`, Terraform places a lock record in the DynamoDB table—blocking others until the operation completes.  
This mechanism prevents race conditions, partial updates, and corrupted states.  

For reliability:
- Ensure the DynamoDB table exists and has proper IAM access.
- Combine S3 versioning and DynamoDB locking for full protection.

## Pitfalls
- If the DynamoDB lock table is deleted or misconfigured, state conflicts can occur.  
- Without proper IAM permissions, Terraform may fail to create or release locks.  
- Manually removing locks can lead to overlapping changes if done carelessly.

## Reference
- [Terraform Docs – State Locking](https://developer.hashicorp.com/terraform/language/state/locking)