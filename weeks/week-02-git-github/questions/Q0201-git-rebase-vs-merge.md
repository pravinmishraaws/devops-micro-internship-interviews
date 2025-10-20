---
id: Q0201
title: Rebase vs Merge — why and when?
difficulty: easy
week: 02
topics: [git, branching]
tags: [git, rebase, merge, history]
author: pravinmishraaws
reviewed: false
---

## Question
When should you use `git rebase` vs `git merge`? Trade-offs?

## Short Answer
- Merge: preserves history; safer for shared branches.
- Rebase: linear history; cleaner but rewrites commits; avoid rebasing shared branches.

## Deep Dive
- Example flows: feature→main with merge commit vs rebase+FF.

## Pitfalls
- Rebasing pushed branches breaks collaborators.

## References
- Git Book — Rebasing
