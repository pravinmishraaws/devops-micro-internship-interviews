---
id: Q0101
title: POSIX permissions vs ACL — when to use which?
difficulty: easy
week: 01
topics: [linux, permissions]
tags: [linux, permissions, acl]
author: pravinmishraaws
reviewed: false
---

## Question
Explain POSIX rwx permissions and how ACLs extend them. When are ACLs appropriate?

## Short Answer
- POSIX: user/group/other with rwx bits.
- ACLs: fine-grained per-user/per-group entries.
- Use ACLs for exceptions; prefer groups for maintainability.

## Deep Dive
- `chmod`, `setfacl`, `getfacl`; default ACLs on directories.

## Pitfalls
- Hidden defaults causing unexpected inheritance.

## References
- man `chmod`, `setfacl`
