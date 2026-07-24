---
id: 5
title: "How do you secure SSH access to production servers?"
difficulty: medium
week: 01
topics: [linux, security, ssh]
tags: [ssh-hardening, security-best-practices, access-control]
author: nkydigitech
reviewed: false
---

## Question
How would you secure SSH access to production servers? Discuss multiple layers of security.

## Short Answer
- Use SSH key authentication only, disable root login, and change the default port from 22 in `/etc/ssh/sshd_config` to reduce attack surface.
- Implement fail2ban to automatically block brute-force attempts, restrict SSH access by IP using firewall rules, and consider adding a bastion host or VPN for extra protection.
- Enable two-factor authentication with tools like Google Authenticator, set up alerts for SSH logins, and regularly review `/var/log/auth.log` for suspicious activity.

## Deep Dive

**Layer 1: SSH Configuration Hardening**

Edit `/etc/ssh/sshd_config` with these security settings:
```bash

## From the Project

The Petclinic Platform avoids SSH access to production nodes entirely:

- **Pod debugging:** `kubectl exec -it <pod> -- /bin/sh` — shell into a running container without touching the node
- **Node access (if unavoidable):** AWS Systems Manager Session Manager — no SSH port open, no key pair management, full audit trail in CloudTrail
- **EKS node security group:** no inbound rule for port 22

This is the recommended posture for production EKS: treat nodes as cattle, not pets. If a node needs investigation, drain it and inspect the pod on a healthy node instead.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
