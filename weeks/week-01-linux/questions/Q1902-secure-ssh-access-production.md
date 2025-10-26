---
id: Q1902
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
