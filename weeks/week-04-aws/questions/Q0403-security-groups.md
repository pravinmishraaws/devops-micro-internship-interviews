---
id: Q0403
title: Security Groups vs Network ACLs
difficulty: easy
week: 04
topics: [aws, networking, vpc, security]
tags: [security-group, nacl]
author: Nchedo Nnaji
reviewed: false
---

## Question
What is the difference between security groups and network ACLs, and when can both be used together for layered network protection in a real-world scenario?


## Short Answer
- Security Groups are stateful, instance-level firewalls that control inbound and outbound traffic for EC2 instances.
- Network ACLs (NACLs) are stateless, subnet-level firewalls that filter traffic entering or leaving a subnet.
They can be used together for layered defense.

## Deep Dive
Security Groups:
- Associated with ENIs or EC2 instances.
- Automatically allow return traffic (stateful).
- Rules are “allow only” — no explicit deny.
- Example: allow inbound HTTP (port 80) from ALB only.

Network ACLs:
- Applied at subnet level.
- Stateless — each rule must allow both inbound and outbound traffic.
- Support both “allow” and “deny” rules.
- Good for broad subnet filtering (e.g., deny all SSH from 0.0.0.0/0).

## Pitfalls
- Conflicting rules between NACL and Security Groups can block valid traffic.
- Forgetting NACL is stateless, requiring both inbound and outbound rules.
- Overcomplicating rules increases maintenance overhead.

## References
- AWS VPC Security Groups - https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
- AWS Network ACLs - https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html

