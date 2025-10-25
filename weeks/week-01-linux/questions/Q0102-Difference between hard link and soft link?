---
id: Q0102
title: Difference between hard link and soft link?
difficulty: easy
week: 01
topics: [linux, permissions]
tags: [linux, permissions, acl]
author: supuni96
reviewed: false
---

## Question
Differentiate between a hard link and a soft (symbolic) link in Linux.

## Short Answer
- Hard link: Points directly to inode.
            Check inode information using:
             ls -i
             Output:
            1842324 myfile.txt
            → Here 1842324 is the inode number.

- Soft link: Points to a file path.
- Hard links can’t span filesystems or link to directories.


## Deep Dive
- Hard link shares the same inode; deleting the original doesn’t remove data until all links are deleted.
- Soft link breaks if the target file is removed.

## Pitfalls
- Using hard links across partitions fails.

## References
- ln, ls -li




