---
id: Q0655
title: Terraform remote state, backends, and locking
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
- Enable state locking using DynamoDB.
- Encourage team members to run terraform plan before apply to check for conflicts.

## References
- Terraform Docs — Backends
