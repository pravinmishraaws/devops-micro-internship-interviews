---
id: Q0401
title: IAM Role vs User vs Policy — differences and use cases
difficulty: easy
week: 04
topics: [aws, iam]
tags: [aws, iam, security]
author: pravinmishraaws
reviewed: false
---

## Question
Contrast IAM users, roles, and policies with examples.

## Short Answer
- User: long-lived identity for a person/app (avoid keys if possible).
- Role: assumed, short-lived creds; preferred for workloads and cross-account.
- Policy: permissions JSON attached to identities/resources.

## References
- AWS IAM docs
