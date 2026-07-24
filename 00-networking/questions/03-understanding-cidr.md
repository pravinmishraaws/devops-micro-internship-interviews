---
id: 3
title: Understanding CIDR — how IP address ranges work
difficulty: entry
week: 00
topics: [networking, ip-addressing]
tags: [cidr, ip, networking, subnetting]
author: "[Hajixhayjhay](https://github.com/Hajixhayjhay)"
reviewed: false
---

## Question
What is CIDR notation, and how does it define IP address ranges in networks?

## Short Answer


## Deep Dive


## Pitfalls


## References


## From the Project

The Petclinic Platform VPC uses deliberate CIDR allocation to separate concerns while keeping costs low:

- **VPC CIDR:** `10.0.0.0/16` — 65,536 addresses, room to grow
- **Public subnets (2 AZs):** `/24` each — EKS nodes and the ALB sit here; no NAT Gateway needed (saves ~$35/month)
- **RDS subnet group:** same subnets, isolated by a security group that allows port 3306 only from the EKS node security group

The all-public subnet design is a deliberate cost trade-off for a learning environment. In production with stricter compliance requirements, database subnets would be private with a NAT Gateway for outbound traffic.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
