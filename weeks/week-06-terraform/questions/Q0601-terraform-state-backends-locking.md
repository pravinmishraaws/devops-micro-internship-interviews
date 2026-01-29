---
id: Q0601
title: Terraform remote state, backends, and locking
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, state, s3, dynamodb, backend]
author: pravinmishraaws
reviewed: false
---

## Question
Why use remote state? How does locking work?

## Short Answer
- Remote state centralizes outputs and prevents drift.
- S3 backend + DynamoDB lock: prevents concurrent applies.

## References
- Terraform Docs — Backends
