---
id: bhupen-Q0601
title: Terraform remote state, backends, and locking
difficulty: easy
week: 06
topics: [terraform, state]
tags: [terraform, state, s3, dynamodb, backend]
author: pravinmishraaws
reviewed: false
---

## Question
When we run terraform init, it initialise backend. Where we can see that backend?

## Short Answer
- Remote state centralizes outputs and prevents drift.
- S3 backend + DynamoDB lock: prevents concurrent applies.

## References
- Terraform Docs — Backends
